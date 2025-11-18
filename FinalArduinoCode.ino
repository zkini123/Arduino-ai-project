#include <DHT.h>

// --- Pin setup ---
#define DHT_PIN 4
#define DHT_TYPE DHT11       // Change to DHT22 if needed
#define BUTTON_PIN 5
#define LED_PIN 13           // Built-in LED (test instead of fan)

// --- Globals ---
DHT dht(DHT_PIN, DHT_TYPE);

bool tempControlEnabled = false;  // Start OFF
float tempThreshold = 23.0;       // Temperature threshold in °C
int lastButtonState = HIGH;       // For toggle button

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(BUTTON_PIN, INPUT_PULLUP); 
  pinMode(LED_PIN, OUTPUT);

  Serial.println("Temperature Control System Ready.");
  Serial.println("Press button to toggle ON/OFF.");
}

void loop() {
  // --- Button toggle ---
  int buttonState = digitalRead(BUTTON_PIN);
  if (buttonState == LOW && lastButtonState == HIGH) {
    tempControlEnabled = !tempControlEnabled; 
    Serial.print("Temp Control: ");
    Serial.println(tempControlEnabled ? "ON" : "OFF");
    delay(2000); // debounce
  }
  lastButtonState = buttonState;

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
      digitalWrite(LED_PIN, HIGH); 
      Serial.println("LED ON (Temp above threshold)");
    } else {
      digitalWrite(LED_PIN, LOW);  
      if (tempControlEnabled) {
        Serial.println("LED OFF (Temp below threshold)");
      }
    }
  }

  delay(2000); // Update every 2 seconds
}
