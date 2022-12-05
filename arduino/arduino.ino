#include <SoftwareSerial.h>
#include <dht.h>

// NodeMCU
const byte rxPin = 5;
const byte txPin = 6;
String str;
SoftwareSerial espSerial(rxPin, txPin);

// Sensor de luminosidad
#define LDR A0
#define G_LED 2
float ldrInput;

// Sensor de temperatura
#define TEMP_SENSOR 12
#define R_LED 4
float tempInput;
dht DHT;

// Sensor de gas
#define GAS_SENSOR A2
#define LED 8
float gasInput;

// Sensor de movimiento
#define PIR 13
#define Y_LED 7
boolean pirInput;


void setup() {
  Serial.begin(9600);
  espSerial.begin(115200);
  pinMode(G_LED, OUTPUT);
  pinMode(R_LED, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(Y_LED, OUTPUT);
  pinMode(PIR, INPUT);
} 


void send(float ldrInput, float tempInput, float gasInput, float pirInput) {
  str = "ldrInput=" + String(ldrInput) + "&tempInput=" + String(tempInput) + "&gasInput=" + String(gasInput) + "&pirInput=" + String(pirInput);
  espSerial.println(str);
}

float light() {
    ldrInput = analogRead(LDR);

  if(ldrInput >= 600) {
    digitalWrite(G_LED, HIGH);
  }else {
    digitalWrite(G_LED, LOW);
  }

  return ldrInput;
}

float temperature() {
    int chk = DHT.read11(TEMP_SENSOR);

    switch(chk) {
        case DHTLIB_OK:
            Serial.print("OK,\t");
            break;
        case DHTLIB_ERROR_CHECKSUM:
            Serial.print("Checksum error,\t");
            break;
        case DHTLIB_ERROR_TIMEOUT:
            Serial.print("Time out error,\t");
            break;
        case DHTLIB_ERROR_CONNECT:
            Serial.print("Connect error,\t");
            break;
        case DHTLIB_ERROR_ACK_L:
            Serial.print("Ack Low error,\t");
            break;
        case DHTLIB_ERROR_ACK_H:
            Serial.print("Ack High error,\t");
            break;
        default:
            Serial.print("Unknown error,\t");
            break;
    }

    //Serial.println(DHT.temperature, 1);

    return DHT.temperature;
}

float gas() {
    gasInput = analogRead(GAS_SENSOR);
  
    if(gasInput > 600){
        digitalWrite(LED, HIGH);
    }else{
        digitalWrite(LED,LOW);
    }

    return gasInput;
}

boolean movement() {
  pirInput = digitalRead(PIR);

  if(pirInput == HIGH){
    digitalWrite(Y_LED, HIGH);
  }else{
    digitalWrite(Y_LED,LOW);
  }

  return pirInput;
}


void loop() {
    ldrInput = light();
    Serial.print("ADC Arduino (Nivel de luz): ");
    Serial.println(ldrInput);
    delay(500);

    Serial.println();

    tempInput = temperature();
    Serial.print("Temperatura: ");
    Serial.println(tempInput, 1);
    delay(500);

    Serial.println();

    gasInput = gas();
    Serial.print("Gas (?): ");
    Serial.println(gasInput);
    delay(500);

    Serial.println();

    pirInput = movement();
    Serial.print("Movimiento: ");
    Serial.println(pirInput);
    delay(500);

    delay(1000);
    send(ldrInput, tempInput, gasInput, pirInput);

    Serial.println("------");
}
