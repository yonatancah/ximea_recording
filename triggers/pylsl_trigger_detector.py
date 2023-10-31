import json
import time

import pylsl

from .base_trigger_detector import BaseTriggerDetector


class PyLSLTriggerDetector(BaseTriggerDetector):

    def __init__(self, timeout=30, verbose=True) -> None:
        super().__init__()
        if verbose:
            print("Waiting for PYLSL Stream to be available...", flush=True)
        t0 = time.perf_counter()
        while time.perf_counter() - t0 < timeout:
            self.streams=pylsl.resolve_stream()
            try:
                stream = self.streams[0]
            except IndexError:
                time.sleep(.5)
                continue
            self.inlet=pylsl.StreamInlet(stream)
            break
        else:
            if verbose:
                print("...timed out", flush=True)
            raise IOError("No PYLSL Connection before timeout.")
        

    def wait_for_triggers(self, start: str, stop: str, close: str) -> None:
        while True:
            sample,timestamp=self.inlet.pull_sample(timeout=100, )

            if sample is not None:
                trigger_message=sample[0]
                message=json.loads(trigger_message)

                if message.get('command')==start:
                    self.start_trigger_detected.send()

                elif message.get('command')==stop:
                    self.stop_trigger_detected.send()

                else:
                    continue

                break
