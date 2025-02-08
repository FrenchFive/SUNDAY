import os
from openai import OpenAI
from pathlib import Path
import dotenv
import csv
import re

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
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow([user, message])  # Writing user and message as separate columns

def get_userdata():
    data_path = f"{DATA_DIR}/userdata.csv"
    if not os.path.exists(data_path):
      return []
    
    with open(data_path, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        return list(reader)

def append_userdata(key, data):
    data_path = f"{DATA_DIR}/userdata.csv"

    with open(data_path, "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow([key, data])

def extract(message):
  pattern = r"--adddata:([a-zA-Z0-9_-]+)-([a-zA-Z0-9_-]+)"  # Regex to match --adddata:key-value
  matches = re.findall(pattern, message)  # Find all matches
  print(matches)
  for match in matches:
    append_userdata(match[0], match[1])

  clean = re.sub(pattern, "", message).strip()
  
  return clean

def personnality():
  with open(f"{DATA_DIR}/personality.txt", "r") as file:
    return file.read()

def ai_chat(message):
  messages=[
    {"role": "developer", "content": personnality()},
    {"role": "developer", "content": f"{str(get_userdata())}"}
  ]
  for mess in get_log():
    messages.append({"role": mess[0], "content": mess[1]})
  messages.append({"role": "user", "content": message})

  completion = CLIENT.chat.completions.create(
    model="gpt-4o",
    messages=messages
  )

  response = completion.choices[0].message.content
  response = extract(response)

  append_log("user", message)
  append_log("assistant", response)
  return response

def ai_audio(txt):
  speech_file_path = f"{DATA_DIR}/speech.mp3"
  response = CLIENT.audio.speech.create(
      model="tts-1",
      voice="sage",
      input=txt,
  )
  response.stream_to_file(speech_file_path)

userInput = input("Enter your message: ")
print(ai_chat(userInput))