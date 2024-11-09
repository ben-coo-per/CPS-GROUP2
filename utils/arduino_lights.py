from typing import List
import serial
import serial.tools.list_ports

vis_threshold = 0.2


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
    ports = serial.tools.list_ports.comports()
    available_ports = [port.device for port in ports]

    # use this to find the correct port
    print("Available ports:")
    print(available_ports)

    ser = serial.Serial(available_ports[5], 9600)
    ser.write(bytes(light_array))
    ser.close()


if __name__ == "__main__":
    send_light_array_to_arduino([1, 0, 1, 0, 1, 0, 1, 0])
