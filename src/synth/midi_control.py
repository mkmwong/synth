from mido import Message
import logging


class MidiControl:
    def __init__(self, oscillator, bs: int, k: int, on_notes: dict):
        self.oscillator = oscillator
        self.bs = bs
        self.k = k

    def note_on(self, msg: Message) -> bool:
        try:
            self.oscillator.note_on(msg.note)
            return True
        except Exception as e:
            logging.exception(f"Exception encountered in note_on : {e}")
            return False

    def note_off(self, msg: Message) -> bool:
        try:
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
