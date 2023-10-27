from __future__ import annotations

import time
from typing import Iterable, Sequence, Type

from .camera_settings import CameraSettings
from .base_camera import BaseCamera




class CameraGroup:

    def __init__(self, cameras: Sequence[BaseCamera]) -> None:
        self.cameras = cameras

    @classmethod
    def init(cls, cam_type: Type[BaseCamera], ids: Iterable[str], settings: CameraSettings = None, start: bool = False, verbose: bool = False) -> CameraGroup:
        cams = []
        for id in ids:
            cam = cam_type.init(id=id, settings=settings, start=start, verbose=verbose)
            cams.append(cam)
        return CameraGroup(cameras=cams)



    def start(self) -> None:
        for cam in self.cameras:
            cam.start()

    def stop(self) -> None:
        for cam in self.cameras:
            cam.stop()

    def close(self) -> None:
        for cam in self.cameras:
            cam.close()

    def stop_and_close(self) -> None:
        for cam in self.cameras:
            cam.stop()
            cam.close()
    
    def get_multi_camera_timestamp_corrections(self) -> list[int]:
        baseline_corrections: list[int] = []
        t0 = time.perf_counter_ns()
        for cam in self.cameras:
            timestamp = cam.get_timestamp_micro()
            t1 = time.perf_counter_ns()
            dt = t1 - t0
            correction = -(timestamp - dt)
            baseline_corrections.append(correction)
        return baseline_corrections