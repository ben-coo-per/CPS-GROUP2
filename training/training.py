import time
import spacy

import argparse

from pythonosc import udp_client

from data.stories import emotion_stories


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


def trainForEmotion(emotion, stories):
    client = get_osc_client()
    for i, story in enumerate(stories):
        story_vector = get_story_vector(story)
        print(f"sending {emotion} story {i+1}/{len(stories)}")
        client.send_message("/sentiment/input", story_vector.tolist())
        time.sleep(1)


if __name__ == "__main__":
    client = get_osc_client()
    for emotion, stories in emotion_stories.items():
        print(f"Set the next class in Wekinator")
        input(f"then press enter to start training for {emotion}")
        trainForEmotion(emotion, stories)
