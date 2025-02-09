import speech_recognition as sr

print("Available Microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")

def listen_and_write(mic_index=0):  # Change mic_index to the correct device index
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=mic_index)
    
    print("Listening... (say 'exit' to stop)")

    with open("spoken_text.txt", "a") as file:
        while True:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Speak now...")
                try:
                    audio = recognizer.listen(source)
                    text = recognizer.recognize_google(audio)
                    print(f"You said: {text}")
                    
                    if text.lower() == "exit":
                        print("Exiting...")
                        break
                    
                    file.write(text + "\n")

                except sr.UnknownValueError:
                    print("Could not understand audio.")
                except sr.RequestError:
                    print("Error connecting to the recognition service.")

if __name__ == "__main__":
    mic_index = int(input("Enter the microphone index: "))  # Ask user for mic index
    listen_and_write(mic_index)
