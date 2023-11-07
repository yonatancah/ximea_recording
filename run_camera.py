"""
Webcam: 
    python run_camera.py 0 -c opencv
Ximea Camera: 
    python run_camera.py CAM1 -c ximea
Simulated Noise (for debugging, no camera hardware needed): 
    python run_camera.py 0 -c dummy
"""

from argparse import ArgumentParser
import importlib
from textwrap import dedent
from typing import Type

import cv2

from camera import CameraSettings
from camera.base_camera import BaseCamera
from video_writers.opencv import OpenCVVideoWriter
from timestamp_writers.csv import CSVTimestampWriter

parser = ArgumentParser(description="View a Live Camera Feed")
parser.add_argument('id', help="Camera ID")
parser.add_argument('--cam-type', '-c', choices=['ximea', 'opencv', 'dummy'], default='ximea', help="The Camera Backend to Use")
args = parser.parse_args()

cam_types = {
    'ximea': lambda: importlib.import_module('camera.ximea_camera').XimeaCamera,
    'dummy': lambda: importlib.import_module('camera.dummy_camera').DummyCamera,
    'opencv': lambda: importlib.import_module('camera.opencv_camera').OpenCVCamera,
}

CamType: Type[BaseCamera] = cam_types[args.cam_type]()

settings = CameraSettings(
    exposure_usec=8000,
    gain_analog=17,
    frame_rate=60, 
    white_balance_auto="auto", 
    image_format="RGB",
    bit_depth=24,
)

cam = CamType.init(id=args.id, settings=settings, start=False, verbose=True)
cam.start()

video_writer =OpenCVVideoWriter.open(
    fname=str('testvideo60fps.avi'), 
    frame_rate=settings.frame_rate, 
    fourcc='XVID',
    autoflush=False,    
)
timestamp_writer = CSVTimestampWriter.open(str('testtimestamp60fps.txt'))
print(cam.get_timestamp_micro())

while True:
    frame=cam.get_frame()
    cv2.putText(frame.image, str(frame.timestamp), (900, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 2)
    cv2.imshow("Camera", frame.image)
    video_writer.write(frame=frame.image)
    timestamp_writer.write(timestamp=frame.timestamp)

    # Handle user inputs
    if cv2.waitKey(1) == ord('q'):
        print("Quit signal received.")
        break

timestamp_writer.close()
video_writer.close()
cam.stop()
cam.close()


