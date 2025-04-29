from virtual_keyboard import Keys
from midi_control import MidiControl
from adsr import ADSREnvelope
from oscillator import Oscillator
from utils import make_audio_callback, compute_buffer
from adsr import make_attack_table_jit, make_release_table_jit
import threading
import numpy as np
import sounddevice as sd


class Synth:
    def __init__(self, t_att, t_dec, sus_lvl, t_rel, curve, bs, sr, type, k, tb_size):
        self.adsr = ADSREnvelope(t_att, t_dec, sus_lvl, t_rel, curve, bs, sr, k)
        self.sampling_rate = sr
        self.bs = bs
        self.on_notes = {}
        self.oscillator = Oscillator(type, tb_size, bs, sr, self.adsr)
        self.midi_ctrl = MidiControl(self.oscillator, self.bs, k, self.on_notes)
        self.keyboard = Keys(self.midi_ctrl)

    def switch_on(self):
        # dummy calls to jit functions
        a, b = compute_buffer(
            0.0, 1.0, np.arange(self.bs), 10, np.zeros(self.bs, dtype=np.float32), 0
        )
        make_attack_table_jit("expo", 0.0, self.sampling_rate, 0.5, 0.5, 0.5, 5)
        make_release_table_jit("expo", 0.0, self.sampling_rate, 0.5)
        print(f"ready! {a}, {b}")
        device_info = sd.query_devices(kind="output")
        print("Default sample rate:", device_info["default_samplerate"])
        keyboard_thread = threading.Thread(
            target=self.keyboard.start_keyboard, daemon=True
        )
        keyboard_thread.start()
        audio_callback = make_audio_callback(self.oscillator)
        stream = sd.OutputStream(
            callback=audio_callback,
            samplerate=self.sampling_rate,
            blocksize=self.bs,
            channels=1,
            dtype="float32",
            latency="low",
        )
        stream.start()
        while True:
            pass
