#include <FastLED.h>
#define NUM_LEDS 100
#define DATA_PIN 6
#define LED_GROUP_SIZE 10
CRGB leds[NUM_LEDS];

// Define LED groups
CRGB* LED_GROUP_A = &leds[0];
CRGB* LED_GROUP_B = &leds[10];
CRGB* LED_GROUP_C = &leds[20];
CRGB* LED_GROUP_D = &leds[30];
CRGB* LED_GROUP_E = &leds[40];
CRGB* LED_GROUP_F = &leds[50];
CRGB* LED_GROUP_G = &leds[60];
CRGB* LED_GROUP_H = &leds[70];
CRGB* LED_GROUP_I = &leds[80];
CRGB* LED_GROUP_J = &leds[90];

// Color definitions
CRGB colors[] = {
  CRGB::Purple,    // Religion_Beliefs
  CRGB::Red,       // Loved Ones
  CRGB::Green,     // Travel_Culture
  CRGB::Silver,    // Achievements_Triumph
  CRGB::Yellow,    // Hobbies_Interests
  CRGB::Orange,    // Aspirations
  CRGB::Blue, // Cues of Reassurance
  CRGB::Brown      // Practicality_Utility
};

void setup() {
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  Serial.begin(9600);
  while (!Serial) {
    // Wait for serial connection
  }
}

void loop() {
  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n');  // Read the full message
    int selectedColors[8] = {0};  // Array to store parsed values

    // Parse the incoming string to populate selectedColors array
    int index = 0;
    char *token = strtok((char*)inputString.c_str(), ",");
    while (token != NULL && index < 8) {
      selectedColors[index] = atoi(token);  // Convert to integer and store
      token = strtok(NULL, ",");
      index++;
    }

    // Create a list of colors to choose from based on the selectedColors array
    CRGB availableColors[8];
    int availableCount = 0;

    for (int i = 0; i < 8; i++) {
      if (selectedColors[i] == 1) {
        availableColors[availableCount] = colors[i];
        availableCount++;
      }
    }

    // Assign colors to LED groups randomly from available colors
    if (availableCount > 0) {
      for (int group = 0; group < 10; group++) {
        CRGB selectedColor = availableColors[random(availableCount)];

        // Assign color to the current LED group
        for (int i = 0; i < LED_GROUP_SIZE; i++) {
          leds[group * LED_GROUP_SIZE + i] = selectedColor;
        }
      }
    } else {
      // If no colors are selected, turn off all LEDs
      fill_solid(leds, NUM_LEDS, CRGB::Black);
    }

    FastLED.show();
    delay(250);  // Delay to avoid rapid updates
  }

  FastLED.show();
  delay(40);
}
