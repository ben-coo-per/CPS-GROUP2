import threading
import time
from utils.arduino_lights import (
    get_arduino_port,
    get_boolean_light_array,
    send_light_array_to_arduino,
)
from utils.serial_comm import ArduinoSerial

from utils.generate_receipt import send_data_to_processing
from utils.normalize_values import get_theme_values_dict
from utils.speech_to_text import get_transcription
from utils.record_audio import record_audio
from utils.send_to_wekinator import send_story_to_wekinator
from utils.wekinator_osc import get_wekinator_osc_server


arduino_port = get_arduino_port()
arduino_serial = ArduinoSerial(arduino_port)


def start_recording():
    arduino_serial.send_app_state(1)  # Set app state to "Recording"


def stop_recording():
    print("Recording stopped")
    arduino_serial.send_app_state(0)  # Set app state to "Idle"


def handle_wekinator_response(_, *args):
    print(f"Received message from Wekinator")
    print(f"Message: {args}")
    theme_dict = get_theme_values_dict(list(args))
    send_data_to_processing(theme_dict)

    led_array = get_boolean_light_array(theme_dict)
    send_light_array_to_arduino(led_array)
    time.sleep(2)
    arduino_serial.send_app_state(2)  # Set app state to "Playback"


def start_osc_server():
    # Start the Wekinator OSC server
    get_wekinator_osc_server(handle_wekinator_response)


if __name__ == "__main__":
    osc_thread = threading.Thread(target=start_osc_server)
    # osc_thread.daemon = True  # Allows the thread to exit when the main program ends
    osc_thread.start()

    button_thread = threading.Thread(
        target=arduino_serial.listen_for_button, args=(start_recording, stop_recording)
    )
    button_thread.start()

    # audio_file_path = record_audio()
    # transcription = get_transcription(audio_file_path)

    # send_story_to_wekinator(transcription)
