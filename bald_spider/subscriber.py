from collections import defaultdict
from typing import Dict, Set, Callable, Coroutine, Any
import asyncio


class Subscriber:
    def __init__(self):
        self._subscriber: Dict[str, Set[Callable[..., Coroutine[Any, Any, None]]]] = defaultdict(set)

    def subscribe(self, receiver: Callable[..., Coroutine[Any, Any, None]], *, event: str) -> None:
        self._subscriber[event].add(receiver)

    def unsubscribe(self, receiver: Callable[..., Coroutine[Any, Any, None]], *, event: str) -> None:
        self._subscriber[event].discard(receiver)

    async def notify(self, event: str, *args: Any, **kwargs: Any) -> None:
        for receiver in self._subscriber[event]:
            # asyncio.create_task(receiver(*args, **kwargs)) # 不需要await 因为是支线任务，没必要等它
            asyncio.create_task(receiver(*args, **kwargs))  # type: ignore
