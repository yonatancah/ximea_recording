from __future__ import annotations
from abc import ABC, abstractmethod

from .camera_settings import CameraSettings
from .frame import Frame


class BaseCamera(ABC):

    @classmethod
    @abstractmethod
    def open(cls, id: str) -> BaseCamera:
        ...

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




