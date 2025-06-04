# SUNDAY
An AI Assistant that listens for the **Sunday** wake word and replies using OpenAI.

## Usage
Install the dependencies:

```bash
pip install -r requirements.txt
```

Ensure the environment variable `OPENAI_KEY` contains your API key. Then run:

```bash
python -m backend.src.main
```

The assistant first runs a lightweight model to decide if helper actions are
needed. This model sees the last few messages, any saved user data and the
current date/time. It can request a web search, capture a screenshot or list
running applications. If a screenshot is requested the image itself is sent to
the OpenAI model (not just the path) so it can be analysed. Search results and
other gathered information are then passed to the main model so responses are
personalised (for example, saving your city allows weather queries to use that
location).

The assistant automatically adds context like the current time and any stored
location when preparing responses.

Persist information with the special command `--adddata:key-value`. Any saved
data is automatically included when determining search queries.

Optional environment variables `CHAT_MODEL`, `TTS_MODEL` and `SEARCH_MODEL` let
you choose which OpenAI models to use. By default the assistant relies on the
lightweight `gpt-4o` model for chat, `tts-1` for speech synthesis and
`gpt-3.5-turbo` for search queries.

