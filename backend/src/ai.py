import os
import base64
from io import BytesIO
from openai import OpenAI
import dotenv
import csv
import re
from datetime import datetime
import pyautogui

from consts import (
    ROOT_DIR,
    DATA_DIR,
    BACKEND_DIR,
    CHAT_MODEL,
    TTS_MODEL,
    SEARCH_MODEL,
)
from search import web_search
import json

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
    if matches:
      print(matches)
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
      temp_add("The current running apps is unknown")

  #GETScreenShot
  pattern = r"--getscreenshot"  # Regex to match --getscreenshot
  matches, message = _ext(pattern, message)
  if matches:
    loop = True
    shot = capture_screenshot()
    if shot:
      temp_add(json.dumps({"image": shot}))

  return message, loop

def plan_actions(message: str) -> dict:
  """Use a lightweight model to decide on helper actions.

  Returns a dictionary with optional keys:
    - ``search``: a query string if a web search is suggested
    - ``screenshot``: boolean
    - ``running_apps``: boolean
  """
  history = get_log()[-6:]  # last 3 exchanges
  msgs = [
      {"role": "system", "content": (
          "Reply ONLY in valid JSON. Decide which helper actions are needed "
          "before another AI crafts the final answer. Keys: 'search' (string or "
          "null), 'screenshot' (true/false), 'running_apps' (true/false). "
          "If no actions are needed use null/false." )},
      {"role": "system", "content": basic_context()},
  ]
  if history:
      msgs.extend({"role": role, "content": content} for role, content in history)
  user_data = get_userdata()
  if user_data:
      msgs.append({"role": "system", "content": f"User data: {user_data}"})
  msgs.append({"role": "user", "content": message})

  try:
    completion = CLIENT.chat.completions.create(
        model=SEARCH_MODEL,
        messages=msgs,
    )
    reply = completion.choices[0].message.content.strip()
    actions = json.loads(reply)
  except Exception:
    return {"search": None, "screenshot": False, "running_apps": False}

  return {
      "search": actions.get("search"),
      "screenshot": bool(actions.get("screenshot")),
      "running_apps": bool(actions.get("running_apps")),
  }

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

def basic_context() -> str:
  """Return a short string describing the current time and known location."""
  now = datetime.now().strftime("%Y-%m-%d %H:%M")
  context = f"The current time is {now}."
  location = None
  for key, value in get_userdata():
    if key.lower() in ("city", "location", "place", "town"):
      location = value
      break
  if location:
    context += f" The user's location is {location}."
  return context

def capture_screenshot() -> str | None:
  """Return a data URL containing a PNG screenshot, or None on failure."""
  try:
    img = pyautogui.screenshot()
    buf = BytesIO()
    img.save(buf, format="PNG")
    encoded = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"
  except Exception as ex:
    temp_add(f"Screenshot failed: {ex}")
    return None

def personnality():
  with open(f"{DATA_DIR}/personality.txt", "r") as file:
    return file.read()

def ai_chat(message):
  messages=[
    {"role": "developer", "content": personnality()},
    {"role": "developer", "content": f"{str(get_userdata())}"},
    {"role": "system", "content": basic_context()},
  ]
  for mess in get_log():
    messages.append({"role": mess[0], "content": mess[1]})
  if get_temp()!=[]:
    for mess in get_temp():
      try:
        info = json.loads(mess[0])
        if isinstance(info, dict) and "image" in info:
          messages.append({
              "role": "system",
              "content": [
                  {"type": "text", "text": "Screenshot from user."},
                  {"type": "image_url", "image_url": {"url": info["image"], "detail": "low"}},
              ],
          })
        else:
          messages.append({"role": "system", "content": mess[0]})
      except Exception:
        messages.append({"role": "system", "content": mess[0]})

  actions = plan_actions(message)
  if actions.get("search"):
    results = web_search(actions["search"])
    messages.append({"role": "system", "content": f"Web search results for '{actions['search']}':\n{results}"})
  if actions.get("screenshot"):
    shot = capture_screenshot()
    if shot:
      messages.append({
          "role": "system",
          "content": [
              {"type": "text", "text": "Screenshot from user."},
              {"type": "image_url", "image_url": {"url": shot, "detail": "low"}},
          ],
      })
  if actions.get("running_apps"):
    if os.name == 'nt':
      running = os.popen("tasklist").read()
    elif os.name == 'posix':
      running = os.popen("ps -A").read()
    else:
      running = "Unknown OS"
    messages.append({"role": "system", "content": f"Running applications:\n{running}"})

  messages.append({"role": "user", "content": message})

  completion = CLIENT.chat.completions.create(
    model=CHAT_MODEL,
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
      model=TTS_MODEL,
      voice="sage",
      input=txt,
  )
  response.stream_to_file(speech_file_path)
  return speech_file_path

