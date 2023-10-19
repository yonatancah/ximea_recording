from __future__ import annotations
from pathlib import Path

from typing import NamedTuple
from multiprocessing import Process, Queue

from camera import Camera, CameraSettings, Frame
## Program Configuration


class ConfigData(NamedTuple):
    cam_ids: list[str]
    cam_settings: CameraSettings


def load_config(fname: str) -> ConfigData:
    ...



