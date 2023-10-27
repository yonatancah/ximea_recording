from __future__ import annotations

from config import ConfigData
from camera import CameraGroup
from camera.ximea_camera import XimeaCamera
from camera_worker import CameraWorker
from triggers import wait_trigger


if __name__ == '__main__':
    config = ConfigData.from_yaml(fname='config.yaml')
    print(config)

    # Connect to Cams, collect baseline timestamps for timestamp alignment
    cams = CameraGroup.init(cam_type=XimeaCamera, ids=config.cam_ids, settings=config.cam_settings, start=True, verbose=True)
    timestamp_corrections = cams.get_multi_camera_timestamp_corrections()
    cams.stop_and_close()
    
    # Start Cameras
    workers: list[CameraWorker] = []
    for cam_id, timestamp_correction in zip(config.cam_ids, timestamp_corrections):
        worker = CameraWorker.init(
            cam_type=XimeaCamera,
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
            print("Main Process: received start trigger", flush=True)
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
