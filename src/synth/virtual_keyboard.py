from pynput import keyboard
from mido import Message
from midi_control import MidiControl
import time


class Keys:
    def __init__(self, midi_ctrl: MidiControl):
        self.key_map = {
            "s": 60,
            "e": 61,
            "d": 62,
            "r": 63,
            "f": 64,
            "g": 65,
            "y": 66,
            "h": 67,
            "u": 68,
            "j": 69,
            "i": 70,
            "k": 71,
        }
        self.octave = 0  # 0 start at C4, min -3, max 4
        self.pressed = set()
        self.channel = 0
        self.midi_ctrl = midi_ctrl
        # self.pressed_count = 0
        # self.release_count = 0

    def shift_octave(self, shift_dir: str):
        if shift_dir == "q" and self.octave < 4:
            print(f"Shifting up to { 4 + self.octave + 1 }")
            self.key_map = {
                k: v + 12 for k, v in self.key_map.items() if isinstance(v, int)
            }
            self.octave = self.octave + 1
        elif shift_dir == "w" and self.octave > -3:
            print(f"Shifting down to { 4 + self.octave - 1}")
            self.key_map = {
                k: v - 12 for k, v in self.key_map.items() if isinstance(v, int)
            }
            self.octave = self.octave - 1
        else:
            print(f"Reach range limit, cannot perform shift.")

    def on_press(self, key: keyboard.Key):
        try:
            if key.char in self.key_map and key.char not in self.pressed:
                # self.pressed_count = self.pressed_count + 1
                # print(f"Pressed {self.key_map[key.char]}  {self.pressed_count}")
                self.pressed.add(key.char)
                self.send_midi_message("note_on", self.key_map[key.char])
            elif key.char in ["q", "w"]:
                self.shift_octave(key.char)
            elif key.char in self.pressed:
                pass
            else:
                print(f"Pressed invalid key.")
        except AttributeError as e:
            print(f"Error: {e}")

    def on_release(self, key: keyboard.Key):
        try:
            if key.char in self.key_map:
                # self.release_count = self.release_count + 1
                time.sleep(0.1)  # to avoid release before attack
                # print(f"Released {self.key_map[key.char]} {self.release_count}")
                self.pressed.remove(key.char)
                self.send_midi_message("note_off", self.key_map[key.char])
        except AttributeError as e:
            print(f"Error: {e}")

    def start_keyboard(self):
        with keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        ) as listener:
            listener.join()

    def send_midi_message(self, operation: str, note_name: int):
        msg = Message(operation, channel=self.channel, note=note_name)
        self.midi_ctrl.handling_message(msg)
