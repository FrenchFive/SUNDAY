import speech_recognition as sr

def real_time_mic_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for background noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        print("Listening continuously... (Press Ctrl+C to stop)")

        while True:
            try:
                print("\nListening...")
                audio = recognizer.listen(source)  # Capture audio from the mic
                text = recognizer.recognize_google(audio)  # Convert to text
                
                print("You said:", text)
            
            except sr.UnknownValueError:
                print("Could not understand the audio")
            except sr.RequestError:
                print("API unavailable")

# Example Usage:
real_time_mic_to_text()
