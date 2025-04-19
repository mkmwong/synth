import mido
from midi_control import MidiControl
from keyboard import Keys
from generate_waveform import generate_waveform

def start_midi_control():
    midi_ctrl = MidiControl()
    midi_ctrl.setup_ports()

def start_keyboard_listener():
    keys = Keys()
    keys.start_keyboard()

if __name__ == "__main__":
    start_midi_control()
    start_keyboard_listener()
