from typing import List
from pprint import pformat
from bald_spider.exceptions import ExtensionInitError
from bald_spider.utils.log import get_logger
from bald_spider.utils.project import load_class


class ExtensionManager:
    def __init__(self, crawler):
        self.crawler = crawler
        self.extensions: List = []
        extensions = self.crawler.settings.get("EXTENSIONS")
        self.logger = get_logger(self.__class__.__name__, crawler.settings.get("LOG_LEVEL"))
        self._add_extensions(extensions)
        self._stats = crawler.stats

    @classmethod
    def create_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def _add_extensions(self, extensions):
        extension_names = []
        for extension in extensions:
            extension_cls = load_class(extension)
            if not hasattr(extension_cls, "create_instance"):
                raise ExtensionInitError(f"{extension_cls.__name__} does not have create_instance method")
            self.extensions.append(extension_cls.create_instance(self.crawler))
            # 收集扩展类的完整名称
            extension_names.append(f"{extension_cls.__module__}.{extension_cls.__name__}")
        if extensions:
            self.logger.debug(f"Loaded extensions:\n{pformat(extension_names)}")

    async def _process_spider_closed(self, spider):
        pass
