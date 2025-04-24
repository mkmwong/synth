import numpy as np


def note_to_frequency(midi_note: int) -> float:
    return 440.0 * (2 ** ((midi_note - 69) / 12))


def make_audio_callback(midi_ctrl):
    def audio_callback(outdata, frames, time, status):
        if status:
            print(status)
        mix = np.zeros((frames, 1), dtype=np.float32)

        for note, gen in list(midi_ctrl.on_notes.items()):
            try:
                wave_chunk, _ = next(gen)
                mix += wave_chunk.reshape(-1, 1)
            except StopIteration:
                print("Stopping playback.")
        outdata[:] = mix

    return audio_callback
