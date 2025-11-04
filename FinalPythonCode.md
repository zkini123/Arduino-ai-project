import time
import speech_recognition as sr
import serial




port = "COM5"
baud_rate = 9600
arduino = serial.Serial(port, baud_rate)


def get_voice_input(prompt):
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
            print(prompt)
            audio = recognizer.listen(mic)
    try:
        text = recognizer.recognize_google(audio)
        print(f"{text} seconds. ")
        return text
    except sr.UnknownValueError:
        print(f"I didn't catch that. Please try again. ")
        return None
    except sr.RequestError as e:
        print("Could not understand. Please try again; {0}".format(e))
        return None




def get_time_input():
    while True:
        voice_text = get_voice_input("How long would you like the fan to stay on? (in seconds): ")
        if voice_text and voice_text.isdigit():
            return int(voice_text)
        else:
            print(f"Please say a number in seconds.")




def main():
    print("Listening for Arduino messages. Say 'exit' to quit.")
    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()
            if line == "LED_ON":
                print("LED is now on")
                seconds = get_time_input()
                print(f"Time set for {seconds} seconds.")
                arduino.write(f"YES\n".encode())
                time.sleep(seconds)
                arduino.write(f"NO\n".encode())
                print(f"Time is up!")
                # again = get_voice_input("Would you like the fan to stay on? (yes/no or exit): ")
                # if not again or again.strip().lower() == 'exit':
                #     print("Exiting program.")
                #     break
                # if again.strip().upper() == 'yes':
                #     arduino.write(again.encode())
                #     print("Fan turning off. Goodbye! ")
            elif line == "LED_OFF":
                print("LED is now OFF")
            else:
                print(f"Unknown message: {line}")
        else:
            time.sleep(0.1)




if __name__ == "__main__":
    main()
