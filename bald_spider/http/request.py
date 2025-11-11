from typing import Dict, Optional, Callable
from urllib.parse import urlencode

class Request:
    def __init__(
            self, url: str, *,
            headers: Optional[Dict] = None,
            callback: Callable = None,
            priority: int = 0,
            method: str = "GET",
            cookies: Optional[Dict] = None,
            params: Optional[Dict] = None,
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
        self.params = params
        if self.params:
            filtered_params = {k: v for k, v in self.params.items() if v is not None}
            query_string = urlencode(filtered_params)
            self.url = f"{self.url}?{query_string}"

    @property
    def full_url(self):
        if self.params:
            filtered_params = {k: v for k, v in self.params.items() if v is not None}
            query_string = urlencode(filtered_params)
            return f"{self.url}?{query_string}"
        print(self.url)
        return self.url

    def __lt__(self, other):
        return self.priority < other.priority

    def __str__(self):
        return f"{self.url} {self.method}"

    @property
    def meta(self):
        return self._meta
