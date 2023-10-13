from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Optional
import cv2
import numpy as np
from ximea import xiapi, xidefs


@dataclass
class CamData:
    cam_id: str
    cam: xiapi.Camera
    img: xiapi.Image
    writer: cv2.VideoWriter
    current_frame: Optional[np.ndarray] = None

    @classmethod
    def from_userid(cls, user_id) -> CamData:
        cam = xiapi.Camera()

        cam.open_device_by("XI_OPEN_BY_USER_ID", user_id)
        cam.set_imgdataformat('XI_RGB24')
        # mode = xidefs.XI_ACQ_TIMING_MODE['XI_ACQ_TIMING_MODE_FRAME_RATE_LIMIT']
        # cam.set_acq_timing_mode(mode)
        # cam.set_param("XI_ACQ_TIMING_MODE", "XI_ACQ_TIMING_MODE_FRAME_RATE_LIMIT")
        # cam.set_param("XI_ACQ_TIMING_MODE", mode)
        cam.set_framerate(60)
        # cam.set_param("XI_ACQ_TIMING_MODE", "XI_ACQ_TIMING_MODE_FRAME_RATE_LIMIT")

        cam.set_exposure_direct(7000)
        cam.set_gain_selector('XI_GAIN_SELECTOR_ANALOG_ALL')
        cam.set_gain_direct(17)
        cam.enable_auto_wb()

        img = xiapi.Image()


        
        writer = cv2.VideoWriter(
            f'calibration2_{user_id}.avi', 
            cv2.VideoWriter_fourcc(*'XVID'), 
            30, 
            (cam.get_width(), cam.get_height()),
        ) 

        return CamData(cam_id=user_id, cam=cam, img=img, writer=writer)

    def start(self):
        self.cam.start_acquisition()

    def stop(self):
        self.writer.release()
        self.cam.stop_acquisition()
        self.cam.close_device()
        

    def update_frame(self):
        self.cam.get_image(image=self.img)
        self.current_frame: np.ndarray = self.img.get_image_data_numpy()
        # time.sleep(.000001)
        # print(self.current_frame.shape)
        
    def write_frame(self):
        self.writer.write(self.current_frame)
    
    def show(self):
        cv2.imshow(self.cam_id, self.current_frame)

