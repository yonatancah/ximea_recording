from __future__ import annotations

from abc import ABC, abstractmethod


class BaseTimestampWriter(ABC):

    @classmethod
    @abstractmethod
    def open(cls, fname: str) -> BaseTimestampWriter:
        ...

    @abstractmethod
    def write(self, timestamp: int, corrected_timestamp: int = 0) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...
    
