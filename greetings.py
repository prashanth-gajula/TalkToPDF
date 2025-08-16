from langchain_openai import ChatOpenAI
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") 

import io

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # reads OPENAI_API_KEY from env

def tts_synthesize(text: str, voice: str = "alloy", fmt: str = "mp3") -> bytes:
    """
    Convert text to speech using OpenAI TTS and return raw audio bytes.
    Works with the streaming interface.
    """
    buf = io.BytesIO()
    # Enter the streaming response context
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
        response_format=fmt,   # "mp3" | "wav" | "opus" | "flac"
    ) as resp:
        # Option A: stream into memory
        for chunk in resp.iter_bytes():
            buf.write(chunk)
        audio_bytes = buf.getvalue()

        # Option B (simpler): stream directly to a file
        # resp.stream_to_file("greeting.mp3")

    return audio_bytes



def speak_greeting():
    llm = ChatOpenAI(model="gpt-4o-mini")
    msg = llm.invoke(
        "In ~60–90 words, welcome the learner. "
        "Explain you're grounded in the uploaded PDF and can summarize, clarify, and quiz. "
        "Be friendly and concise."
    ).content

    audio = tts_synthesize(msg)  # bytes (mp3/wav) from your TTS wrapper
    return msg, audio
