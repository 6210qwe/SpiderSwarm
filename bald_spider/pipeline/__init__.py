from bald_spider.items.items import Item


class BasePipeline:
    def process_item(self, item: Item, spider) -> None:
        raise NotImplementedError

    @classmethod
    def from_crawler(cls, crawler):
        return cls()
