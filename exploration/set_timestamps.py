import sys
import time
import cv2
from camdata import CamData


    

cams = [
    CamData.from_userid("CAM1"),
    CamData.from_userid("CAM2"),
    CamData.from_userid("CAM3"),
    CamData.from_userid("CAM4")
]
for cam in cams:
    cam.start()


for _ in range(10):
    # time.sleep(.000001)
    start = time.perf_counter()
    # print(*[cam.get_timestamp() // 1000 for cam in cams])
    # for cam in cams:
    #     cam.update_frame()
    # print(*[cam.current_timestamp_milli for cam in cams])
    stop = time.perf_counter()
    print(stop - start, 1 / (stop - start))

for cam in cams:
    cam.stop()