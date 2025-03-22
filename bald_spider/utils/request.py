import hashlib
import json

from w3lib.url import canonicalize_url
from bald_spider import Request
from typing import Optional, Iterator, Union, Iterable, Tuple

# 指纹生成器

def to_bytes(text, encoding="utf-8"):
    if isinstance(text, bytes):
        return text
    if isinstance(text, str):
        return text.encode(encoding)
    if isinstance(text, dict):
        return json.dumps(text, sort_keys=True).encode(encoding)


def request_fingerprint(request: Request,
                        include_headers: Optional[Iterable[Union[bytes, str]]] = None
                        ) -> str:
    headers: Optional[Tuple[str, ...]] = None
    if include_headers is not None:
        headers = tuple(header.lower() for header in sorted(include_headers))
    fp = hashlib.md5()
    fp.update(to_bytes(request.method))
    fp.update(to_bytes(canonicalize_url(request.url)))
    fp.update(to_bytes(request.body or b""))
    if headers:
        for h in headers:
            if h in request.headers:
                fp.update(to_bytes(h))
                fp.update(to_bytes(request.headers.get(h)))
    fingerprint = fp.hexdigest()
    return fingerprint

















