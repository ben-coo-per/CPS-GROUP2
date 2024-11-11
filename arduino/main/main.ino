#include "motors.h"
#include "ledControl.h"

// Define app states
enum AppState {
    Idle = 0,
    Recording = 1,
    Playback = 2
};

AppState appState = Idle; // Initial app state

String LEDLightInputString = ""; // String to hold the LED light input

void setup() {
    Serial.begin(9600);
    setupMotor();
    setupLEDs();
}

void loop() {
    // Check for a serial message
    if (Serial.available() > 0) {
        LEDLightInputString = Serial.readStringUntil('\n'); // Read the full message

        // Set the app state to Playback and update LEDs
        updateLEDs(LEDLightInputString);
        appState = Playback;
    }

    switch (appState) {
        case Idle:
            warmGlowEffect();
            break;

        case Recording:
            recordingAnimation();
            break;

        case Playback:
            updateLEDs(LEDLightInputString);
            break;
    }
}
