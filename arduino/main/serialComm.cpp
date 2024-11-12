#include "serialComm.h"
#include "appState.h" // Include the appState definitions
#include <Arduino.h>

void setupSerial() {
    Serial.begin(9600); // Initialize serial communication
}

void checkSerialInput() {
    if (Serial.available() > 0) {
        String inputString = Serial.readStringUntil('\n');
        
        if (inputString.startsWith("app_state:")) {
            int newState = inputString.substring(10).toInt();
            if (newState >= 0 && newState <= 2) {
                appState = static_cast<AppState>(newState);
            }
        }

        if (inputString.startsWith("lights:")) {
          inputString = inputString.substring(7); // Remove "lights:" prefix
          lightPattern = static_cast<String>(inputString);
        }
    }
}
