from __future__ import annotations
import time

import numpy as np
from .base_camera import BaseCamera, CameraSettings
from .frame import Frame

class DummyCamera(BaseCamera):
    
    @classmethod
    def open(cls, id: str) -> BaseCamera:
        return DummyCamera()

    def set_settings(self, settings: CameraSettings) -> None:
        pass
    
    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass
        
    def close(self) -> None:
        pass
        
    def get_timestamp_micro(self) -> int:
        return int(time.monotonic_ns() // 1000)

    def get_frame(self) -> Frame:
        return Frame(
            timestamp=self.get_timestamp_micro(),
            image=np.random.randint(0, 255, size=(400, 600, 3), dtype=np.uint8)
        )
    
