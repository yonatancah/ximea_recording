from __future__ import annotations
from camera.dummy_camera import DummyCamera

from config import ConfigData
from camera import CameraGroup
from camera.ximea_camera import XimeaCamera
from camera_worker import CameraWorker
from triggers.pylsl_trigger_detector import PyLSLTriggerDetector


if __name__ == '__main__':
    config = ConfigData.from_yaml(fname='config.yaml')
    print(config)

    # Connect to Cams, collect baseline timestamps for timestamp alignment
    # cams = CameraGroup.init(cam_type=XimeaCamera, ids=config.cam_ids, settings=config.cam_settings, start=True, verbose=True)
    cams = CameraGroup.init(cam_type=DummyCamera, ids=config.cam_ids, settings=config.cam_settings, start=True, verbose=True)
    timestamp_corrections = cams.get_timestamp_corrections()
    cams.stop_and_close()
    
    # Start Cameras
    workers: list[CameraWorker] = []
    for cam_id, timestamp_correction in zip(config.cam_ids, timestamp_corrections):
        worker = CameraWorker.init(
            cam_type=DummyCamera,
            cam_id=cam_id, 
            cam_settings=config.cam_settings, 
            timestamp_correction=timestamp_correction
        )
        worker.start()
        workers.append(worker)


    # Wait for trigger
    trigger_detector = PyLSLTriggerDetector()

    def send_start_event(workers, destination):
        for worker in workers:
            print("sending start event to worker, ", destination)
            worker.send_start_event(destination=destination)
    trigger_detector.start_trigger_detected.connect(lambda data: send_start_event(workers=workers, destination=data['destination']))

    def send_stop_event(workers):
        for worker in workers:
            print("sending stop event to worker.")
            worker.send_stop_event()

    trigger_detector.stop_trigger_detected.connect(lambda data: send_stop_event(workers=workers))



    while True:
        trigger_detector.wait_for_triggers(start='start', stop='stop', close=None)


#     for worker in workers:
#         worker.join()
