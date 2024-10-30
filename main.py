from utils.speech_to_text import get_transcription
from utils.record_audio import record_audio

if __name__ == "__main__":
    audio_file_path = record_audio()
    transcription = get_transcription(audio_file_path)
    print(transcription)
