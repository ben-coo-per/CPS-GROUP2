import time
from typing import List
import serial
import serial.tools.list_ports
from utils.serial_comm import ArduinoSerial

vis_threshold = 0.1


def get_arduino_port() -> str:
    ports = serial.tools.list_ports.comports()
    available_ports = [port.device for port in ports]

    # use this to find the correct port
    print("Available ports:")
    print(available_ports)
    return available_ports[5]


arduino_port = get_arduino_port()
arduino_serial = ArduinoSerial(arduino_port)


def get_boolean_light_array(values: dict[str, float]) -> List[int]:
    """
    Get boolean light array from theme values dictionary.
    returns a list of [0, 1] values.
    """
    return list(map(lambda x: int(x > vis_threshold), values.values()))


def send_light_array_to_arduino(light_array: List[int]) -> None:
    """
    Send light array to Arduino via serial connection.
    """
    serial_port = get_arduino_port()
    print(f"Using port: {serial_port}")
    # Ensure the port is correct (e.g., available_ports[0])
    with serial.Serial(serial_port, 9600, timeout=2) as ser:
        time.sleep(2)  # Wait for the connection to stabilize
        message = "lights:" + ",".join(map(str, light_array)) + "\n"
        ser.write(message.encode())
        print("Data sent")


if __name__ == "__main__":
    send_light_array_to_arduino([1, 0, 0, 1, 0, 1, 0, 1])
    time.sleep(2)
    arduino_serial.send_app_state(2)  # Set app state to "Playback"
