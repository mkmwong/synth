import numpy as np
import sounddevice as sd
from typing import Tuple, Generator
from adsr import ADSREnvelope


class Waveform:
    def __init__(self, sr, type, adsr, freq):
        if type not in ["sine", "sawtooth", "triangle", "square"]:
            raise ValueError(
                f"Waveform type '{self.type} is not supported'. Expected one of ['sine', 'sawtooth', 'triangle', 'square']."
            )
        #self.frequency = freq
        self.sampling_rate = sr
        self.type = type
        self.adsr = adsr
        self.freq = freq
        
    # what is the minimum sampling rate allowed?
    # duration should never be allowed to be 0 ?
    def generate_waveform(
        self,
        k,
        buffer_size: int = 2048,
    ) -> Generator[Tuple[np.ndarray, int], None, None]:

        ph = 0.0
        t = np.arange(buffer_size) / self.sampling_rate
        self.adsr.start_attack()
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
                print("Amplitude is 0. Exiting generator")
                return

            yield wave * amp_arr, self.sampling_rate
            ph += buffer_size / self.sampling_rate

    def play_wave(self, wave: np.ndarray, sr: int) -> bool:
        try:
            print("playingsound")
            sd.play(wave, samplerate=sr, blocking=True)
            return True
        except Exception as e:
            print(f"Error during playback: {e}")
            return False
        