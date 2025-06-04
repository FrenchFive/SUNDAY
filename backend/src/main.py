from consts import ROOT_DIR, DATA_DIR
import ai
import mic

def main() -> None:
    """Continuously record audio and reply using the AI assistant."""
    while True:
        try:
            user = mic.record()
            if not user:
                continue
            print(user)

            result, _ = ai.ai_chat(user)
            print(result)

            ai_audio_path = ai.ai_audio(result)
            print(ai_audio_path)

            mic.play_sound(ai_audio_path)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
