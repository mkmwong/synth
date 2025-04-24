import mido
from midi_control import MidiControl
from virtual_keyboard import Keys

# from generate_waveform import generate_waveform
from synth import Synth
import sounddevice as sd
from utils import make_audio_callback

if __name__ == "__main__":
    t_att = 0.2
    t_dec = 0.2
    sus_lvl = 0.7
    t_rel = 0.2
    curve = "expo" 
    bs = 4096
    sr = 44100
    k = 5
    type = "sine"
    syn = Synth(
        t_att=t_att,
        t_dec=t_dec,
        sus_lvl=sus_lvl,
        t_rel=t_rel,
        curve=curve,
        bs=bs,
        sr=sr,
        type=type,
        k = k
    )
    syn.switch_on()
