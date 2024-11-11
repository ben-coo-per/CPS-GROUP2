#include "motors.h"
#include <Arduino.h>

void setupMotor() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  digitalWrite(ENA, HIGH);  // Enable motor
}

void rampUpRampDown() {
    static int pwmValue = 150;  // Start with a higher initial value to jump-start the motor
    static bool rampingUp = true;
    static unsigned long previousMotorMillis = 0;
    const int motorDelay = 100;  // Time between each step

    // Check if enough time has passed for the next motor step
    if (millis() - previousMotorMillis >= motorDelay) {
        previousMotorMillis = millis();

        // Increase or decrease PWM value based on ramping direction
        if (rampingUp) {
            pwmValue += 5;
            if (pwmValue >= 255) {
                rampingUp = false;  // Switch to ramping down
            }
        } else {
            pwmValue -= 5;
            if (pwmValue <= 50) {
                rampingUp = true;  // Switch to ramping up
            }
        }

        // Apply PWM value to motor
        analogWrite(IN1, pwmValue);
        digitalWrite(IN2, LOW);
    }
}
