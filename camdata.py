from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Optional
import cv2
import numpy as np
from ximea import xiapi, xidefs


def get_baseline_timestamps_for_cameras(*cams: xiapi.Camera) -> list[int]:
    t0 = time.perf_counter_ns() 
    timestamps = []
    for cam in cams:
        timestamp = cam.get_timestamp()
        t1 = time.perf_counter_ns()
        dt = t1 - t0
        timestamps.append(int((timestamp - dt) // 1000))
        # timestamps.append(int(timestamp // 1000))
    
    return timestamps


def set_baseline_timestamps(*cam_datas: CamData) -> None:
    baseline_timestamps = get_baseline_timestamps_for_cameras(*[cam.cam for cam in cam_datas])
    for cam_data, baseline_timestamp in zip(cam_datas, baseline_timestamps):
        cam_data.baseline_timestamp = baseline_timestamp



@dataclass
class CamData:
    cam_id: str
    cam: xiapi.Camera
    img: xiapi.Image
    writer: cv2.VideoWriter
    current_frame: Optional[np.ndarray] = None
    current_timestamp_micro: int = 0
    baseline_timestamp: int = 0


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
            f'cal4_{user_id}.avi', 
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
        
    def get_timestamp(self):
        return self.cam.get_timestamp()

    def update_frame(self):
        self.cam.get_image(image=self.img)
        self.current_frame: np.ndarray = self.img.get_image_data_numpy()
        self.current_timestamp_micro = (self.img.tsSec * 1_000_000 + self.img.tsUSec)# - self.baseline_timestamp
        # time.sleep(.000001)
        # print(self.current_frame.shape)
        
    @property
    def current_timestamp_corrected_micro(self) -> int:
        return self.current_timestamp_micro - self.baseline_timestamp

    def write_frame(self):
        self.writer.write(self.current_frame)
        self.writer.set(cv2.CAP_PROP_POS_MSEC, 1000)
    
    def show(self):
        cv2.imshow(self.cam_id, self.current_frame)

