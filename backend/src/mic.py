from RealtimeSTT import AudioToTextRecorder
import sounddevice as sd
import os

from consts import ROOT_DIR

# Get the default microphone index
default_device_index = sd.default.device[0]

# Define the path to your custom wake word file (.ppn)
ww_path = f"{ROOT_DIR}/backend/data/sunday.onnx"

def record():
    # Initialize RealtimeSTT with the custom wake word
    recorder = AudioToTextRecorder(
        wakeword_backend="oww",
        wake_words_sensitivity=0.35,
        openwakeword_model_paths=ww_path,
        wake_word_buffer_duration=1,
        input_device_index=default_device_index
    )

    print('Say "Sunday" to start recording.')
    print(recorder.text())

if __name__ == "__main__":
    record()