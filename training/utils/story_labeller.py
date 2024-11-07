import os
import time
from utils.openai_client import client
import json
import csv
from tqdm import tqdm

current_dir = os.path.dirname(__file__)

system_prompt = """You are a sentimental meaning game machine. You assign values to stories about an object supplied by the player from (0-10) based on how much the story fits into 8 themes:
- Religion & Beliefs: objects with religious beliefs, spirituality, superstition, etc. associated with them.
- Loved Ones: objects with sentimental meaning relating to family, friends, pets, or other loved ones.
- Travel & Cultures: objects related to travel, vacations, or cultural experiences.
- Achievements & Triumph: objects that relate to the player's successes, achievement, or signify accomplishment.
- Hobbies & Interests: objects that relate to the sports, exercise, arts, etc. that the player is interested in and a part of their identity they want to express.
- Aspirations: objects that signify who the player wants to become in life, or the type of life they want to live.
- Cues of Relief or Reassurance: objects that are a source of comfort for the user; something they turn to for emotional relief.
- Practicality & Utility: objects that have a utilitarian purpose for the player.

You will be given a story, then you will respond with a valid JSON object
with an example structure like:
{"religion_beliefs": 2, "loved_ones": 4, "travel_culture": 4, 
"achievements_triumph": 0, "hobbies_interests": 0, "aspirations": 3, 
"cues_of_reassurance": 1, "practicality_utility": 2}.
You will not include anything in your response besides the dictionary."""


def label_story(src, story, writer):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": story},
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Extracting the response content
    json_string = response.choices[0].message.content
    try:
        obj = json.loads(json_string)
        # Append the result to the CSV
        append_row(src, story, obj, writer)

    except json.JSONDecodeError:
        print("Error decoding JSON string")
        print("Trying again...")
        try:
            label_story(src, story, writer)
        except Exception as e:
            print(f"Error: {e}")
        return


def append_row(src, story, obj, writer):
    # Write the story and the values as a row in the CSV
    writer.writerow(
        [
            src,
            story,
            obj.get("religion_beliefs", 0),
            obj.get("loved_ones", 0),
            obj.get("travel_culture", 0),
            obj.get("achievements_triumph", 0),
            obj.get("hobbies_interests", 0),
            obj.get("aspirations", 0),
            obj.get("cues_of_reassurance", 0),
            obj.get("practicality_utility", 0),
        ]
    )


if __name__ == "__main__":
    print("Starting the story labeller")
    # Define paths for the CSV files
    stories_csv_path = os.path.join(current_dir, "stories_source.csv")
    stories_new_csv_path = os.path.join(current_dir, "stories_new.csv")

    # Open the output CSV file in write mode with a CSV writer
    with open(stories_new_csv_path, mode="w", newline="") as output_file:
        writer = csv.writer(output_file)

        # Write the header row
        writer.writerow(
            [
                "source",
                "transcript",
                "religion_beliefs",
                "loved_ones",
                "travel_culture",
                "achievements_triumph",
                "hobbies_interests",
                "aspirations",
                "cues_of_reassurance",
                "practicality_utility",
            ]
        )

        # Read from the input CSV file and process each story
        with open(stories_csv_path, mode="r", newline="") as input_file:
            reader = csv.DictReader(input_file)
            print('Labelling stories from "stories.csv"\n\n\n')
            total_rows = sum(1 for _ in open(stories_csv_path)) - 1
            for row in tqdm(reader, total=total_rows):
                label_story(row["Source"], row["Transcript"], writer)
                time.sleep(1)
