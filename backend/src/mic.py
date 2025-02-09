import speech_recognition as sr

'''
print("Available Microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")
'''


def listen_and_write(mic_index=3):  # Change mic_index to the correct device index
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=mic_index)
    
    print("Listening... (say 'exit' to stop)")

    while True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            # recognizer.energy_threshold = 300  # Adjust value if necessary
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                
                if "sunday" in text.lower():
                    print("-- SUNDAY DETECTED")
                    break
                
            except sr.RequestError:
                print("Error connecting to the recognition service.")

listen_and_write()