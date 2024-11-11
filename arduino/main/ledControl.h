#ifndef LEDCONTROL_H
#define LEDCONTROL_H

#include <FastLED.h>

#define NUM_LEDS 100
#define DATA_PIN 5
#define LED_GROUP_SIZE 10  // Number of LEDs per color group
#define TRICKLE_SPEED 100  // Speed of the trickle effect in milliseconds

extern CRGB leds[NUM_LEDS];

// Function declarations
void setupLEDs();
void updateLEDs(String inputString);
void warmGlowEffect();
void recordingAnimation();

#endif
