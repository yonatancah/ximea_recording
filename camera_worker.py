from __future__ import annotations
from pathlib import Path

from typing import NamedTuple
from multiprocessing import Process, Queue
from camera import CameraSettings

from camera.base_camera import BaseCamera
from writers import VideoWriter, TimestampWriter

## Program Configuration

def run_camera(queue: Queue, cam_id: str, cam_settings: CameraSettings, timestamp_correction: int = 0) -> None:
    cam = BaseCamera.open(id=cam_id)
    cam.set_settings(settings=cam_settings)
    cam.set_timestamp_correction(timestamp_correction)

    while True:
        event = queue.get()
        if event.type == "start":
            event: StartEvent
            path = Path(event.destination).with_suffix(cam_id)
            video_writer = VideoWriter.open(fname=str(path.with_suffix(".mkv")))
            timestamp_writer = TimestampWriter.open(str(path.with_suffix("_timestamps.txt")))
            cam.start()
            while True:
                if queue.empty():
                    frame = cam.get_frame()
                    video_writer.write(frame=frame)
                    timestamp_writer.write(
                        timestamp=frame.timestamp, 
                        corrected_timestamp=frame.corrected_timestamp,
                    )
                else:
                    event = queue.get()
                    if event.type == "stop":
                        video_writer.close()
                        timestamp_writer.close()
                        cam.stop()
                        break
                    elif event.type == "close":
                        cam.close()
                        return
                    else:
                        raise ValueError(f"Unrecognized Event: {event}")
        elif event.type == "close":
            cam.close()
            return
        else:
            raise ValueError(f"Unrecognized Event: {event}")
                        




    # cam.start()

class StartEvent(NamedTuple):
    destination: str
    type: str = "start"


class StopEvent(NamedTuple):
    type: str = "stop"

class CloseEvent(NamedTuple):
    type: str = "close"


class CameraWorker(NamedTuple):
    process: Process
    queue: Queue

    @classmethod
    def init(cls, cam_id: str, cam_settings: CameraSettings, timestamp_correction: int = 0) -> CameraWorker:
        queue = Queue()
        return CameraWorker(
            process=Process(target=run_camera, args=(queue, cam_id, cam_settings, timestamp_correction)),
            queue=queue,
        )

    def start(self) -> None:
        self.process.start()

    def join(self) -> None:
        self.process.join()

    def send_start_event(self, destination: str) -> None:
        self.queue.put(StartEvent(destination=destination))

    def send_stop_event(self) -> None:
        self.queue.put(StopEvent())

    def send_close_event(self) -> None:
        self.queue.put(CloseEvent())
