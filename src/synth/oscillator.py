import numpy as np
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
        self.last_amp = {}
        self.adsr = adsr
        self.arange_buffer = np.arange(self.buffer_size)

    def note_on(self, note, freq):
        inc = self.table_size * freq / self.sampling_rate
        if note not in self.current_notes:
            self.current_notes[note] = (
                freq,
                0.0,
                inc,
                0,
            )  # phase and phase increase,sample done, last intensity
        else:
            self.current_notes[note] = (freq, 0.0, inc, 0)
            if note in self.note_off_queue:
                self.note_off_queue.remove(note)

    def note_off(self, note):
        if note not in self.note_off_queue:
            self.note_off_queue.append(note)
        else:
            pass

    def make_wave_table(self):
        if self.type == "sine":
            tab = np.sin(
                2 * np.pi * np.arange(self.table_size) / self.table_size
            ).astype(np.float32)
            return tab

    def get_buffer(self, note):
        freq, phase, inc, sample_done = self.current_notes[note]
        buf, new_phase = compute_buffer(
            phase,
            inc,
            self.arange_buffer,
            self.table_size,
            self.wave_table,
            self.buffer_size,
        )
        return buf, new_phase

    def mix_waves(self):
        out_arr = np.zeros(self.buffer_size)
        if len(self.current_notes) > 0:
            keys = list(self.current_notes.keys())
            for note in keys:
                freq, phase, inc, sample_done = self.current_notes[note]
                buf, new_phase = self.get_buffer(note)
                if note in self.last_amp:
                    lst_amp = self.last_amp[note]
                else:
                    lst_amp = 0
                amp = self.adsr.get_amplitude(sample_done, lst_amp)
                self.current_notes[note] = (
                    freq,
                    new_phase,
                    inc,
                    sample_done + self.buffer_size,
                )
                self.last_amp[note] = amp[-1]
                out_arr += buf * amp
            out_arr = out_arr / len(self.current_notes)
        if len(self.note_off_queue) > 0:
            if self.note_off_queue[0] in self.current_notes:
                del self.current_notes[self.note_off_queue[0]]
            self.note_off_queue.pop(0)

        return out_arr
