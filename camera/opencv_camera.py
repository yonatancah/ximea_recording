from __future__ import annotations
import time

import cv2
import numpy as np

from .base_camera import BaseCamera, CameraSettings
from .frame import Frame

class OpenCVCamera(BaseCamera):

    def __init__(self, cap: cv2.VideoCapture) -> None:
        self._cap = cap
    
    @classmethod
    def open(cls, id: str) -> OpenCVCamera:
        return OpenCVCamera(
            cap=cv2.VideoCapture(0),
        )

    def set_settings(self, settings: CameraSettings) -> None:
        pass
    
    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass
        
    def close(self) -> None:
        self._cap.release()
        
    def get_timestamp_micro(self) -> int:
        return int(time.monotonic_ns() // 1000)

    def get_frame(self) -> Frame:
        ret, img = self._cap.read()
        return Frame(
            timestamp=self.get_timestamp_micro(),
            image=img,
        )
    
