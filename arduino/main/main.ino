#include "motors.h"
#include "setupPins.h"
#include "ledControl.h"

// Define app states
enum AppState {
    Idle = 0,
    Recording = 1,
    Playback = 2
};

AppState appState = Idle; // Initial app state

void setup() {
    Serial.begin(9600);
    setupPins();    // Initialize motor pins
    setupLEDs();    // Initialize LEDs
}

void loop() {
    // Check for a serial message
    if (Serial.available() > 0) {
        String inputString = Serial.readStringUntil('\n'); // Read the full message

        // Set the app state to Playback and update LEDs
        appState = Playback;
        updateLEDs(inputString);
    }

    switch (appState) {
        case Idle:
            warmGlowEffect();
            break;

        case Recording:
            recordingAnimation();
            break;

        case Playback:
            // TODO: other playback behaviors
            break;
    }
}
