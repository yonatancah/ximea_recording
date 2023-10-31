from __future__ import annotations
from abc import ABC, abstractmethod
from typing import NamedTuple


class TimestampData(NamedTuple):
    timestamp: int
    corrected_timestamp: int


class BaseTimestampWriter(ABC):

    @classmethod
    @abstractmethod
    def open(cls, fname: str) -> BaseTimestampWriter:
        ...

    @abstractmethod
    def write(self, timestamp: TimestampData) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...
    
