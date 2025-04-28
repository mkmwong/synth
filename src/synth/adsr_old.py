import numpy as np
import logging
import time


# TODO should allow different curve type - currently only doing exponential for attack, decay and release
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
        self.amplitude = 0
        self.tmp_amplitude = 0
        self.rel_amplitude = 0
        self.time_chunk = self.buffer_size / self.sampling_rate
        # self.vectorized_get_amplitude = np.vectorize(self.get_amplitude)

    def start_attack(self) -> bool:
        try:
            self.time_passed = 0
            self.phase = "attack"
            return True
        except Exception as e:
            logging.warning(f"Exception encountered in start_attack: {e}")
            return False

    def end_attack(self) -> bool:
        # sdprint("endingattack")
        try:
            self.time_passed = 0
            self.phase = "release"
            self.rel_amplitude = self.tmp_amplitude
            return True
        except Exception as e:
            logging.warning(f"Exceotion encountered in end_attack: {e}")
            return False

    def get_amplitude_arr(self, k: float) -> np.ndarray:
        # Cache the position array if necessary
        if (
            not hasattr(self, "_cached_pos_arr")
            or self._cached_pos_arr.shape[0] != self.buffer_size
        ):
            self._cached_pos_arr = np.linspace(0, self.time_chunk, self.buffer_size)

        t = self._cached_pos_arr + self.time_passed
        amp_arr = np.zeros_like(t)

        ta, td, tr = self.attack_time, self.decay_time, self.release_time
        sl, rel_amp = self.sustain_level, self.rel_amplitude

        if self.phase == "attack":
            decay_start = ta
            decay_end = ta + td

            # Use masks to avoid nested np.where and reduce computation
            mask_attack = t <= ta
            mask_decay = (t > ta) & (t <= decay_end)

            # Precompute values used in both regions
            norm_attack_t = t[mask_attack] / ta
            norm_decay_t = (t[mask_decay] - ta) / td
            one_minus_sl = 1 - sl

            amp_arr[mask_attack] = 1 - np.exp(-k * norm_attack_t)
            amp_arr[mask_decay] = sl + one_minus_sl * np.exp(-k * norm_decay_t)
            amp_arr[t > decay_end] = sl

        elif self.phase == "release":
            mask_release = t <= tr
            amp_arr[mask_release] = rel_amp * np.exp(-k * t[mask_release] / tr)
            amp_arr[t > tr] = 0
            if t[-1] > tr:
                self.phase = "idle"

        else:  # idle
            amp_arr[:] = 0

        self.tmp_amplitude = amp_arr[-1]
        self.time_passed += self.time_chunk
        return amp_arr

    """ def get_amplitude_arr(self, k: int) -> np.ndarray:
        # print(f"phase is {self.phase}")
        pos_arr = np.linspace(
            self.time_passed, self.time_passed + self.time_chunk, self.buffer_size
        )
        amp_arr = self.vectorized_get_amplitude(pos_arr, k)
        self.tmp_amplitude = amp_arr[-1]
        self.time_passed += self.time_chunk
        return amp_arr

    def get_amplitude(self, t: int, k: int) -> np.ndarray:

        # if phase is attack  & t is < ta, do attack calculation
        if self.phase == "attack" and t <= self.attack_time:
            amp = 1 - np.exp(-k * t / self.attack_time)

        # if phase is attack t  & is > ta but < ta + td, do decay calculation
        elif self.phase == "attack" and (
            t > self.attack_time and t <= self.attack_time + self.decay_time
        ):
            amp = self.sustain_level + (1 - self.sustain_level) * np.exp(
                -k * (t - self.attack_time) / self.decay_time
            )

        # if phase is attack  t &  is > td, do sustain
        elif self.phase == "attack" and t > self.attack_time + self.decay_time:
            amp = self.sustain_level

        # if phrase is release and t is < tr, do release, else reset
        elif self.phase == "release" and t <= self.release_time:
            amp = self.rel_amplitude * np.exp(-k * t / self.release_time)
        elif self.phase == "release" and t > self.release_time:
            amp = 0
            self.phase = "idle"
        else:  # this only handle idle cases?
            amp = 0
        return amp """

    """def get_amplitude_arr(self, k: float) -> np.ndarray:
        pos_arr = np.linspace(
            self.time_passed, self.time_passed + self.time_chunk, self.buffer_size
        )
        t = pos_arr  # alias for clarity

        amp_arr = np.zeros_like(t)

        if self.phase == "attack":
            ta, td, sl = self.attack_time, self.decay_time, self.sustain_level

            # Attack phase: t <= ta
            mask_attack = t <= ta
            amp_arr[mask_attack] = 1 - np.exp(-k * t[mask_attack] / ta)

            # Decay phase: ta < t <= ta + td
            mask_decay = (t > ta) & (t <= ta + td)
            decay_t = t[mask_decay] - ta
            amp_arr[mask_decay] = sl + (1 - sl) * np.exp(-k * decay_t / td)

            # Sustain phase: t > ta + td
            mask_sustain = t > ta + td
            amp_arr[mask_sustain] = sl

        elif self.phase == "release":
            tr = self.release_time

            # Release phase: t <= tr
            mask_release = t <= tr
            amp_arr[mask_release] = self.rel_amplitude * np.exp(-k * t[mask_release] / tr)

            # If fully released, switch to idle
            if t[-1] > tr:
                self.phase = "idle"

        else:
            amp_arr[:] = 0  # idle

        self.tmp_amplitude = amp_arr[-1]
        self.time_passed += self.time_chunk
        return amp_arr 
        """
