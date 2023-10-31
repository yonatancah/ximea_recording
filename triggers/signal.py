from typing import Callable, Set


class Signal:
    def __init__(self) -> None:
        self._observers: Set[Callable] = set()
        
    def connect(self, fun) -> None:
        self._observers.add(fun)

    def send(self, *args, **kwargs) -> None:
        for fun in self._observers:
            fun(*args, **kwargs)
