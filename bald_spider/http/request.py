from typing import Dict, Optional, Callable


class Request:
    def __init__(
            self, url: str, *,
            headers: Optional[Dict] = None,
            callback: Callable = None,
            priority: int = 0,
            method: str = "GET",
            cookies: Optional[Dict] = None,
            proxy: Optional[Dict] = None,
            body: Optional[Dict] = None,
            encoding="utf-8",
            # 和请求无关，但是和运行流程有关
            meta: Optional[Dict] = None,
            dont_filter= None
    ):
        self.url = url
        self.headers = headers if headers else {}
        self.callback = callback
        self.priority = -priority  #设置优先级队列，实现越大越优先
        self.method = method
        self.cookies = cookies
        self.proxy = proxy
        self.body = body
        self.encoding = encoding
        self._meta = meta if meta is not None else {}
        self.dont_filter = dont_filter

    def __lt__(self, other):
        return self.priority < other.priority

    def __str__(self):
        return f"{self.url} {self.method}"

    @property
    def meta(self):
        return self._meta
