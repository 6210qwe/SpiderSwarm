import asyncio
import aiomysql
from loguru import logger


class MySQLClient:
    def __init__(self, pool):
        self.pool = pool

    @classmethod
    async def create_client(cls, host, port, user, password, db, charset='utf8mb4'):
        """创建客户端并初始化连接池"""
        pool = await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            charset=charset,
            minsize=1,
            maxsize=10
        )
        return cls(pool)

    async def insert(self, table: str, data: dict, return_id: bool = True) -> int:
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

                    inserted_id = 0
                    # 获取ID逻辑
                    if return_id:
                        await cur.execute("SELECT LAST_INSERT_ID();")
                        result = await cur.fetchone()
                        inserted_id = result[0] if result else 0
                    else:
                        inserted_id = data.get('id', 0)  # 假设自定义ID字段为id

            # 打印日志（使用提供的ID或自增ID）
            provided_id = data.get('id', inserted_id)
            if inserted_id > 0:
                logger.info(f"Insert success 【{table}】-【{provided_id}】")

            return inserted_id

        except Exception as e:
            logger.error(f"插入失败: {str(e)}", exc_info=True)
            return 0