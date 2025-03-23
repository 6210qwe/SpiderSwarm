from inspect import isgenerator, isasyncgen


from bald_spider.exceptions import TransformTypeError


async def transform(func_result):
    try:
        # 这个地方就是对异步生成器和同步生成器进行兼容，都转化成异步生成器
        if isgenerator(func_result):
            for r in func_result:
                yield r
        elif isasyncgen(func_result):
            async for r in func_result:
                yield r
        else:
            raise TransformTypeError("callback return value must be generator or asyncgen")
    except Exception as exc:
        yield exc  # 把异常返回出去，在engine中就可以拿到了




