from consts import ROOT_DIR, DATA_DIR
import ai
import mic

if __name__ == "__main__":
    while True:
        user = mic.record()
        loop = True
        print(user)
        result, submit = ai.ai_chat(user)

        print(result)
        ai_audio_path = ai.ai_audio(result)
        print(ai_audio_path)

        mic.play_sound(ai_audio_path)
