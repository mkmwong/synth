import numpy as np
import time
from numba import njit


@njit
def compute_buffer(phase, inc, arange_buffer, table_size, wave_table, buffer_size):
    idxs = (phase + inc * arange_buffer) % table_size
    idxs = idxs.astype(np.int32)
    buf = np.take(wave_table, idxs)
    new_phase = phase + inc * buffer_size % table_size
    return buf, new_phase


def note_to_frequency(midi_note: int) -> float:
    return 440.0 * (2 ** ((midi_note - 69) / 12))


def save_to_csv(mix_buffer, filename="audio_data.csv"):
    # Open the file in append mode
    with open(filename, mode="a") as f:
        np.savetxt(f, mix_buffer, delimiter=",", fmt="%.6f")  # Save the amplitudes only


def make_audio_callback(osc):
    def audio_callback(outdata, frame, t, status):
        starttime = time.time()
        aud = osc.mix_waves()
        outdata[:] = aud.reshape(-1, 1) * 0.1
        endtime = time.time()
        if (endtime - starttime) >= 8192 / 44100 * 0.5:
            print(f"time take to callback is {endtime - starttime}")

    return audio_callback
