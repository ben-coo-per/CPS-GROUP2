import serial
import time


class ArduinoSerial:
    def __init__(self, port, baud_rate=9600):
        try:
            self.arduino = serial.Serial(port, baud_rate, timeout=1)
            print(f"Connected to Arduino on port {port}")
        except serial.SerialException:
            print(
                "Could not open serial port. Check if Arduino is connected and the port is correct."
            )
            exit()

    def send_app_state(self, app_state):
        message = f"app_state:{app_state}\n"
        self.arduino.write(message.encode("utf-8"))
        print(f"Sent to Arduino: {message.strip()}")

    def listen_for_button(self, start_recording, stop_recording):
        """Continuously listen for button state changes from Arduino."""
        try:
            while True:
                if self.arduino.in_waiting > 0:
                    line = self.arduino.readline().decode("utf-8").strip()
                    print("Received from Arduino:", line)
                    if line == "btn_start":
                        start_recording()
                    elif line == "btn_stop":
                        stop_recording()
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nButton listener stopped.")

        finally:
            self.arduino.close()
            print("Closed serial connection for button listener.")
