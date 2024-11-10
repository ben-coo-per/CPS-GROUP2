from pythonosc import udp_client
import time

from utils.normalize_values import get_theme_values_dict


def get_processing_client(ip="127.0.0.1", port=1334):
    return udp_client.SimpleUDPClient(ip, port)


def generate_data_packet(value_dict: dict[str, float]) -> str:
    """
    Generate a data packet string from the given categories and values.
    """
    print("valdict ", value_dict)
    categories = list(value_dict.keys())
    values = list(value_dict.values())
    return ",".join(f"{cat}:{perc}" for cat, perc in zip(categories, values))


def send_data_to_processing(value_dict: dict[str, float]) -> None:
    client = get_processing_client()
    data_str = generate_data_packet(value_dict)
    client.send_message("/update_data", data_str)
    time.sleep(0.1)  # Wait briefly to ensure the message is fully sent


if __name__ == "__main__":
    """
    To test, run this script and check the Processing for the output.
    """
    values = [0.77, 0.10, 0.6, 0.35, 0.25, 0.9, 0.1, 0]
    theme_dict = get_theme_values_dict(values)
    send_data_to_processing(theme_dict)
