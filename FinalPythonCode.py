import time
import speech_recognition as sr
import serial

PORT = "COM5"
BAUD_RATE = 9600
arduino = serial.Serial(PORT, BAUD_RATE)


def get_voice_input(prompt: str) -> str | None:
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        print(prompt)
        audio = recognizer.listen(mic)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("I didn't catch that. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Could not understand. Please try again. (Error: {e})")
        return None


def get_time_input() -> int:
    while True:
        voice_text = get_voice_input("How long would you like the fan to stay on? (in seconds): ")
        if voice_text and voice_text.isdigit():
            return int(voice_text)
        else:
            print("Please say a whole number in seconds.")


def main():
    print("Listening for Arduino messages. Say 'exit' to quit.")
    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode("utf-8").strip()
            print(f"Arduino says: {line}")
            if line == "LED_ON":
                print("LED is now ON.")
                seconds = get_time_input()
                print(f"Time set for {seconds} seconds.")
                arduino.write("YES\n".encode())
                time.sleep(seconds)
                arduino.write("NO\n".encode())
                print("Time is up! Fan off.")
            elif line == "LED_OFF":
                print("LED is now OFF.")
            else:
                print(f"Unknown message: {line}")
        else:
            time.sleep(0.1)


arduino_code = r"""
const int ledPin = 13;
const int fanPin = 12;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(fanPin, OUTPUT);
  Serial.println("LED_ON");
}

void loop() {}
"""


def save_arduino_code(filename: str = "fan_controller.ino"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(arduino_code)
    print(f"Arduino code saved to {filename}")


if __name__ == "__main__":
    main()
