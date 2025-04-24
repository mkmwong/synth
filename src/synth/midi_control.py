from mido import Message
from waveform import Waveform
import sounddevice as sd
import numpy as np
import time
import logging


class MidiControl:
    def __init__(self, wave, bs, k):
        self.waveforms = wave
        self.bs = bs
        self.on_notes = {}
        self.k = k

    def note_on(self, msg) -> bool:
        try:
            if msg.note in self.on_notes:
                logging.warning(
                    f" Note {msg.note} is already in on_note. This is a bug!"
                )
            else:
                self.on_notes[msg.note] = self.waveforms[msg.note].generate_waveform(
                    self.k
                )
            return True
        except Exception as e:
            logging.exception(f"Exception encountered in note_on : {e}")
            return False

    def note_off(self, msg) -> bool:
        try:
            if msg.note not in self.on_notes:
                logging.warning(
                    f"Note {msg.note} is already in on_note. This is a bug!"
                )
            else:
                del self.on_notes[msg.note]
                self.waveforms[msg.note].adsr.end_attack()
            return True
        except Exception as e:
            logging.exception(f"Exception encountered in note_off: {e}")
            return False

    def handling_message(self, msg: Message) -> bool:
        success = True
        if msg.type == "note_on":
            success = success and self.note_on(msg)
        elif msg.type == "note_off":
            success = success and self.note_off(msg)
        else:
            logging.warning(f"Encountered unhandled message type: {msg.type}")
        return success
