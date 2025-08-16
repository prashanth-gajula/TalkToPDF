# stt_whisper.py
from __future__ import annotations
from openai import OpenAI
import io
from typing import Optional
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # reads OPENAI_API_KEY from env

def transcribe_audio(
    audio_bytes: bytes,
    *,
    model: str = "whisper-1",          
    filename: str = "speech.wav",
    language: Optional[str] = "en",    # e.g., "en"
    prompt: Optional[str] = None       # optional biasing prompt
) -> str:
    """
    Convert audio bytes to text using OpenAI Whisper (server-side).
    Returns the transcript string. Raises on API errors.
    """
    file_tuple = (filename, io.BytesIO(audio_bytes))
    resp = client.audio.transcriptions.create(
        model=model,
        file=file_tuple,
        language=language,
        prompt=prompt,
        # temperature=0  # uncomment if you want more deterministic output
    )
    # OpenAI returns either .text or .segments; .text is the final transcript
    return resp.text.strip()
