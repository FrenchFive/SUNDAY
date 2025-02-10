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
    log_path = f"{DATA_DIR}/chat.csv"
    
    log = get_log()

    # Append the new message
    log.append([user, message.replace("\n", "")])

    # Keep only the last 10 entries
    log = log[-10:]

    # Write the trimmed log back to the file
    with open(log_path, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerows(log)

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
  loop = False
  def _ext(pattern, message):
    matches = re.findall(pattern, message)
    print (matches)
    clean = re.sub(pattern, "", message).strip()
    return matches, clean
    
  #USER DATA
  pattern = r"--adddata:([a-zA-Z0-9_-]+)-([a-zA-Z0-9_-]+)"  # Regex to match --adddata:key-value
  matches, message = _ext(pattern, message)
  for match in matches:
    append_userdata(match[0], match[1])
  
  #GETRUNNING APPS
  pattern = r"--getrunningapps"  # Regex to match --getrunningapps
  matches, message = _ext(pattern, message)
  if matches:
    loop = True
    #get a list of the current running apps
    if os.name == 'nt':
      temp_add("The current running apps are: "+os.system("tasklist"))
    elif os.name == 'posix':
      temp_add("The current running apps are: "+os.system("ps -A"))
    else:
      temp_add("The current running apps is unknown"))

  #GETScreenShot 
  pattern = r"--getscreenshot"  # Regex to match --getscreenshot
  matches, message = _ext(pattern, message)
  if matches:
    loop = True
    #get a screenshot of the current screen
    temp_add("The screenshot is saved at: "+os.system(f"gnome-screenshot -f {BCKEND_DIR}/screenshot.png"))

  return message, loop

def get_temp():
    tmp_path = f"{DATA_DIR}/tmp.csv"
    if not os.path.exists(tmp_path):
      return []
    
    with open(tmp_path, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        return list(reader)

def temp_add(data):
  tmp_path = f"{DATA_DIR}/tmp.csv"

  with open(tmp_path, "a", newline='', encoding="utf-8") as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerow([data])

def temp_clear():
  tmp_path = f"{DATA_DIR}/tmp.csv"
  with open(tmp_path, "w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerows([])

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
  if get_temp()!=[]:
    for mess in get_temp():
      messages.append({"role": "system", "content": mess[0]})
  messages.append({"role": "user", "content": message})

  completion = CLIENT.chat.completions.create(
    model="gpt-4o",
    messages=messages
  )

  response = completion.choices[0].message.content
  response, loop = extract(response)

  append_log("user", message)
  append_log("assistant", response)
  temp_clear()
  return response, loop

def ai_audio(txt):
  speech_file_path = f"{DATA_DIR}/speech.mp3"
  response = CLIENT.audio.speech.create(
      model="tts-1",
      voice="sage",
      input=txt,
  )
  response.stream_to_file(speech_file_path)
  return speech_file_path
