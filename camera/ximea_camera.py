from ximea import xiapi

from .camera_settings import CameraSettings
from .frame import Frame
from .base_camera import BaseCamera


class XimeaCamera(BaseCamera):

    def __init__(self, cam: xiapi.Camera) -> None:
        self.cam = cam

    @classmethod
    def open(cls, id: str) -> BaseCamera:
        cam = xiapi.Camera()
        cam.open_device_by("XI_OPEN_BY_USER_ID", id)
        
        self = XimeaCamera(cam=cam)
        return self
    
    def set_settings(self, settings: CameraSettings) -> None:
        self.cam.set_exposure(settings.exposure_usec)
        self.cam.set_framerate(settings.frame_rate)
        if settings.white_balance_auto:
            self.cam.enable_auto_wb()
        bit_settings = {
            ('RGB', 24): "XI_RGB24",
            ('RGB', 32): "XI_RGB32",
            ('RGB', 48): "XI_RGB48",
            ('RGB', 64): "XI_RGB64",
            ('RAW', 8): "XI_RAW8",
            ('RAW', 16): "XI_RAW16",
            ('RAW', 32): "XI_RAW32",
            ('MONO', 8): "XI_MONO8",
            ('MONO', 16): "XI_MONO16",

        }
        data_format = bit_settings[settings.image_format, settings.bit_depth]
        self.cam.set_imgdataformat(data_format)

    def start(self) -> None:
        self.cam.start_acquisition()
    
    def stop(self) -> None:
        self.cam.stop_acquisition()

    def close(self) -> None:
        self.cam.close_device()
    
    def get_timestamp_micro(self) -> int:
        timestamp=self.cam.get_timestamp()
        return timestamp
    
    def get_frame(self) -> Frame:
        img = xiapi.Image()
        self.cam.get_image(image=img)
        microseconds = img.tsSec * 1_000_000 + img.tsUSec
        frame = Frame(
            timestamp=microseconds,
            image=img.get_image_data_numpy()
        )
        return frame
