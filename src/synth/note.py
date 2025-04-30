from __future__ import annotations
import numpy as np
from adsr import ADSREnvelope


class Note:
    def __init__(self, freq: float, step_size: int, adsr: ADSREnvelope):
        # TODO should throw exception if freq is not float
        # TODO should throw exception if step_size is not int
        # Todo should throw exception if adsr is not an envelope
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

    def __str__(self) -> str:
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

    def start_attack(self) -> None:
        self.state = "attack"
        self.sample_passed = 0
        self.attack_table = self.make_attack_table(self.last_amplitude)

    def start_release(self) -> None:
        self.state = "release"
        self.release_sample = 0
        self.release_table = self.make_release_table(self.last_amplitude)

    def reset_notes(self) -> None:
        self.phase = 0.0
        self.sample_passed = 0
        self.state = "idle"
        self.release_amplitude = 0
        self.release_sample = 0

    def make_attack_table(self, starting_amp) -> np.ndarray:
        return self.adsr.make_attack_table(starting_amp)

    def make_release_table(self, starting_amp) -> np.ndarray:
        return self.adsr.make_release_table(starting_amp)
