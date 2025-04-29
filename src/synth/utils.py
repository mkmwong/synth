import numpy as np
import time
from numba import njit


@njit
def make_attack_table_jit(
    curve, starting_amplitude, sampling_rate, attack_time, sustain_level, decay_time, k
):
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
    curve, starting_amplitude, num_sample, sampling_rate, release_time
):
    if curve == "expo":
        t = np.arange(num_sample) / sampling_rate
        rel_table = starting_amplitude * np.exp(-t / (release_time / -np.log(0.001)))
    return rel_table


@njit
def get_expo_release_table(off_queue, rel_time, sample_rate, buffer_size):
    time_passed = off_queue[1]
    amp = off_queue[0]
    num_sample = int(rel_time * sample_rate)
    t = np.arange(num_sample) / sample_rate
    rel_table = amp * np.exp(-t / (rel_time / -np.log(0.001)))
    end_point = min(time_passed + buffer_size, len(rel_table))
    ret_arr = np.zeros(buffer_size)
    ret_arr[0 : end_point - time_passed] = rel_table[time_passed:end_point]
    return ret_arr, time_passed + buffer_size


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
