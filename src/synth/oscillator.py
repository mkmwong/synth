import numpy as np
import time
from adsr import ADSREnvelope
from numba import njit
from utils import compute_buffer

class Oscillator:
    def __init__(self, type, tb_size, bs, sampling_rate, adsr):
        self.type = type
        self.table_size = tb_size
        self.sampling_rate = sampling_rate
        self.wave_table = self.make_wave_table()
        self.buffer_size = bs
        self.current_notes = {}
        self.note_off_queue = []
        self.adsr = adsr
        self.arange_buffer = np.arange(self.buffer_size)

    def note_on(self, note, freq):
        inc = self.table_size * freq / self.sampling_rate
        self.current_notes[note] = (
            freq,
            0.0,
            inc,
            0,
        )  # phase and phase increase, and sample done
        pass

    def note_off(self, note):
        print(f"trying to off {note}, queue right now is {self.note_off_queue}")
        if note not in self.note_off_queue:
            self.note_off_queue.append(note)
        else:
            print(f"note {note} is already in off queue")
        pass

    def make_wave_table(self):
        if self.type == "sine":
            tab = np.sin(
                2 * np.pi * np.arange(self.table_size) / self.table_size
            ).astype(np.float32)
            return tab

    def get_buffer(self, note):
        freq, phase, inc, sample_done = self.current_notes[note]
        buf, new_phase = compute_buffer(phase, inc, self.arange_buffer, self.table_size, self.wave_table, self.buffer_size)
        self.current_notes[note] = (
            freq,
            new_phase,
            inc,
            sample_done + self.buffer_size,
        )
        return buf

    def mix_waves(self):
        # print(f"self.current_notes are {self.current_notes}")
        out_arr = np.zeros(self.buffer_size)
        if len(self.current_notes) > 0:
            keys = list(self.
            current_notes.keys())
            for note in keys:
                t1 = time.time()
                buf = self.get_buffer(note)
                t2 = time.time()
                amp = self.adsr.get_amplitude(self.current_notes[note][3])
                t3 = time.time()
                out_arr += buf * amp
                t4 = time.time()
                print(f"time to get wave buffer for {note} is {t2 - t1}")
                #print(f"time to get adsr env for {note} is {t3 - t2}")
                #print(f"time to multiple for {note} is {t4 - t3}")
            out_arr = out_arr / len(self.current_notes)
        if len(self.note_off_queue) > 0:
            print(f"In mix wave, queue right now is {self.note_off_queue}")
            if self.note_off_queue[0] in self.current_notes:
                del self.current_notes[self.note_off_queue[0]]
            self.note_off_queue.pop(0)

        return out_arr
