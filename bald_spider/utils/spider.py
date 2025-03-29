from inspect import isgenerator, isasyncgen
from typing import Union, Generator, AsyncGenerator

from bald_spider import Response, Request, Item
from bald_spider.exceptions import TransformTypeError

T = Union[Request, Item]
SpiderOutputType = Union[Generator, AsyncGenerator]


# Generator有三种情况
# yield type
# send type
# return type

async def transform(func_result, response: Response):
    # func_result都是从response中产生的, response中的depth是从上一个层级来的
    def set_request(t: T) -> T:
        if isinstance(t, Request):
            t.meta["depth"] = response.meta['depth']
        return t

    try:
        # 这个地方就是对异步生成器和同步生成器进行兼容，都转化成异步生成器
        if isgenerator(func_result):
            for r in func_result:
                yield set_request(r)
        elif isasyncgen(func_result):
            async for r in func_result:
                yield set_request(r)
        else:
            raise TransformTypeError("callback return value must be generator or asyncgen")
    except Exception as exc:
        yield exc  # 把异常返回出去，在engine中就可以拿到了
