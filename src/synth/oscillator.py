import numpy as np
from utils import compute_buffer, note_to_frequency
from note import Note


class Oscillator:
    def __init__(self, type, tb_size, bs, sampling_rate, adsr):
        self.type = type
        self.table_size = tb_size
        self.sampling_rate = sampling_rate
        self.wave_table = self.make_wave_table()
        self.buffer_size = bs
        self.all_notes = {}
        self.adsr = adsr
        for note in range(1, 129):
            freq = note_to_frequency(note)
            step_size = self.table_size * freq / self.sampling_rate
            self.all_notes[note] = Note(freq, step_size, self.adsr)
        self.arange_buffer = np.arange(self.buffer_size)
        self.rel_samples = self.adsr.release_time * self.sampling_rate

    def note_on(self, notename):
        note = self.all_notes[notename]
        note.start_attack()

    def note_off(self, notename):
        note = self.all_notes[notename]
        note.start_release()

    def get_active_notes(self):
        active_notes = [
            key for key, val in self.all_notes.items() if val.state != "idle"
        ]
        return active_notes

    def make_wave_table(self):
        if self.type == "sine":
            tab = np.sin(
                2 * np.pi * np.arange(self.table_size) / self.table_size
            ).astype(np.float32)
            return tab

    def get_buffer(self, note):
        phase = note.phase
        inc = note.step_size
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
        keys = self.get_active_notes()
        if len(keys) > 0:
            print(f"active notes are {keys}")
            for notename in keys:
                note = self.all_notes[notename]
                buf, new_phase = self.get_buffer(note)
                amp = self.adsr.get_amplitude(
                    note
                )  # sample_done, note.last_amplitude, notename)
                note.phase = new_phase
                out_arr += buf * amp
            out_arr = out_arr / len(keys)
        return out_arr
