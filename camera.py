from __future__ import annotations
import time

from typing import Iterable, NamedTuple


class CameraSettings(NamedTuple):
    exposure: int
    frame_rate: int
    white_balance: str


class Camera:

    @classmethod
    def open(cls, id: str) -> Camera:
        ...

    @staticmethod
    def get_multi_camera_timestamp_corrections(cams: Iterable[Camera]) -> list[int]:
        baseline_corrections: list[int] = []
        t0 = time.perf_counter_ns()
        for cam in cams:
            timestamp = cam.get_timestamp_micro()
            t1 = time.perf_counter_ns()
            dt = t1 - t0
            correction = -(timestamp - dt)
            baseline_corrections.append(correction)
            
    def set_settings(self, settings: CameraSettings) -> None:
        ...

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...

    def close(self) -> None:
        ...

    def get_timestamp_nano(self) -> int:
        ...

    def set_timestamp_correction(self, dt_nano: int) -> None:
        ...

    def get_corrected_timestamp(self) -> int:
        ...

    def get_frame(self) -> Frame:
        return Frame(
            timestamp=...,
            corrected_timestamp=...,
        )




class Frame(NamedTuple):
    timestamp: int
    corrected_timestamp: int
