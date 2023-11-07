from __future__ import annotations
from pathlib import Path
import os

from typing import NamedTuple, Type
from multiprocessing import Process, Queue
from camera import CameraSettings

from camera.base_camera import BaseCamera
from video_writers.opencv import OpenCVVideoWriter
from timestamp_writers.csv import CSVTimestampWriter


## Program Configuration

def run_camera(queue: Queue, cam_type: Type[BaseCamera], cam_id: str, cam_settings: CameraSettings, timestamp_correction: int = 0) -> None:
    cam = cam_type.init(id=cam_id, settings=cam_settings, start=False, verbose=True)
    
    while True:
        print(f"{cam_id} waiting for queue to fill...")
        event = queue.get()
        print(f"{cam_id} something is in the queue!")
        if event.type == "start":
            print(f"{cam_id} Process: received start trigger", flush=True)
            event: StartEvent
            base_path = Path(r"D:\\")
            # test = r"C:\\Users\\VR-PC-User\\Desktop\\data\\S3_replication\\S3_rep_test\\9990\\S001\\camera\\XIMEARecording_T005_068_rock_novisible_close_attack_weapons_nosafehouse.mkv"
            # event = StartEvent(destination=test)
            destination_path = base_path.joinpath(*Path(event.destination).parts[5:])
            destination_path.stem.mkdir(parents=True, exist_ok=True)

            video_path = destination_path.joinpath(f"{cam_id}_{destination_path.stem}.avi")
            print(f"{cam_id} opening files")
            video_writer = OpenCVVideoWriter.open(fname=str(video_path), frame_rate=cam_settings.frame_rate, fourcc='XVID' ,autoflush=False)
            timestamp_writer = CSVTimestampWriter.open(str(video_path.with_suffix(".txt")))
            
            print(f"{cam_id} starting camera...")
            cam.start()
            while True:
                if queue.empty():
                    frame = cam.get_frame()
                    video_writer.write(frame=frame.image)
                    timestamp_writer.write(
                        timestamp=frame.timestamp, 
                        timestamp_correction=timestamp_correction, #  TODO
                    )
                else:
                    event = queue.get()
                    if event.type == "stop":
                        print(f"{cam_id} Process: received stop trigger", flush=True)
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
            print(f"{cam_id} Process: received close trigger", flush=True)
            cam.close()
            return
        else:
            raise ValueError(f"Unrecognized Event: {event}")
                        

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
    def init(cls, cam_type: Type[BaseCamera], cam_id: str, cam_settings: CameraSettings, timestamp_correction: int = 0) -> CameraWorker:
        queue = Queue()
        return CameraWorker(
            process=Process(target=run_camera, args=(queue, cam_type, cam_id, cam_settings, timestamp_correction)),
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
