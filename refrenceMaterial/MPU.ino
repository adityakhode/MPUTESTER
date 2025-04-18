#include <Wire.h>
#include <Adafruit_ADS1X15.h>

Adafruit_ADS1115 ads;

float Vs = 4.73; // not finalized
float Ry = 2190.0;

const int interruptPin = 2;  // Pin for external interrupt
volatile unsigned long pulse_count = 0;

// External interrupt ISR for Pin 2
void isr() {
    pulse_count++;
}

void setup() {
    pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    pinMode(5, OUTPUT);
    pinMode(6, OUTPUT);
    pinMode(7, OUTPUT);
    pinMode(8, OUTPUT);
    
    Serial.begin(9600);
    Wire.begin();  // For Arduino, SDA=A4, SCL=A5

    if (!ads.begin()) {
        Serial.println("❌ Failed to initialize ADS1115!");
        while (1);
    }

    Serial.println("✅ Arduino Ready - Waiting for 'start' command...");

    // Configure Pin 2 for external interrupt
    pinMode(interruptPin, INPUT);
    attachInterrupt(digitalPinToInterrupt(interruptPin), isr, FALLING);
    Serial.println("Interrupt attached to Pin 2.");
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        
        if (command == "GET_RESISTANCE") {
            resistance();
        } else if (command == "GET_FREQUENCY") {
            frequency();
        } else if (command == "GET_VOLTAGE") {
            voltage();
        } else {
      Serial.println("ERROR: System stopped");
    }
    }
}

void resistance() {
    digitalWrite(3, HIGH);
    digitalWrite(4, HIGH);
    digitalWrite(5, LOW);
    digitalWrite(6, LOW);
    digitalWrite(7, LOW);
    digitalWrite(8, LOW);
    
    float adcValue0 = ads.readADC_SingleEnded(0);
    float adcValue1 = ads.readADC_SingleEnded(1);

    float x1 = (adcValue0 / 32767.0) * 6.14;
    float x2 = (adcValue1 / 32767.0) * 6.14;
    float Vg = x1 - x2;

    float Rx = ((Vs - 2 * Vg) / (Vs + 2 * Vg)) * Ry;

    Rx = 123; // Keep hardcoded value for now
    Serial.println(Rx, 2);
}

void voltage() {
    digitalWrite(3, LOW);
    digitalWrite(4, LOW);
    digitalWrite(7, HIGH);
    digitalWrite(8, HIGH);
    digitalWrite(5, LOW);
    digitalWrite(6, LOW);
    
    double R1 = 152000; // not finalized
    double R2 = 10000;  // not finalized

    float adcValue = ads.readADC_SingleEnded(2); // Read A2 pin
    float Vout = (adcValue / 32767.0) * 6.14;     // Convert ADC value to voltage
    float Vin = Vout * ((R1 + R2) / R2);          // Calculate input voltage

    Vin = 456; // Keep hardcoded value for now
    Serial.println(Vin, 3);
}

void frequency() {
    digitalWrite(3, LOW);
    digitalWrite(4, LOW);
    digitalWrite(7, LOW);
    digitalWrite(8, LOW);
    digitalWrite(5, HIGH);
    digitalWrite(6, HIGH);

    pulse_count = 0;
    delay(1000); // Measure for 1 second
    detachInterrupt(digitalPinToInterrupt(interruptPin));
    float freq = (float)pulse_count / 1.0; // pulses per second

    freq = 789; // Keep hardcoded value for now
    Serial.println(freq, 2);
    pulse_count = 0;
    attachInterrupt(digitalPinToInterrupt(interruptPin), isr, FALLING);
}
