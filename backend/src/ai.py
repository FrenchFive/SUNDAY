import os
from openai import OpenAI
import dotenv

dotenv.load_dotenv()

key = os.getenv("OPENAI_KEY")
client = OpenAI(api_key=key)

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "developer", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)
