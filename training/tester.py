# client.py

import argparse

from utils.speech_to_text import get_story_vector
from utils.wekinator_osc import get_wekinator_input_client


def main(send_ip, send_port, story):
    client = get_wekinator_input_client(ip=send_ip, send_port=send_port)

    test_vector = get_story_vector(story).tolist()

    # Send the test message
    print("Sending message...")
    client.send_message("/sentiment/input", test_vector)
    print(f"Sent vector.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip", default="127.0.0.1", help="The IP to send OSC messages to"
    )
    parser.add_argument(
        "--port", type=int, default=6448, help="The port to send OSC messages to"
    )
    parser.add_argument(
        "--story",
        type=str,
        default="",
        help="The story to convert into a vector and send",
    )

    args = parser.parse_args()

    main(args.ip, args.port, args.story)
