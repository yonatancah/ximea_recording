import sys
from triggers.keyboard_trigger_detector import KeyboardTriggerDetector
from triggers.pylsl_trigger_detector import PyLSLTriggerDetector

#detector = KeyboardTriggerDetector()

detector = PyLSLTriggerDetector()
detector.start_trigger_detected.connect(lambda data: print(data))
detector.stop_trigger_detected.connect(lambda data: print(data))


print('press a key')

while True:
    detector.wait_for_triggers(start='start', stop='stop', close='close')
