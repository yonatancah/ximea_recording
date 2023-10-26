from argparse import ArgumentParser
import importlib

import cv2

from camera import CameraSettings

parser = ArgumentParser(description="View a Camera")
parser.add_argument('--cam-type', '-c', choices=['ximea', 'opencv', 'dummy'], default='ximea')
args = parser.parse_args()

cam_types = {
    'ximea': lambda: importlib.import_module('camera.ximea_camera').XimeaCamera,
    'dummy': lambda: importlib.import_module('camera.dummy_camera').DummyCamera,
    'opencv': lambda: importlib.import_module('camera.opencv_camera').OpenCVCamera,
}

CamType = cam_types[args.cam_type]()

settings = CameraSettings(
    exposure_usec=40000, 
    frame_rate=40, 
    white_balance_auto="auto", 
    image_format="RGB",
    bit_depth=24,
)


cam = CamType.open(id="CAM2")

cam.set_settings(settings=settings)
cam.start()

print(cam.get_timestamp_micro())


while True:
    frame=cam.get_frame()
    print(frame.image.shape)

    cv2.putText(
        frame.image, str(frame.timestamp), (900, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 2
    )
    cv2.imshow("Camera", frame.image)

    # Handle user inputs
    if cv2.waitKey(1) == ord('q'):
        print("Quit signal received.")
        break


cam.stop()
cam.close()


