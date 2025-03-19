
class TestPipeline:

    def process_item(self, item, spider):
        # 代码写到这里基本的逻辑已经通了，可以写具体的pipeline了
        print(f"我是pipeline, 我正在处理item: {item}")
        # 接收两个参数，需要处理的数据，和从那个spider过来的
        pass
        # print(item)
        # return item

    @classmethod
    def create_instance(cls, crawler):
        return cls()