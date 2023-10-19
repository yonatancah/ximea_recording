import time
from multiprocessing import Process

import cv2

from camdata import CamData

### Utils
def run_camera(cam_id):
    cam = CamData.from_userid(user_id=cam_id)
    cam.start()

    while True:
        # Get a frame
        start_time = time.perf_counter()
        cam.update_frame()
        cam.write_frame()
        end_time = time.perf_counter()
        print(f'{cam.cam_id} FPS: {round(1/(end_time - start_time), 1)}')

        # Show it.
        cam.show()

        # Handle user inputs
        if cv2.waitKey(1) == ord('q'):
            print("Quit signal received.")
            break

    cam.stop()



if __name__ == '__main__':
    # Connect to a camera, set it up
    cam_ids = ['CAM1', 'CAM2', 'CAM3', 'CAM4', 'CAM5', 'CAM6', 'CAM7', 'CAM8', 'CAM9']

    procs = []
    for cam_id in cam_ids:
        proc = Process(target=run_camera, args=(cam_id,))
        proc.start()
        procs.append(proc)
    
    for proc in procs:
        proc.join()
