from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal

from numpy.typing import NDArray


class BaseVideoWriter(ABC):

    @abstractmethod
    @classmethod
    def open(cls, fname: str, frame_rate: int, frame_width: int, frame_height: int, fourcc: Literal["FMP4"] = "FMP4") -> VideoWriter:
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


