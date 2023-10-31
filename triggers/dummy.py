from __future__ import annotations
from pathlib import Path

from typing import NamedTuple


class StartTrigger(NamedTuple):
    destination: Path
    type: str = 'start'

class StopTrigger(NamedTuple):
    type: str = 'stop'


def wait_trigger(name: str) -> StartTrigger | StopTrigger:
    if name == "start":
        return StartTrigger(destination=".")