#include "buttonControl.h"
#include <Arduino.h>

const int buttonPin = 2; // The pin connected to the button
int buttonState = HIGH;  // Current state of the button
int lastButtonState = HIGH; // Previous state of the button

void setupButton() {
    pinMode(buttonPin, INPUT_PULLUP); // Set button pin as input with pull-up resistor
}

void checkButton() {
    // Read the button's state
    buttonState = digitalRead(buttonPin);

    // Check if the button state has changed
    if (buttonState != lastButtonState) {
        if (buttonState == LOW) {
            // Button is pressed
            Serial.println("btn_start");
        } else {
            // Button is released
            Serial.println("btn_stop");
        }

        // Update the lastButtonState to the current state
        lastButtonState = buttonState;
    }

    delay(10); // Small delay to debounce the button
}
