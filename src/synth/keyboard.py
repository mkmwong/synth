from pynput import keyboard


class Keys:
    def __init__(self):
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
                print(f"Pressed {self.key_map[key.char]} ")
                self.pressed.add(key.char)
                return True
            elif key.char in ["q", "w"]:
                self.shift_octave(key.char)
                return True
            else:
                print(f"Pressed invalid key.")
                return False
        except AttributeError as e:
            print(f"Error: {e}")
            return False

    def on_release(self, key: keyboard.Key):
        try:
            if key.char in self.key_map:
                print(f"Released {self.key_map[key.char]} ")
                self.pressed.remove(key.char)
        except AttributeError as e:
            print(f"Error: {e}")

    def start_keyboard(self):
        with keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        ) as listener:
            listener.join()


if __name__ == "__main__":
    keys = Keys()
    keys.start_keyboard()
