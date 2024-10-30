import os
import time
from openai_client import client
import json
import csv

current_dir = os.path.dirname(__file__)


def label_story(src, story, writer):
    print("getting response...")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a sentimental meaning game machine. You assign values to stories "
                    "from (0-10) based on how much the story fits into 7 themes:\n"
                    "- Religion & Beliefs\n"
                    "- Loved Ones\n"
                    "- Travel & Cultures\n"
                    "- Achievements & Triumph\n"
                    "- Hobbies & Interests\n"
                    "- Aspirations\n"
                    "- Cues of Relief or Reassurance\n\n"
                    "You will be given a story, then you will respond with a valid JSON object "
                    "with an example structure like:\n"
                    '{"religion_beliefs": 20, "loved_ones": 40, "travel_culture": 40, '
                    '"achievements_triumph": 0, "hobbies_interests": 0, "aspirations": 30, '
                    '"cues_of_reassurance": 10}.\n'
                    "You will not include anything in your response besides the dictionary."
                ),
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
    obj = json.loads(json_string)
    # Append the result to the CSV
    append_row(src, story, obj, writer)


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
        ]
    )


if __name__ == "__main__":

    print("Starting the story labeller")
    # Define paths for the CSV files
    stories_csv_path = os.path.join(current_dir, "stories.csv")
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
            ]
        )

        # Read from the input CSV file and process each story
        with open(stories_csv_path, mode="r", newline="") as input_file:
            reader = csv.DictReader(input_file)
            print('Reading stories from "stories.csv"')
            for row in reader:
                label_story(row["Source"], row["Transcript"], writer)
                time.sleep(1)
