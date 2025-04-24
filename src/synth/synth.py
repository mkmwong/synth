from virtual_keyboard import Keys
from midi_control import MidiControl
from adsr import ADSREnvelope
from waveform import Waveform
from utils import note_to_frequency, make_audio_callback
import threading
import numpy as np
import sounddevice as sd


class Synth:
    def __init__(self, t_att, t_dec, sus_lvl, t_rel, curve, bs, sr, type, k):
        self.adsr = ADSREnvelope(t_att, t_dec, sus_lvl, t_rel, curve, bs, sr)
        self.sampling_rate = sr
        self.bs = bs
        self.waveforms = {}
        for midi_note in range(128):
            freq = note_to_frequency(midi_note)
            waveform = Waveform(sr, type, self.adsr, freq)
            self.waveforms[midi_note] = waveform
        self.midi_ctrl = MidiControl(self.waveforms, self.bs)
        self.midi_ctrl = MidiControl(self.waveforms,k)
        self.keyboard = Keys(self.midi_ctrl)

    def switch_on(self):
        keyboard_thread = threading.Thread(
            target=self.keyboard.start_keyboard, daemon=True
        )
        keyboard_thread.start()
        audio_callback = make_audio_callback(self.midi_ctrl)
        stream = sd.OutputStream(
            callback=audio_callback,
            samplerate=self.sampling_rate,
            blocksize=self.bs,
            channels=1,
            dtype="float32",
        )
        stream.start()
        while True:
            pass
