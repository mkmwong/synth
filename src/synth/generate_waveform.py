import numpy as np
import sounddevice as sd
from typing import Tuple

def note_to_frequency(midi_note: int) -> float:
    return 440.0 * (2 ** ((midi_note - 69)/ 12))

# what is the minimum sampling rate allowed?
# duration should never be allowed to be 0 ?
def generate_waveform(
    frequency: float = 440.0,
    sampling_rate: int = 44100,
    type: str = "sine",
    buffer_size: int = 1024,
) -> Tuple[np.ndarray, int]:

    if type not in ["sine", "sawtooth", "triangle", "square"]:
        raise ValueError(
            f"Waveform type '{type} is not supported'. Expected one of ['sine', 'sawtooth', 'triangle', 'square']."
        )
    ph = 0.0
    t = np.arange(buffer_size) / sampling_rate
    #t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    while True:
        current_t = ph + t 
        if type == "sine":
            wave = np.sin(2 * np.pi * frequency * current_t)
        elif type == "sawtooth":
            wave = 2 * (t - np.floor(current_t)) - 1
        elif type == "triangle":
            wave = 2 * np.arcsin(np.sin(2 * np.pi * frequency * current_t)) / np.pi
        elif type == "square":
            wave = np.sign(np.sin(2 * np.pi * frequency * current_t))
        yield wave, sampling_rate
        ph += buffer_size / sampling_rate
    #play_wave(wave, sampling_rate)
    return wave, sampling_rate


def play_wave(wave: np.ndarray, sr: int) -> bool:
    try:
        sd.play(wave, samplerate=sr, blocking=True)
        return True
    except Exception as e:
        print(f"Error during playback: {e}")
        return False


if __name__ == "__main__":
    generate_waveform(type="triangle")
