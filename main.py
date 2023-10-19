from __future__ import annotations

from config import load_config
from camera import Camera
from camera_worker import CameraWorker
from triggers import wait_trigger


config = load_config(fname='config.yaml')

# Baseline Timestamp
cams: list[Camera] = []
for cam_id in config.cam_ids:
    cam = Camera.open(id=cam_id)
    cam.set_settings(settings=config.cam_settings)
    cam.start()
    cams.append(cam)

timestamp_corrections = Camera.get_multi_camera_timestamp_corrections(cams=cams)

for cam in cams:
   cam.stop()
   cam.close()


# Start Cameras
workers: list[CameraWorker] = []
for cam_id, timestamp_correction in zip(config.cam_ids, timestamp_corrections):
    worker = CameraWorker.init(
        cam_id=cam_id, 
        cam_settings=config.cam_settings, 
        timestamp_correction=timestamp_correction
    )
    worker.start()
    workers.append(worker)


# Wait for trigger
while True:
    try:
        start_trigger = wait_trigger(name='start')
        for worker in workers:
            worker.send_start_event(destination=start_trigger.destination)
        stop_trigger = wait_trigger(name='stop')
        for worker in workers:
            worker.send_stop_event()
    except KeyboardInterrupt:
        for worker in workers:
            worker.send_close_event()
        break

for worker in workers:
    worker.join()
