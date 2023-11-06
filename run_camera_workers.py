from camera import CameraSettings
from camera.dummy_camera import DummyCamera
from camera_worker import CameraWorker


if __name__ == '__main__':
    workers = []
    for cam_id in ['One', 'Two', 'Three']:
        worker = CameraWorker.init(
            cam_type=DummyCamera,
            cam_id=cam_id, 
            cam_settings=CameraSettings(exposure_usec=100, gain_analog=17, frame_rate=15, white_balance_auto=True, image_format='RGB', bit_depth=8), 
            timestamp_correction=0,
        )
        worker.start()
        workers.append(worker)




