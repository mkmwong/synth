from __future__ import annotations
import numpy as np
from numba import njit


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
        env_arr = np.empty(len(attack) + len(decay))
        env_arr[: len(attack)] = attack
        env_arr[len(attack) :] = decay
    return env_arr


@njit
def make_release_table_jit(
    curve: str, starting_amplitude: float, sampling_rate: int, release_time: float
) -> np.ndarray:
    num_sample = int(release_time * sampling_rate)
    if curve == "expo":
        t = np.arange(num_sample) / sampling_rate
        rel_table = starting_amplitude * np.exp(-t / (release_time / -np.log(0.001)))
    return rel_table


class ADSREnvelope:
    def __init__(
        self,
        t_att: float,
        t_dec: float,
        sus_lvl: float,
        t_rel: float,
        curve: str,
        bs: int,
        sr: int,
        k: int,
    ):
        self.attack_time = t_att
        self.decay_time = t_dec
        self.sustain_level = sus_lvl
        self.release_time = t_rel
        self.curve = curve
        self.phase = "idle"
        self.time_passed = 0
        self.buffer_size = bs
        self.sampling_rate = sr
        self.time_chunk = self.buffer_size / self.sampling_rate
        self.k = k

    def make_attack_table(self, starting_amplitude: float) -> np.ndarray:
        tab = make_attack_table_jit(
            self.curve,
            starting_amplitude,
            self.sampling_rate,
            self.attack_time,
            self.sustain_level,
            self.decay_time,
            self.k,
        )
        return tab

    def make_release_table(self, starting_amplitude: float) -> np.ndarray:
        tab = make_release_table_jit(
            self.curve, starting_amplitude, self.sampling_rate, self.release_time
        )
        return tab

    def get_amplitude(self, note: "Note") -> np.ndarray:
        attack_table = note.attack_table
        release_table = note.release_table
        amp_arr = np.full(self.buffer_size, self.sustain_level)
        if note.state == "sustain":
            pass
        elif note.state == "attack" or note.state == "decay":
            tab_start_pos = note.sample_passed
            tab_end_pos = min(note.sample_passed + self.buffer_size, len(attack_table))
            arr_end_pos = min(tab_end_pos - tab_start_pos, self.buffer_size)
            amp_arr[0:arr_end_pos] = attack_table[tab_start_pos:tab_end_pos]
            note.sample_passed += self.buffer_size
            if (
                note.state == "attack"
                and note.sample_passed >= self.attack_time * self.sampling_rate
            ):
                note.state = "decay"
            if (
                note.state == "decay"
                and note.sample_passed
                >= (self.attack_time + self.decay_time) * self.sampling_rate
            ):
                note.state = "sustain"
        elif note.state == "release":
            tab_start_pos = note.release_sample
            tab_end_pos = min(
                note.release_sample + self.buffer_size, len(release_table)
            )
            arr_end_pos = min(tab_end_pos - tab_start_pos, self.buffer_size)
            amp_arr[0:arr_end_pos] = release_table[tab_start_pos:tab_end_pos]
            if arr_end_pos < self.buffer_size:
                amp_arr[arr_end_pos:] = 0.0
            note.release_sample += self.buffer_size
            if note.release_sample >= self.release_time * self.sampling_rate:
                note.reset_notes()
        else:
            amp_arr[:] = 0
        note.last_amplitude = amp_arr[-1]
        return amp_arr
