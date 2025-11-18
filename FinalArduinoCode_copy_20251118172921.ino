#include <DHT.h>




const int motorIn1 = 9;  
const int motorIn2 = 10;




// --- Pin setup ---
#define LED_PIN 8
#define BUTTON_PIN 2
#define DHT_PIN 4
#define DHT_TYPE DHT11       // Change to DHT22 if needed




// --- Globals ---
DHT dht(DHT_PIN, DHT_TYPE);




bool tempControlEnabled = false;  // Start OFF
float tempThreshold = 35.0;       // Temperature threshold in °C




bool ledState = false;
bool lastButtonState = LOW;
unsigned long lastDebounceTime = 0;
const unsigned long debounceDelay = 50;
int reading = 0;




void setup() {
  pinMode(motorIn1,OUTPUT);
  pinMode(motorIn2,OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);
  Serial.begin(9600);
  dht.begin();




  digitalWrite(LED_PIN, LOW);
  stopFan();




  Serial.println("Temperature Control System Ready.");
  Serial.println("Press button to toggle ON/OFF.");
}




void loop() {
  reading = digitalRead(BUTTON_PIN);
 
    //button stuff
    if (reading == HIGH && lastButtonState == LOW) {
      ledState = !ledState;
      Serial.println(ledState);




      if (ledState == HIGH) {
        stopFan();
        digitalWrite(LED_PIN, HIGH);
        Serial.println("LED_ON");
      } else {
        digitalWrite(LED_PIN, LOW);
        stopFan();
        Serial.println("LED_OFF");
      }
    }
    lastButtonState = reading;




  //fan stuff
  if (Serial.available() > 0) {
    String pyResponse = Serial.readStringUntil('\n');
    if (ledState == HIGH && pyResponse == "YES"){
      fanON();
    }
    if (ledState == HIGH && pyResponse == "NO"){
      stopFan();
    }
  }
 
  if (ledState == LOW) {
    tempControlEnabled = !tempControlEnabled;
    temp();
  }




}




void fanON() {
  analogWrite(motorIn1, 200);  //set the speed of motor
  analogWrite(motorIn2,0);  //stop the motorIn2 pin of motor
}




void stopFan() {
  analogWrite(motorIn1, 0);
  analogWrite(motorIn2, 0);
}




void temp() {
  // --- Read temperature ---
  float temp = dht.readTemperature();
  if (isnan(temp)) {
    Serial.println("Error: Cannot read from DHT sensor!");
  } else {
    Serial.print("Temperature: ");
    Serial.print(temp);
    Serial.println(" °C");








    // --- Control logic ---
    if (tempControlEnabled && temp >= tempThreshold) {
      Serial.println("LED ON (Temp above threshold)");
      fanON();
    }
    else {  
      if (tempControlEnabled) {
        Serial.println("LED OFF (Temp below threshold)");
        stopFan();
      }
    }
  }
  delay(2000);
}
