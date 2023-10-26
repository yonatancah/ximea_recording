from __future__ import annotations

from .base_camera import BaseCamera, CameraSettings, Frame


class DummyCamera(BaseCamera):

    @classmethod
    def open(cls, id: str) -> DummyCamera:
        ...

    def close(self) -> None:
        return super().close()
    
    def set_settings(self, settings: CameraSettings) -> None:
        return super().set_settings(settings)
    

    def start(self) -> None:
        return super().start()
    
    def stop(self) -> None:
        return super().stop()
    
    
    def get_frame(self) -> Frame:
        return super().get_frame()
    
    def get_timestamp_micro(self) -> int:
        return super().get_timestamp_micro()
    
    
    
    
    
    
    

   
