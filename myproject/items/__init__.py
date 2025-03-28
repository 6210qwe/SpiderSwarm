from bald_spider import Item, Field

class ExampleItem(Item):
    title = Field()
    link = Field()
    content = Field()
    created_at = Field()
