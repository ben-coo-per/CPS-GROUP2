from .openai_client import client
import spacy

nlp = spacy.load("en_core_web_md")


def get_story_vector(story):
    doc = nlp(story)
    return doc.vector


def get_transcription(file_path: str) -> str:
    audio_file = open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=audio_file, response_format="text"
    )
    return transcription
