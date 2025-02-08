import os
from openai import OpenAI
from pathlib import Path
import dotenv

from consts import ROOT_DIR, DATA_DIR, BCKEND_DIR

dotenv.load_dotenv()

key = os.getenv("OPENAI_KEY")
CLIENT = OpenAI(api_key=key)

def personnality():
  with open(f"{DATA_DIR}/personality.txt", "r") as file:
    return file.read()

def ai_chat(messages):
  completion = CLIENT.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "developer", "content": personnality()},
      {"role": "user", "content": f"{messages}"}
    ]
  )
  return completion.choices[0].message.content

def ai_audio(txt):
  speech_file_path = f"{BCKEND_DIR}/speech.mp3"
  response = CLIENT.audio.speech.create(
      model="tts-1",
      voice="sage",
      input=txt,
  )
  response.stream_to_file(speech_file_path)

response = ai_chat("hey Yo Whats up today?")
ai_audio(response)