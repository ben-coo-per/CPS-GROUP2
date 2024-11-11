#include <math.h>
#include "ledControl.h"

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

int selectedColors[8] = { 0 };

void setupLEDs() {
    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
    FastLED.setMaxPowerInVoltsAndMilliamps(5, 500);  // Set max power for safety
    fill_solid(leds, NUM_LEDS, CRGB::Black);
    FastLED.show();
}

void warmGlowEffect() {
    static unsigned long previousMillis = 0;
    static int offset = 0; // Offset for color movement
    const int glowSpeed = 50; // Interval for brightness update
    const int movementSpeed = 200; // Interval for moving the color blobs
    const int groupSize = 10;

    // Calculate brightness using a sine wave for a 10-second cycle
    float time = millis() / 10000.0; // Time in seconds, scaled for 10s cycle
    uint8_t brightness = (sin(time * 2 * PI) + 1) * 122.5 + 10; // Range 10-255

    // Apply the calculated brightness to FastLED
    FastLED.setBrightness(brightness);

    // Define warm colors for the effect
    CRGB warmColor1 = CRGB(255, 150, 50);  // Soft orange
    CRGB warmColor2 = CRGB(255, 200, 100); // Warm yellow
    CRGB warmColor3 = CRGB(255, 240, 200); // Off-white

    // Check if it's time to update the LEDs
    if (millis() - previousMillis >= glowSpeed) {
        previousMillis = millis();

        // Fill the LEDs with groups of colors, using the offset for movement
        int groupSize = 5; // Number of LEDs per color "blob"
        for (int i = 0; i < NUM_LEDS; i++) {
            // Cycle through color blobs with an offset
            int colorIndex = (i + offset) / groupSize;
            if (colorIndex % 3 == 0) {
                leds[i] = warmColor1;
            } else if (colorIndex % 3 == 1) {
                leds[i] = warmColor2;
            } else {
                leds[i] = warmColor3;
            }
        }

        // Display the LEDs with the adjusted brightness
        FastLED.show();
    }

    // Move the color blobs subtly over time
    static unsigned long previousMovementMillis = 0;
    if (millis() - previousMovementMillis >= movementSpeed) {
        previousMovementMillis = millis();
        offset = (offset + 1) % (groupSize * 3); // Loop the offset within blob cycle
    }
}

void recordingAnimation() {
    static unsigned long previousMillis = 0;
    const int animationSpeed = 30; // Speed of animation for pulsing effect

    // Color for the recording effect
    CRGB recordingColor = CRGB::Red;
    CRGB backgroundColor = CRGB(30, 0, 0); // Dark red as the background color

    // Simulated "level" effect parameters
    static int level = 0;
    static int levelDirection = 1; // 1 for expanding, -1 for contracting
    const int maxLevel = NUM_LEDS / 2; // Maximum level to light up (half the strip)

    // Check if it's time to update the animation
    if (millis() - previousMillis >= animationSpeed) {
        previousMillis = millis();

        // Update the "level" to create a bouncing effect
        level += levelDirection;
        if (level >= maxLevel || level <= 0) {
            levelDirection = -levelDirection; // Reverse direction at bounds
        }

        // Set background color for the entire strip
        fill_solid(leds, NUM_LEDS, backgroundColor);

        // Light up LEDs from the center outward based on the "level"
        for (int i = 0; i < level; i++) {
            leds[NUM_LEDS / 2 + i] = recordingColor; // Right side from center
            leds[NUM_LEDS / 2 - i] = recordingColor; // Left side from center
        }

        // Display the LEDs
        FastLED.show();
    }
}

// LED updates from wek values
void updateLEDs(String inputString) {
    static uint8_t baseIndex = 0;
    static uint8_t trickleStep = 0;
    static unsigned long previousLEDMillis = 0;

    const int ledUpdateInterval = TRICKLE_SPEED;

    // Parse the input string only if there is new data
    if (inputString.length() > 0) {
        int index = 0;
        char *token = strtok((char *)inputString.c_str(), ",");
        while (token != NULL && index < 8) {
            selectedColors[index] = atoi(token);
            token = strtok(NULL, ",");
            index++;
        }
    }

    // Check if it's time to update the LEDs
    if (millis() - previousLEDMillis >= ledUpdateInterval) {
        previousLEDMillis = millis();

        // Create an array of selected colors
        CRGB availableColors[8];
        int availableCount = 0;

        for (int i = 0; i < 8; i++) {
            if (selectedColors[i] == 1) {
                availableColors[availableCount] = colors[i];
                availableCount++;
            }
        }

        // If no colors are selected, clear the LEDs
        if (availableCount == 0) {
            fill_solid(leds, NUM_LEDS, CRGB::Black);
            FastLED.show();
            return;
        }

        // Assign colors to each LED group with a trickling effect
        for (int group = 0; group < NUM_LEDS / LED_GROUP_SIZE; group++) {
            CRGB targetColor = availableColors[(baseIndex + group) % availableCount];
            int ledIndex = group * LED_GROUP_SIZE + trickleStep;
            leds[ledIndex] = targetColor;
        }

        FastLED.show();

        // Update trickle step and base index
        trickleStep++;
        if (trickleStep >= LED_GROUP_SIZE) {
            trickleStep = 0;
            baseIndex++;
        }
    }
}