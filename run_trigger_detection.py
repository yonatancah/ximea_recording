import sys
from triggers.keyboard_trigger_detector import KeyboardTriggerDetector
from triggers.pylsl_trigger_detector import PyLSLTriggerDetector

#detector = KeyboardTriggerDetector()

detector = PyLSLTriggerDetector()
detector.start_trigger_detected.connect(lambda: print('start detected'))
detector.stop_trigger_detected.connect(lambda: print('stop detected'))
detector.close_trigger_detected.connect(lambda: (print('close detected'), sys.exit()))


print('press a key')

while True:
    detector.wait_for_triggers(start='start', stop='stop', close='close')
