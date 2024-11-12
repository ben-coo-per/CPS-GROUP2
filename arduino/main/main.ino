#include "motors.h"
#include "ledControl.h"
#include "buttonControl.h"
#include "serialComm.h"
#include "appState.h" // Include the appState definitions

AppState appState = Idle; // Define the main appState variable here
String lightPattern = "";

void setup() {
    Serial.begin(9600);
    setupMotor();
    setupLEDs();
    setupButton();
    setupSerial(); // Initialize serial communication
}

void loop() {
    checkButton();      // Check button state changes
    checkSerialInput(); // Check for serial messages to update app state

    // Perform actions based on app state
    switch (appState) {
        case Idle:
            warmGlowEffect();
            break;

        case Recording:
            recordingAnimation();
            break;

        case Playback:
            delay(100);
            updateLEDs(lightPattern);
            break;
    }
}
