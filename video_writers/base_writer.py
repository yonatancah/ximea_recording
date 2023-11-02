from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal

from numpy.typing import NDArray


class BaseVideoWriter(ABC):

    @classmethod
    @abstractmethod
    def open(cls, fname: str, frame_rate: int, fourcc: Literal["FMP4"] = "FMP4") -> BaseVideoWriter:
        ...

    @abstractmethod
    def write(self, frame: NDArray) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    def __enter__(self) -> BaseVideoWriter:
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


