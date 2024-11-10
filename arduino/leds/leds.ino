#include <FastLED.h>
#define NUM_LEDS 100
#define DATA_PIN 5
#define LED_GROUP_SIZE 10  // Number of LEDs per color group
#define TRICKLE_SPEED 100  // Speed of the trickle effect in milliseconds
CRGB leds[NUM_LEDS];

// Define the possible colors
CRGB colors[] = {
  CRGB::Purple,  // Religion_Beliefs
  CRGB::Red,     // Loved Ones
  CRGB::Green,   // Travel_Culture
  CRGB::Silver,  // Achievements_Triumph
  CRGB::Yellow,  // Hobbies_Interests
  CRGB::Orange,  // Aspirations
  CRGB::Blue,    // Cues of Reassurance
  CRGB::Brown    // Practicality_Utility
};

void setup() {
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, 500);  // Set max power for safety
  Serial.begin(9600);

  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();
}

void loop() {
  // For now, we're just simulating the serial message, but uncomment this to get the actual message from python
  // if (Serial.available() > 0) {
  // String inputString = Serial.readStringUntil('\n');  // Read the full message


  // Simulate a received serial message
  String inputString = "1,1,1,0,1,1,0,0";  // Test message
  int selectedColors[8] = { 0 };
  int index = 0;
  char *token = strtok((char *)inputString.c_str(), ",");
  while (token != NULL && index < 8) {
    selectedColors[index] = atoi(token);
    token = strtok(NULL, ",");
    index++;
  }

  // Build an array of only the selected colors
  CRGB availableColors[8];
  int availableCount = 0;

  for (int i = 0; i < 8; i++) {
    if (selectedColors[i] == 1) {
      availableColors[availableCount] = colors[i];
      availableCount++;
    }
  }

  // If no colors are selected, default to a blank strip
  if (availableCount == 0) {
    fill_solid(leds, NUM_LEDS, CRGB::Black);
    FastLED.show();
    delay(500);
    return;
  }

  // Calculate the current base index for color cycling
  static uint8_t baseIndex = 0;
  static uint8_t trickleStep = 0;

  // Assign colors to each LED group with a trickling effect
  for (int group = 0; group < NUM_LEDS / LED_GROUP_SIZE; group++) {
    // Get the target color for this group
    CRGB targetColor = availableColors[(baseIndex + group) % availableCount];

    // Only change one LED at a time within each group for the trickling effect
    int ledIndex = group * LED_GROUP_SIZE + trickleStep;
    leds[ledIndex] = targetColor;
  }

  // Display the LEDs
  FastLED.show();

  // Increment the trickle step to move to the next LED in each group
  trickleStep++;
  if (trickleStep >= LED_GROUP_SIZE) {
    trickleStep = 0;
    baseIndex++;  // Move to the next color for each group after a full trickle cycle
  }

  delay(TRICKLE_SPEED);  // Controls the speed of the trickling effect
}
