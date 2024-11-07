import time
import spacy
import csv
import argparse
from pythonosc import udp_client
from tqdm import tqdm

import os

from utils.gui_controller import set_wekinator_model_values

nlp = spacy.load("en_core_web_md")


def get_story_vector(story):
    doc = nlp(story)
    return doc.vector


def get_osc_client():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
    parser.add_argument(
        "--port", type=int, default=6448, help="The port the OSC server is listening on"
    )
    args = parser.parse_args()

    return udp_client.SimpleUDPClient(args.ip, args.port)


def sendStory(story):
    client = get_osc_client()
    story_vector = get_story_vector(story["transcript"])
    model_values = [
        int(story["religion_beliefs"]) / 100,
        int(story["loved_ones"]) / 100,
        int(story["travel_culture"]) / 100,
        int(story["achievements_triumph"]) / 100,
        int(story["hobbies_interests"]) / 100,
        int(story["aspirations"]) / 100,
        int(story["cues_of_reassurance"]) / 100,
    ]

    # set_wekinator_model_values
    print(f"Setting model values to: {model_values}")
    set_wekinator_model_values(model_values)

    print(f"sending story...")
    client.send_message("/sentiment/input", story_vector.tolist())
    time.sleep(1)


if __name__ == "__main__":
    client = get_osc_client()
    current_dir = os.path.dirname(__file__)
    training_data_path = os.path.join(current_dir, "data", "stories.csv")

    with open(training_data_path, mode="r") as file:
        reader = csv.DictReader(file)
        total_rows = sum(1 for _ in open(training_data_path)) - 1
        for story in tqdm(reader, total=total_rows):
            sendStory(story)
            time.sleep(0.1)
