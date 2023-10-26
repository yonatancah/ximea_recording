from __future__ import annotations

from config import ConfigData
from camera import get_multi_camera_timestamp_corrections
from camera.ximea_camera import XimeaCamera
# from camera_worker import CameraWorker
from triggers import wait_trigger


config = ConfigData.from_yaml(fname='config.yaml')
print(config)

# Baseline Timestamp
cams: list[XimeaCamera] = []
for cam_id in config.cam_ids:
    cam = XimeaCamera.open(id=cam_id)
    cam.set_settings(settings=config.cam_settings)
    cam.start()
    print(f"started {cam_id}.", flush=True)
    cams.append(cam)

timestamp_corrections = get_multi_camera_timestamp_corrections(cams=cams)
print(timestamp_corrections)


# for cam in cams:
#    cam.stop()
#    cam.close()


# # Start Cameras
# workers: list[CameraWorker] = []
# for cam_id, timestamp_correction in zip(config.cam_ids, timestamp_corrections):
#     worker = CameraWorker.init(
#         cam_id=cam_id, 
#         cam_settings=config.cam_settings, 
#         timestamp_correction=timestamp_correction
#     )
#     worker.start()
#     workers.append(worker)


# # Wait for trigger
# while True:
#     try:
#         start_trigger = wait_trigger(name='start')
#         for worker in workers:
#             worker.send_start_event(destination=start_trigger.destination)
#         stop_trigger = wait_trigger(name='stop')
#         for worker in workers:
#             worker.send_stop_event()
#     except KeyboardInterrupt:
#         for worker in workers:
#             worker.send_close_event()
#         break

# for worker in workers:
#     worker.join()
