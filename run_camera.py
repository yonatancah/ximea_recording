from camera import CameraSettings
from camera.ximea_camera import XimeaCamera
import cv2

settings = CameraSettings(
    exposure_usec=40000, 
    frame_rate=40, 
    white_balance_auto="auto", 
    image_format="RGB",
    bit_depth=24,
)

cam = XimeaCamera.open(id="CAM2")

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


