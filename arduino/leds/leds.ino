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
  CRGB::Blue,      // Cues of Reassurance
  CRGB::Brown      // Practicality_Utility
};

unsigned long lastColorChange = 0;
const unsigned long colorChangeInterval = 30000;  // 30 seconds
bool colorsAssigned = false;
bool messageReceived = false; // Flag to check if the serial message has been received

void setup() {
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  Serial.begin(9600);

  // Turn off all LEDs initially
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();
}

void loop() {
  // Check for a serial message and process it
  // if (Serial.available() > 0) {
    // String inputString = Serial.readStringUntil('\n');  // Read the full message
    String inputString = "0,1,1,0,0,1,0,0";  // Read the full message

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
          FastLED.show();
        }
      }
      colorsAssigned = true;     // Mark colors as assigned
      messageReceived = true;    // Mark message as received
    } else {
      // If no colors are selected, turn off all LEDs
      fill_solid(leds, NUM_LEDS, CRGB::Black);
      colorsAssigned = false;
      messageReceived = false;
      FastLED.show();
    }

    delay(250);  // Delay to avoid rapid updates
  // }

  // Only run the rest of the loop if the message has been received
  if (messageReceived) {
    // Sequentially turn on LEDs after color assignment
    if (colorsAssigned) {
      for (int i = 0; i < NUM_LEDS; i++) {
        // Turn on each LED in sequence, leaving the previous ones on
        leds[i] = leds[i]; // Keep the assigned color
        FastLED.show();
        delayMicroseconds(200);  // 0.2ms interval between each LED turning on
      }
      colorsAssigned = false;  // Reset the flag after the initial turn-on sequence
    }

    // Check if it's time to reassign colors every 30 seconds
    if (millis() - lastColorChange >= colorChangeInterval) {
      lastColorChange = millis();

      // Randomly reassign colors to each LED group
      for (int group = 0; group < 10; group++) {
        CRGB newColor = colors[random(8)];  // Choose a new random color

        // Apply the new color to each LED in the group
        for (int i = 0; i < LED_GROUP_SIZE; i++) {
          leds[group * LED_GROUP_SIZE + i] = newColor;
        }
      }
      FastLED.show();
    }
  }

  delay(40);
}
