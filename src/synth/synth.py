from virtual_keyboard import Keys
from midi_control import MidiControl
from adsr import ADSREnvelope
from waveform import Waveform
import threading

class Synth():
    def __init__(self, t_att, t_dec, sus_lvl, t_rel, curve, bs, sr, type):
        self.adsr = ADSREnvelope(t_att, t_dec, sus_lvl, t_rel, curve, bs, sr)
        self.Waveform = Waveform(sr, type, self.adsr)
        self.midi_ctrl = MidiControl(self.Waveform)
        self.keyboard = Keys(self.midi_ctrl)

    def switch_on(self):
        #self.keyboard.start_keyboard()
        keyboard_thread = threading.Thread(target = self.keyboard.start_keyboard, daemon = True)
        keyboard_thread.start()

        