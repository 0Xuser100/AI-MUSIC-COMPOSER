import music21
import numpy as np
import io
from scipy.io.wavfile import write as wav_write
from synthesizer import Synthesizer, Waveform
from loguru import logger


def note_to_frequencies(note_list):
    freqs = []
    for note_str in note_list:
        try:
            note = music21.note.Note(note_str)
            freqs.append(note.pitch.frequency)
        except Exception as e:
            logger.warning("Invalid note ignored: {!r} ({})", note_str, e)
    return freqs


def generate_wav_bytes_from_notes_freq(notes_freq):
    if not notes_freq:
        logger.warning("No valid frequencies provided; returning empty audio.")
        return b""
    synth = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
    sample_rate = 44100
    chunks = [synth.generate_constant_wave(freq, 0.5) for freq in notes_freq]
    audio = np.concatenate(chunks)
    buffer = io.BytesIO()
    wav_write(buffer, sample_rate, audio.astype(np.float32))
    return buffer.getvalue()


# if __name__ == "__main__":
#     logger.info("Starting audio generation test...")

#     notes = ["C4", "E4", "G4", "C5"]
#     logger.info("Input notes: {}", notes)

#     freqs = note_to_frequencies(notes)
#     logger.info("Frequencies (Hz): {}", freqs)

#     wav_bytes = generate_wav_bytes_from_notes_freq(freqs)
#     logger.info("Generated WAV bytes: {} bytes", len(wav_bytes))

#     if wav_bytes:
#         out_path = "out.wav"
#         with open(out_path, "wb") as f:
#             f.write(wav_bytes)
#         logger.success("Saved {}", out_path)
#     else:
#         logger.warning("No audio produced (empty WAV bytes). Check your notes / parsing.")
