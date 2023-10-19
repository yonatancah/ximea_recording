from __future__ import annotations

from camera import Frame


class VideoWriter:

    @classmethod
    def open(self, fname: str) -> VideoWriter:
        ...

    def write(self, frame: Frame) -> None:
        ...

    def close(self) -> None:
        ...


class TimestampWriter:

    @classmethod
    def open(self, fname: str) -> TimestampWriter:
        ...

    def write(self, timestamp: int) -> None:
        ...

    def close(self) -> None:
        ...

