import os

DATA_DIR: str = os.path.realpath(os.path.join(os.path.dirname(p=__file__), "../data"))
ROOT_DIR: str = os.path.realpath(os.path.join(os.path.dirname(p=__file__), "../.."))
BACKEND_DIR: str = os.path.realpath(os.path.join(os.path.dirname(p=__file__), ".."))

# Chat, TTS, and search model names. These can be overridden with
# environment variables for flexibility. The defaults favor lightweight,
# fast models.
CHAT_MODEL: str = os.getenv("CHAT_MODEL", "gpt-4o")
TTS_MODEL: str = os.getenv("TTS_MODEL", "tts-1")
# Separate model for generating search queries – defaults to an even lighter
# model so web searches are inexpensive.
SEARCH_MODEL: str = os.getenv("SEARCH_MODEL", "gpt-3.5-turbo")
