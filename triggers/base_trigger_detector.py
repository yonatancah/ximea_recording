from __future__ import annotations

from abc import ABC, abstractmethod

from .signal import Signal


class BaseTriggerDetector(ABC):
    start_trigger_detected: Signal
    stop_trigger_detected: Signal
    close_trigger_detected: Signal

    def __init__(self) -> None:
        self.start_trigger_detected = Signal()
        self.stop_trigger_detected = Signal()
        self.close_trigger_detected = Signal()

    @abstractmethod
    def wait_for_triggers(self, start: str, stop: str, close: str) -> None:
        ...

    




