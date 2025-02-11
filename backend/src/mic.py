from RealtimeSTT import AudioToTextRecorder
import sounddevice as sd
from pydub import AudioSegment
from pydub.playback import play

from consts import ROOT_DIR

# Get the default microphone index
DEVICE_ID = sd.default.device[0]
DEFAULT_AUDIO = f"{ROOT_DIR}/backend/data/sfx_start.mp3"
WW_PATH = f"{ROOT_DIR}/backend/data/sunday.onnx"

def play_audio(audio):
    """Plays an audio file."""
    sound = AudioSegment.from_file(audio, format="mp3")
    play(sound)

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