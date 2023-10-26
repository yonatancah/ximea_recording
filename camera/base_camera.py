from __future__ import annotations
from abc import ABC, abstractmethod
import time

from typing import Iterable, Literal, NamedTuple

from numpy.typing import NDArray


class CameraSettings(NamedTuple):
    exposure_usec: int
    frame_rate: int
    white_balance_auto: bool
    image_format: Literal['RGB', 'MONO', 'RAW']
    bit_depth: int


class BaseCamera(ABC):

    @classmethod
    @abstractmethod
    def open(cls, id: str) -> BaseCamera:
        ...

    @staticmethod
    def get_multi_camera_timestamp_corrections(cams: Iterable[BaseCamera]) -> list[int]:
        baseline_corrections: list[int] = []
        t0 = time.perf_counter_ns()
        for cam in cams:
            timestamp = cam.get_timestamp_micro()
            t1 = time.perf_counter_ns()
            dt = t1 - t0
            correction = -(timestamp - dt)
            baseline_corrections.append(correction)
            
    @abstractmethod
    def set_settings(self, settings: CameraSettings) -> None:
        ...
    
    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...
        
    @abstractmethod
    def close(self) -> None:
        ...
        
    @abstractmethod
    def get_timestamp_micro(self) -> int:
        ...

    @abstractmethod
    def get_frame(self) -> Frame:
        return Frame(
            timestamp=...,
            corrected_timestamp=...,
        )




class Frame(NamedTuple):
    timestamp: int
    image: NDArray
