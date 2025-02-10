from consts import ROOT_DIR, DATA_DIR
import ai 
import mic

while True:
    user = mic.record()

    result = ai.ai_chat(user)
    print(result)
    ai_audio_path = ai.ai_audio(result)
    mic.play(ai_audio_path)
    