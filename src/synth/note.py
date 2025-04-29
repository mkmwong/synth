import numpy as np


class Note:
    def __init__(self, freq, step_size, adsr):
        self.freq = freq
        self.phase = 0.0
        self.step_size = step_size
        self.sample_passed = 0
        self.state = "idle"
        self.last_amplitude = 0.0
        self.release_sample = 0
        self.adsr = adsr
        self.attack_table = np.empty(0)
        self.release_table = np.empty(0)

    def __str__(self):
        def preview(arr, max_len=10):
            if arr.size == 0:
                return "[]"
            elif arr.size <= max_len:
                return np.array2string(arr, precision=3, separator=", ")
            else:
                return f"{np.array2string(arr[:max_len], precision=3, separator=', ')} ... (len={len(arr)})"

        return (
            f"Note object:\n"
            f"  freq: {self.freq}\n"
            f"  phase: {self.phase}\n"
            f"  step_size: {self.step_size}\n"
            f"  sample_passed: {self.sample_passed}\n"
            f"  state: {self.state}\n"
            f"  last_amplitude: {self.last_amplitude}\n"
            f"  release_sample: {self.release_sample}\n"
            f"  adsr: {self.adsr}\n"
            f"  attack_table: {preview(self.attack_table)}\n"
            f"  release_table: {preview(self.release_table)}"
        )

    def start_attack(self):
        self.state = "attack"
        self.sample_passed = 0
        self.make_attack_table(self.last_amplitude)

    def start_decay(self):
        self.state = "decay"

    def start_sustain(self):
        self.state = "sustain"

    def start_release(self):
        self.state = "release"
        self.make_release_table(self.last_amplitude)

    def reset_notes(self):
        self.phase = 0.0
        self.sample_passed = 0
        self.state = "idle"
        self.release_amplitude = 0
        self.release_sample = 0

    def make_attack_table(self, starting_amp):
        self.attack_table = self.adsr.make_attack_table(starting_amp)

    def make_release_table(self, starting_amp):
        self.release_table = self.adsr.make_release_table(starting_amp)
