# Attack: Time taken for the rise of the level from nil to peak
# Decay: Time taken for the level to reduce from attack to sustain
# Sustain: Leel maintain until the key is released
# Release: time level to decay to nil

import numpy as np

class ADSREnvelope:
    def __init__(self, t_att, t_dec, sus_lvl, t_rel, curve, bs, sr):
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
        self.time_chunk = self.buffer_size/self.sampling_rate
        self.vectorized_get_amplitude = np.vectorize(self.get_amplitude)

    def start_attack(self):
        self.time_passed = 0
        self.phase = "attack"

    def end_attack(self):
        self.time_passed = 0
        self.phase = "release" 


    def get_amplitude_arr(self, k):
        pos_arr = np.linspace(self.time_passed, self.time_passed + self.time_chunk, self.buffer_size )
        #pos_arr = pos_arr * self.time_passed
        amp_arr = self.vectorized_get_amplitude(pos_arr, k)
        self.time_passed += self.time_chunk
    #print(amp_arr)
        import time
        #time.sleep(20)
        return amp_arr

    def get_amplitude(self, t, k):
        #print(f"time is {t} in get_amp")
        # if phase is attack  & t is < 
        # ta, do attack calculation 
        if self.phase == "attack" and t <= self.attack_time:
            #print("in attack")
            amp = 1 - np.exp (-k * t / self.attack_time )

        # if phase is attack t  & is > ta but < ta + td, do decay calculation 
        elif self.phase == "attack" and ( t > self.attack_time and t <= self.attack_time + self.decay_time):
            #print("in decay")
            amp = self.sustain_level + (1 - self.sustain_level) * np.exp(-k * (t-self.attack_time)/self.decay_time)

        # if phase is attack  t &  is > td, do sustain 
        elif self.phase == "attack" and t > self.attack_time + self.decay_time:
            #print("in sustain")
            amp = self.sustain_level
        # if phrase is release and t is < tr, do release, else reset 
        elif self.phase == "release" and t <= self.release_time:
            amp = self.sustain_level * np.exp(-k * t/self.release_time)
        elif self.phase == "release" and t > self.release_time:
            amp = 0
            self.phrase = "idle"
        return amp