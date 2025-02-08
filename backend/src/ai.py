import os
from openai import OpenAI
from pathlib import Path
import dotenv
import csv

from consts import ROOT_DIR, DATA_DIR, BCKEND_DIR

dotenv.load_dotenv()

key = os.getenv("OPENAI_KEY")
CLIENT = OpenAI(api_key=key)

def get_log():
    log_path = f"{DATA_DIR}/chat.csv"
    if not os.path.exists(log_path):
      return []
    
    with open(log_path, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        return list(reader)

def append_log(user, message):
    get_log()
    log_path = f"{DATA_DIR}/chat.csv"

    # Open the file in append mode
    with open(log_path, "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        # Append the new message correctly
        writer.writerow([user, message])  # Writing user and message as separate columns

def personnality():
  with open(f"{DATA_DIR}/personality.txt", "r") as file:
    return file.read()

def ai_chat(message):
  messages=[
    {"role": "developer", "content": personnality()},
  ]
  for mess in get_log():
    messages.append({"role": mess[0], "content": mess[1]})
  messages.append({"role": "user", "content": message})

  completion = CLIENT.chat.completions.create(
    model="gpt-4o",
    messages=messages
  )

  response = completion.choices[0].message.content
  append_log("user", message)
  append_log("assistant", response)
  return response

def ai_audio(txt):
  speech_file_path = f"{BCKEND_DIR}/speech.mp3"
  response = CLIENT.audio.speech.create(
      model="tts-1",
      voice="sage",
      input=txt,
  )
  response.stream_to_file(speech_file_path)

userInput = input("Enter your message: ")
print(ai_chat(userInput))