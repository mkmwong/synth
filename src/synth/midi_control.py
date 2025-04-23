from mido import Message
from waveform import Waveform
import sounddevice as sd
import numpy as np
import time

class MidiControl:
    def __init__(self, wave): #, input_name, output_name):
        self.waveforms = wave
        self.on_notes = {}

    def note_on(self,msg):
        #freq = self.note_to_frequency(msg.note)
        #print(f"Received a note on message for {msg.note} at {freq}")
        #self.on_notes[msg.note] = self.waveforms[msg.note]
        #gen = self.Waveform.generate_waveform(5,freq)
        self.on_notes[msg.note] = self.waveforms[msg.note].generate_waveform(5)
        print(self.on_notes)
        #waveform_data = []
        #for i in range(22):  # however many chunks you want
        #    wave_chunk, _ = next(gen)
        #    waveform_data.append(wave_chunk)

        #np.savetxt("waveform_output.csv", waveform_data, delimiter=",")
        #print("waveformsaved ")

        #cb = self.make_callback(gen, 5, freq)
        #with sd.OutputStream(samplerate=self.Waveform.sampling_rate, blocksize = 2048, channels = 1, 
        #                     dtype = 'float32', callback = cb):
        #    print("Streaming...")
        #    while True:
        #        pass

    def note_off(self, msg):
        print(f"Received a note off message for {msg.note}")
        del self.on_notes[msg.note]
        self.waveforms[msg.note].adsr.end_attack()
        pass

    def handling_message(self, msg: Message ):
        if msg.type == "note_on":
            self.note_on(msg)
        elif msg.type == "note_off":
            self.note_off(msg)
        pass

    def make_callback(self,gen, k , freq):
        def waveform_callback( dat, f, t, s):
            if s:
                print(s)
            start_time = time.time()
            try:
                wave, _ = next(gen)
                dat[:] = wave.reshape(-1,1)
            except StopIteration:
                raise sd.CallbackStop()
            end_time = time.time()
            callback_duration = end_time - start_time
            #print(f"Callback executed in {callback_duration:.6f} seconds")
        return waveform_callback
