import time
import speech_recognition as sr
import serial


# --------------------- SERIAL SETUP ---------------------


port = "COM4"
baud_rate = 9600
arduino = serial.Serial(port, baud_rate)
time.sleep(2)  # let Arduino reset




# --------------------- VOICE INPUT ----------------------


def get_voice_input(prompt):
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        print(prompt)
        audio = recognizer.listen(mic)


    try:
        text = recognizer.recognize_google(audio)
        print(f"Heard: {text}")
        return text
    except sr.UnknownValueError:
        print("I didn't catch that. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Could not understand. Error: {e}")
        return None




# --------------------- TIME PARSER ----------------------


def parse_time_input(text):
    text = text.lower().strip()


    # Fix common hearing mistakes
    text = text.replace("for", "four")
    text = text.replace("to ", "two ")
    text = text.replace("too ", "two ")


    number_words = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
        "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
        "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
        "fifty": 50
    }


    # Replace number words with digits
    for word, val in number_words.items():
        text = text.replace(word, f" {val} ")


    # Extract all digits
    nums = [int(x) for x in text.split() if x.isdigit()]


    minutes = 0
    seconds = 0


    # Minutes + seconds
    if "minute" in text and "second" in text:
        if len(nums) >= 1:
            minutes = nums[0]
        if len(nums) >= 2:
            seconds = nums[1]


    # Minutes only
    elif "minute" in text:
        if len(nums) >= 1:
            minutes = nums[0]


    # Seconds only
    elif "second" in text:
        if len(nums) >= 1:
            seconds = nums[0]


    # Just a number (“8”, “15”)
    elif len(nums) == 1:
        seconds = nums[0]


    return minutes * 60 + seconds




# --------------------- GET TIME INPUT ----------------------


def get_time_input():
    while True:
        voice_text = get_voice_input("How long would you like the fan to stay on?")
        if voice_text:
            total_seconds = parse_time_input(voice_text)


            if total_seconds > 0:
                # Convert back to readable format
                minutes = total_seconds // 60
                seconds = total_seconds % 60


                if minutes > 0 and seconds > 0:
                    readable = f"{minutes} minute{'s' if minutes != 1 else ''} {seconds} second{'s' if seconds != 1 else ''}"
                elif minutes > 0:
                    readable = f"{minutes} minute{'s' if minutes != 1 else ''}"
                else:
                    readable = f"{seconds} second{'s' if seconds != 1 else ''}"


                print(f"Time set for {readable}.")
                return total_seconds


            else:
                print("I couldn't understand the time. Please try again.")




# --------------------- MAIN LOOP ----------------------


def main():
    print("Listening for Arduino messages. Say 'exit' to quit.")


    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()


            if line == "LED_ON":
                print("LED is now ON")


                seconds = get_time_input()


                # Start the fan
                arduino.write("YES\n".encode())
                time.sleep(seconds)
                arduino.write("NO\n".encode())


                print("Time is up!")


            elif line == "LED_OFF":
                print("LED is now OFF")


            else:
                print(f"Unknown message: {line}")
        else:
            time.sleep(0.1)




if __name__ == "__main__":
    main()
    