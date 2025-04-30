from __future__ import annotations
import numpy as np
import time
from numba import njit
from typing import Callable
from sounddevice import CallbackFlags


@njit
def make_attack_table_jit(
    curve: str,
    starting_amplitude: float,
    sampling_rate: int,
    attack_time: float,
    sustain_level: float,
    decay_time: float,
    k: int,
) -> np.ndarray:
    if curve == "expo":
        attack = starting_amplitude + (1 - starting_amplitude) * (
            1
            - np.exp(
                -k
                * (np.arange(sampling_rate * attack_time) / sampling_rate)
                / attack_time
            )
        )
        decay = sustain_level + (1 - sustain_level) * np.exp(
            -k * (np.arange(sampling_rate * decay_time) / sampling_rate) / decay_time
        )
        env_arr = np.concatenate([attack, decay])
    return env_arr


@njit
def make_release_table_jit(
    curve: str,
    starting_amplitude: float,
    num_sample: int,
    sampling_rate: int,
    release_time: float,
) -> np.ndarray:
    if curve == "expo":
        t = np.arange(num_sample) / sampling_rate
        rel_table = starting_amplitude * np.exp(-t / (release_time / -np.log(0.001)))
    return rel_table


@njit
def compute_buffer(
    phase: float,
    inc: int,
    arange_buffer: np.ndarray,
    table_size: int,
    wave_table: np.ndarray,
    buffer_size: int,
):
    idxs = (phase + inc * arange_buffer) % table_size
    idxs = idxs.astype(np.int32)
    buf = np.take(wave_table, idxs)
    new_phase = phase + inc * buffer_size % table_size
    return buf, new_phase


def note_to_frequency(midi_note: int) -> float:
    return 440.0 * (2 ** ((midi_note - 69) / 12))


def save_to_csv(mix_buffer: np.ndarray, filename="audio_data.csv") -> None:
    # Open the file in append mode
    with open(filename, mode="a") as f:
        np.savetxt(f, mix_buffer, delimiter=",", fmt="%.6f")  # Save the amplitudes only


def make_audio_callback(osc: "Oscillator") -> Callable:
    def audio_callback(
        outdata: np.ndarray, frame: int, t: float, status: CallbackFlags
    ):
        try:
            # starttime = time.time()
            aud = osc.mix_waves()
            outdata[:] = aud.reshape(-1, 1) * 0.1
            # endtime = time.time()
            # if (endtime - starttime) >= 4096 / 44100 * 0.5:
            # print(f"time take to callback is {endtime - starttime}")
            with open("audio.csv", "a") as f:
                np.savetxt(f, outdata, fmt="%.10f", delimiter=",")
        except Exception as e:
            print(f"Error in audio callback: {e}")

    return audio_callback
