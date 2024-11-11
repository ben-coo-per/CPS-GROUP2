#include "setupPins.h"
#include "pins.h"
#include <Arduino.h>

void setupPins() {
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(ENA, OUTPUT);

    digitalWrite(ENA, HIGH);  // Enable motor
}
