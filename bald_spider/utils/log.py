# from logging import Formatter, StreamHandler, INFO, Logger
#
# LOG_FORMAT = F"%(asctime)s [%(name)s] %(levelname)s: %(message)s"
#
#
# class LogManager:
#     logger = {}
#
#     @classmethod
#     def get_logger(cls, name: str = "default", log_level=None, log_format=LOG_FORMAT):
#         # 在这个地方其实是使用name和level唯一化一个logger，当存在直接从字典中返回
#         # 若不存在在创建一个新的logger返回
#         key = (name, log_level)
#
#         def gen_logger():
#             log_formatter = Formatter(log_format)
#             handler = StreamHandler()
#             handler.setFormatter(log_formatter)
#             handler.setLevel(log_level or INFO)
#             _logger = Logger(name)
#             _logger.addHandler(handler)
#             _logger.setLevel(log_level or INFO)
#             cls.logger[key] = _logger
#             return _logger
#
#         return cls.logger.get(key, None) or gen_logger()
#
#
# get_logger = LogManager.get_logger
#
# if __name__ == "__main__":
#     LogManager.get_logger(name="xxx", log_level=INFO)


from loguru import logger
from typing import Dict, Tuple, Optional, Any



class LogManager:
    _loggers: Dict[Tuple[str, Optional[int]], Any] = {}

    @classmethod
    def get_logger(cls, name: str = "default", log_level=None, log_format=None) -> logger:
        """
        获取logger实例
        :param name: logger名称
        :param log_level: 日志级别
        :param log_format: 日志格式
        :return: logger实例
        """
        key = (name, log_level)

        def gen_logger():
            # 创建新的logger实例
            _logger = logger.bind(name=name)

            # # 移除默认的处理器
            # _logger.remove()
            #
            # # 添加新的处理器
            # _logger.add(
            #     "sys.stdout",
            #     format=log_format or "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{extra[name]}</cyan>: <level>{message}</level>",
            #     level=log_level or INFO,
            #     colorize=True
            # )

            cls._loggers[key] = _logger
            return _logger

        return cls._loggers.get(key) or gen_logger()


# 为了保持与原代码相同的使用方式
get_logger = LogManager.get_logger

if __name__ == "__main__":
    # 使用示例
    logger = LogManager.get_logger(name="xxx", log_level=INFO)
    logger.info("这是一条测试日志")
    logger.error("这是一条错误日志")