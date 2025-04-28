from mido import Message
from oscillator import Oscillator
from utils import note_to_frequency
import sounddevice as sd
import numpy as np
import time
import logging


class MidiControl:
    def __init__(self, oscillator, bs: int, k: int, on_notes: dict):
        self.oscillator = oscillator
        self.bs = bs
        # self.on_notes = on_notes
        self.k = k

    # self.count = 0

    def note_on(self, msg: Message) -> bool:
        try:
            freq = note_to_frequency(msg.note)
            self.oscillator.note_on(msg.note, freq)
            return True
        except Exception as e:
            logging.exception(f"Exception encountered in note_on : {e}")
            return False

    def note_off(self, msg: Message) -> bool:
        # print("midi off ")
        try:
            # if msg.note not in self.on_notes:
            #    logging.warning(
            #        f"Note {msg.note} is already not in on_note. This is a bug!"
            #   )
            # else:
            self.oscillator.note_off(msg.note)
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
