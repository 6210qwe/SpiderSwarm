# coding:utf-8
from typing import Union, List, Optional, Dict, Tuple

import aiomysql
import traceback
from loguru import logger


class AsyncMySQLClient:
    def __init__(self, host: str, user: str, password: str, db: str, port: int = 3306, loop=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.loop = loop
        self.pool = None

    async def connect(self):
        try:
            self.pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db,
                loop=self.loop,
                autocommit=True
            )
        except:
            print(f"connect error:{traceback.format_exc()}")

    async def close(self):
        self.pool.close()
        await self.pool.wait_closed()

    async def execute(self, query: str, args: tuple = None) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)
                return cur.rowcount

    async def executemany(self, query: str, args: list = None) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.executemany(query, args)
                return cur.rowcount

    async def fetchone(self, query: str, args: tuple = None) -> dict:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                return await cur.fetchone()

    async def fetchall(self, query: str, args=None) -> list:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                return await cur.fetchall()

    # async def insert(self, table: str, data: dict) -> int:
    #     """
    #     :param table: 表名
    #     :param data: 数据
    #     :return:
    #     """
    #     keys = ','.join(data.keys())
    #     values = ','.join(['%s'] * len(data))
    #     query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
    #     try:
    #         return await self.execute(query, tuple(data.values()))
    #     except:
    #         print(f"execute {query} with {data} failed, error{traceback.format_exc()}")
    #         return 0
    async def insert(self, table: str, data: Dict, return_id: bool = True) -> int:
        """
        插入数据并返回ID，支持自定义ID或自增ID

        :param table: 表名
        :param data: 要插入的数据字典
        :param return_id: 是否返回ID，自定义ID时设为False
        :return: 插入记录的ID，失败返回0
        """
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'

        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, tuple(data.values()))

                    # 获取ID逻辑
                    if return_id:
                        inserted_id = cur.lastrowid + 1
                        print(inserted_id)
                    else:
                        inserted_id = data.get('id', 0)  # 假设自定义ID字段为id

            # 打印日志（使用提供的ID或自增ID）
            provided_id = data.get('id', inserted_id)
            print(provided_id)
            if inserted_id > 0:
                logger.info(f"insert success【{table}】-【{provided_id}】")

            return inserted_id

        except Exception as e:
            print(f"插入失败: {str(e)}")
            return 0

    # async def insert_many(self, table: str, data_list: list) -> int:
    #     """
    #     :param table: 表名
    #     :param data_list: 数据列表
    #     :return:
    #     """
    #     keys = ','.join(data_list[0].keys())
    #     values = ','.join(['%s'] * len(data_list[0]))
    #     query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
    #     args = [tuple(data.values()) for data in data_list]
    #     try:
    #         return await self.executemany(query, args)
    #     except:
    #         print(f"execute {query} with {args} failed, error{traceback.format_exc()}")
    #         return 0
    # async def insert_many(self, table: str, data_list: List[Dict], return_id: bool = False) -> List[int]:
    #     """
    #     批量插入数据并返回自增ID列表，支持自定义ID
    #
    #     :param table: 表名
    #     :param data_list: 要插入的数据列表
    #     :param return_id: 是否返回自增ID，自定义ID时设为False
    #     :return: 插入记录的ID列表，失败返回空列表
    #     """
    #     if not data_list:
    #         logger.warning(f"批量插入数据为空，表: {table}")
    #         return []
    #
    #     keys = ','.join(data_list[0].keys())
    #     values = ','.join(['%s'] * len(data_list[0]))
    #     query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
    #     args = [tuple(data.values()) for data in data_list]
    #
    #     inserted_ids = []
    #     try:
    #         async with self.pool.acquire() as conn:
    #             async with conn.cursor() as cur:
    #                 # 执行批量插入
    #                 await cur.executemany(query, args)
    #
    #                 # 获取自增ID（仅支持MySQL风格批量插入）
    #                 if return_id:
    #                     first_id = cur.lastrowid
    #                     inserted_ids = list(range(first_id, first_id + len(data_list)))
    #                 else:
    #                     # 使用自定义ID
    #                     inserted_ids = [data.get('id', 0) for data in data_list]
    #
    #         # 打印成功日志
    #         if inserted_ids:
    #             logger.info(f"批量插入成功【{table}】-【{inserted_ids[0]}-{inserted_ids[-1]}】")
    #
    #         return inserted_ids
    #
    #     except Exception as e:
    #         print(f"批量插入失败: {str(e)}")
    #         print(traceback.format_exc())
    #         return []

    async def insert_many(self, table: str, data_list: list) -> int:
        """
        :param table: 表名
        :param data_list: 数据列表
        :return: 成功插入的记录数
        """
        if not data_list:
            logger.info(f"insert success【{table}】-【0条记录】")
            return 0

        keys = ','.join(data_list[0].keys())
        values = ','.join(['%s'] * len(data_list[0]))
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        args = [tuple(data.values()) for data in data_list]

        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.executemany(query, args)
                    affected_rows = cur.rowcount

                    if 'id' in data_list[0]:
                        ids = [str(data['id']) for data in data_list]
                    else:  # 尝试获取自增ID（适用于MySQL）
                        first_id = cur.lastrowid
                        ids = [str(first_id + i) for i in range(len(data_list))]

                    for id in ids:
                        logger.info(f"insert success【{table}】-【{id}】")
                    return affected_rows

        except Exception as e:
            logger.error(f"execute {query} with {args} failed, error:{str(e)}")
            return 0

    async def query_by_fields(
            self,
            table: str,
            fields: Union[str, List[str]] = "*",
            condition: Dict[str, any] = None,
            order_by: str = None,
            limit: int = None,
            offset: int = 0
    ) -> List[Dict]:
        """
        按指定字段查询数据

        :param table: 表名
        :param fields: 要查询的字段，默认查询所有字段
        :param condition: 查询条件，格式为 {字段: 值}
        :param order_by: 排序字段，如 "id DESC"
        :param limit: 限制返回结果数
        :param offset: 偏移量，用于分页
        :return: 查询结果列表
        """
        # 处理字段参数
        if isinstance(fields, list):
            fields_str = ", ".join(fields)
        else:
            fields_str = fields

        # 构建SQL
        sql = f"SELECT {fields_str} FROM {table}"
        where_clause, params = self._build_where_clause(condition)
        if where_clause:
            sql += f" WHERE {where_clause}"

        if order_by:
            sql += f" ORDER BY {order_by}"

        if limit is not None:
            sql += f" LIMIT {offset}, {limit}" if offset > 0 else f" LIMIT {limit}"

        try:
            return await self.fetchall(sql, params)
        except Exception as e:
            print(f"查询失败: {sql}, 错误: {str(e)}")
            print(traceback.format_exc())
            return []

    # 辅助方法：构建WHERE子句
    def _build_where_clause(
            self,
            condition: Dict[str, any]
    ) -> Tuple[Optional[str], Optional[Tuple]]:
        """
        构建WHERE子句和参数

        :param condition: 查询条件
        :return: (WHERE子句, 参数元组)
        """
        if not condition:
            return None, None

        clauses = []
        params = []

        for key, value in condition.items():
            # 处理特殊操作符（如包含、大于等）
            if isinstance(value, dict):
                op = next(iter(value.keys()))
                val = value[op]
                if op == "$in":
                    clauses.append(f"{key} IN ({', '.join(['%s'] * len(val))})")
                    params.extend(val)
                elif op == "$like":
                    clauses.append(f"{key} LIKE %s")
                    params.append(f"%{val}%")
                elif op == "$gt":  # 大于
                    clauses.append(f"{key} > %s")
                    params.append(val)
                elif op == "$lt":  # 小于
                    clauses.append(f"{key} < %s")
                    params.append(val)
                else:
                    clauses.append(f"{key} = %s")
                    params.append(val)
            else:
                clauses.append(f"{key} = %s")
                params.append(value)

        where_clause = " AND ".join(clauses)
        return where_clause, tuple(params)

    # 新增：按字段查询单条记录
    async def get_by_fields(
            self,
            table: str,
            fields: Union[str, List[str]] = "*",
            condition: Dict[str, any] = None,
            order_by: str = None
    ) -> Optional[Dict]:
        """
        按指定字段查询单条记录

        :param table: 表名
        :param fields: 要查询的字段
        :param condition: 查询条件
        :param order_by: 排序字段
        :return: 单条记录或None
        """
        results = await self.query_by_fields(
            table,
            fields,
            condition,
            order_by,
            limit=1
        )
        return results[0] if results else None
