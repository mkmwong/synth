import numpy as np


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
        self.adtable = self.make_attack_decay_table()
        # self.vectorized_get_amplitude = np.vectorize(self.get_amplitude)

    def make_attack_decay_table(self):
        if self.curve == "expo":
            attack = 1 - np.exp(
                -self.k
                * (
                    np.arange(self.sampling_rate * self.attack_time)
                    / self.sampling_rate
                )
            )
            decay = self.sustain_level + (1 - self.sustain_level) * np.exp(
                -self.k
                * (
                    np.arange(self.sampling_rate * self.attack_time)
                    / self.sampling_rate
                )
            )
            env_arr = np.concatenate([attack, decay])
            return env_arr

    # def make_release_table(self):

    def get_amplitude(self, sample_passed, start_amp):
        if start_amp != 0 and sample_passed == 0:  # reattack condition
            last_attk_pos = np.round(self.attack_time * self.sampling_rate)
            print(f" last_attk_pos {last_attk_pos}")
            sample_passed = np.abs(self.adtable[0:last_attk_pos] - start_amp).argmin()
            print(
                f"reattacking from {sample_passed} which has amp of {self.adtable[sample_passed]}"
            )
        amp_arr = np.full(self.buffer_size, self.sustain_level)
        if sample_passed <= len(self.adtable):
            if len(self.adtable) - sample_passed < self.buffer_size:
                ad_end = len(self.adtable)
                amp_end = len(self.adtable) - sample_passed
            else:
                ad_end = sample_passed + self.buffer_size
                amp_end = self.buffer_size
            amp_arr[0:amp_end] = self.adtable[sample_passed:ad_end]
        return amp_arr
