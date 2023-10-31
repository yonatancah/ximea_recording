from __future__ import annotations

from .base_trigger_detector import BaseTriggerDetector

import keyboard



# Set up the hook


# Keep the program running


class KeyboardTriggerDetector(BaseTriggerDetector):

    def __init__(self) -> None:
        super().__init__()
        self._pressed_keys = set()  # Set to keep track of pressed keys
        # keyboard.hook(on_key_event) 
        

    def wait_for_triggers(self, start: str, stop: str, close: str) -> None:
        while True:
            event: keyboard.KeyboardEvent = keyboard.read_event()
            if event.event_type == 'down':  # only respond to keydown events
                if event.name == start:
                    self.start_trigger_detected.send()
                elif event.name == stop:
                    self.stop_trigger_detected.send()
                elif event.name == close:
                    self.close_trigger_detected.send()
                else:
                    continue
                break



#     def on_key_event(event):
#         global pressed_keys
#         if event.name == 'a':
#             if event.event_type == keyboard.KEY_DOWN:
#                 if 'a' not in pressed_keys:
#                     print('The "a" key was pressed down.')
#                     pressed_keys.add('a')
#             elif event.event_type == keyboard.KEY_UP:
#                 pressed_keys.discard('a')


