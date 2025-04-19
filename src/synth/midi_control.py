from generate_waveform import *

class MidiControl:
    def __init__(self, input_name, output_name):
        pass

    def note_on(self,msg):
        freq = note_to_frequency(msg.node)
        wave, _ = generate_waveform(frequency = freq)

    def note_off(self, msg):
        pass
    def start_listening(self):
        pass