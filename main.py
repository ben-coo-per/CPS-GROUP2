import threading

from utils.normalize_values import get_theme_values_dict
from utils.speech_to_text import get_transcription
from utils.record_audio import record_audio
from utils.send_to_wekinator import send_story_to_wekinator
from utils.wekinator_osc import get_wekinator_osc_server


def handle_wekinator_response(_, *args):
    print(f"Received message from Wekinator")
    print(f"Message: {args}")
    theme_dict = get_theme_values_dict(list(args))
    print(theme_dict)


def start_osc_server():
    # Start the Wekinator OSC server
    get_wekinator_osc_server(handle_wekinator_response)


if __name__ == "__main__":
    osc_thread = threading.Thread(target=start_osc_server)
    # osc_thread.daemon = True  # Allows the thread to exit when the main program ends
    osc_thread.start()

    audio_file_path = record_audio()
    transcription = get_transcription(audio_file_path)

    send_story_to_wekinator(transcription)
