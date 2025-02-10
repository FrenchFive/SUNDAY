from consts import ROOT_DIR, DATA_DIR
import ai
import mic

if __name__ == "__main__":
    while True:
        user = mic.record()
        loop = True
        while loop:
            result, submit = ai.ai_chat(user)

        print(result)
        ai_audio_path = ai.ai_audio(result)
        mic.play(ai_audio_path)
