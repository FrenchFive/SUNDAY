from RealtimeSTT import AudioToTextRecorder
import sounddevice as sd
import os
from pydub import AudioSegment

import simpleaudio as sa

from consts import DATA_DIR

# Get the default microphone index
DEVICE_ID = sd.default.device[0]
DEFAULT_AUDIO = f"{DATA_DIR}/sfx_start.mp3"
WW_PATH = f"{DATA_DIR}/sunday.onnx"

def play_sound(audio):
    """Plays an MP3 file using simpleaudio."""
    audio = audio.replace("\\", "/")
    
    if not os.path.exists(audio):
        print(f"Error: File not found - {audio}")
        return
    
    # Convert MP3 to WAV for simpleaudio
    sound = AudioSegment.from_file(audio, format="mp3")
    temp_wav = f"{DATA_DIR}/temp_audio.wav"
    sound.export(temp_wav, format="wav")

    # Play the converted WAV file
    wave_obj = sa.WaveObject.from_wave_file(temp_wav)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until the sound finishes playing

    # Clean up temp file
    os.remove(temp_wav)


def record():
    """Records audio, prints transcribed text, and plays sound if the wakeword is detected."""
    recorder = AudioToTextRecorder(
        wakeword_backend="oww",
        wake_words_sensitivity=0.35,
        openwakeword_model_paths=WW_PATH,
        wake_word_buffer_duration=1,
        input_device_index=DEVICE_ID,
    )

    return recorder.text()