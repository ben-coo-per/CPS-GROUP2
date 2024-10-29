import os
from training.utils.openai import client


def get_transcription(file_path: str) -> str:
    audio_file = open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=audio_file, response_format="text"
    )
    return transcription


current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "Louis.m4a")
text = get_transcription(file_path)
print(text)
