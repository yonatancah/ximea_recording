import time
from camdata import set_baseline_timestamps, CamData



cams = [
    CamData.from_userid("CAM1"),
    CamData.from_userid("CAM2"),
    CamData.from_userid("CAM3"),
    CamData.from_userid("CAM4")
]
for cam in cams:
    cam.start()

set_baseline_timestamps(*cams)

t0 = time.perf_counter()
for _ in range(100):
    for cam in cams:
        cam.update_frame()
    
    print(time.perf_counter() - t0)
    print(*[cam.current_timestamp_micro for cam in cams])
    print(*[cam.baseline_timestamp for cam in cams])
    print(*[cam.current_timestamp_corrected_micro for cam in cams])
    print('')