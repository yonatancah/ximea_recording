from __future__ import annotations
from abc import ABC, abstractmethod

from .camera_settings import CameraSettings
from .frame import Frame


class BaseCamera(ABC):

    @classmethod
    @abstractmethod
    def open(cls, id: str) -> BaseCamera:
        ...

    @classmethod
    def init(cls, id: str, settings: CameraSettings = None, start: bool = False, verbose: bool = False) -> BaseCamera:
        """
        A convenient constructor for connecting to, setting up, and starting a Camera.
        """
        if verbose:
            print(f"Connecting to camera {id}...", flush=True)
        cam = cls.open(id=id)
        if settings:
            cam.set_settings(settings=settings)
        if start:
            cam.start()
        if verbose:
            print(f"...done", flush=True)
        return cam

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
        ...




