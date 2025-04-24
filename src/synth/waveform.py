import numpy as np
import sounddevice as sd
from typing import Tuple, Generator
from adsr import ADSREnvelope
import logging


class Waveform:
    def __init__(self, sr, type, adsr, freq):
        if type not in ["sine", "sawtooth", "triangle", "square"]:
            raise ValueError(
                f"Waveform type '{self.type} is not supported'. Expected one of ['sine', 'sawtooth', 'triangle', 'square']."
            )
        self.sampling_rate = sr
        self.type = type
        self.adsr = adsr
        self.freq = freq

    def generate_waveform(
        self,
        k,
        buffer_size: int = 2048,
    ) -> Generator[Tuple[np.ndarray, int], None, None]:

        ph = 0.0
        t = np.arange(buffer_size) / self.sampling_rate
        if not self.adsr.start_attack():
            logging.warning(f"Failed to start attack for frequencing {self.freq}")
        while True:
            current_t = ph + t
            if self.type == "sine":
                wave = np.sin(2 * np.pi * self.freq * current_t)
            elif self.type == "sawtooth":
                wave = 2 * (t - np.floor(current_t)) - 1
            elif self.type == "triangle":
                wave = 2 * np.arcsin(np.sin(2 * np.pi * self.freq * current_t)) / np.pi
            elif self.type == "square":
                wave = np.sign(np.sin(2 * np.pi * self.freq * current_t))

            amp_arr = self.adsr.get_amplitude_arr(k)
            if np.all(amp_arr == 0):
                logging.warning("Amplitude is 0. Exiting generator")
                return

            yield wave * amp_arr, self.sampling_rate
            ph += buffer_size / self.sampling_rate
