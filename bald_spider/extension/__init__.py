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
        for extension in extensions:
            extension_cls = load_class(extension)
            if not hasattr(extension_cls, "create_instance"):
                raise ExtensionInitError(f"{extension_cls.__name__} does not have create_instance method")
            self.extensions.append(extension_cls.create_instance(self.crawler))
        if extensions:
            self.logger.info(f"Loaded extensions:\n{pformat(self.extensions)}")

    async def _process_spider_closed(self, spider):
        pass
