from __future__ import annotations
import time

from typing import Iterable

from .base_camera import BaseCamera


def get_multi_camera_timestamp_corrections(cams: Iterable[BaseCamera]) -> list[int]:
    baseline_corrections: list[int] = []
    t0 = time.perf_counter_ns()
    for cam in cams:
        timestamp = cam.get_timestamp_micro()
        t1 = time.perf_counter_ns()
        dt = t1 - t0
        correction = -(timestamp - dt)
        baseline_corrections.append(correction)
    return baseline_corrections