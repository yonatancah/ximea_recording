import time

import cv2

from camdata import CamData

# Connect to a camera, set it up
cam_ids = ['CAM1']#, 'CAM2', 'CAM4', 'CAM7']
cams = [CamData.from_userid(user_id=cam_id) for cam_id in cam_ids]  

for cam in cams:
    cam.start()

while True:
    
    # Get a frame
    start_time = time.perf_counter()
    for cam in cams:
        cam.update_frame()
        cam.write_frame()
    end_time = time.perf_counter()
    print(f'FPS: {round(1/(end_time - start_time), 1)}\tFrame: {cam.img.nframe}\tRate: {cam.cam.get_framerate()}\tMode: {cam.cam.get_acq_timing_mode()}')

    # Show it.
    for cam in cams:
        cam.show()

    # Handle user inputs
    if cv2.waitKey(1) == ord('q'):
        print("Quit signal received.")
        break

    
# Disconnect
for cam in cams:
    cam.stop()