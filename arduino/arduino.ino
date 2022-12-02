#include <dht.h>

// Sensor de luminosidad
#define LDR A0
#define G_LED 2
float ldrInput;

// Sensor de temperatura
#define TEMP_SENSOR 12
#define R_LED 4
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
  pinMode(G_LED, OUTPUT);
  pinMode(R_LED, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(Y_LED, OUTPUT);
  pinMode(PIR, INPUT);
} 


void light() {
    ldrInput = analogRead(LDR);

  if(ldrInput >= 600) {
    digitalWrite(G_LED, HIGH);
    Serial.println("LED ON");
    Serial.println(ldrInput);
  }else {
    digitalWrite(G_LED, LOW);
    Serial.println("LED OFF");
    Serial.println(ldrInput);
  }
  delay(1000);
}

void temperature() {
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

  Serial.println(DHT.temperature, 1);

  delay(2000);
}

void gas() {
    gasInput = analogRead(GAS_SENSOR);
    Serial.println(gasInput);
  
    if(gasInput > 600){
        digitalWrite(LED, HIGH);
    }else{
        digitalWrite(LED,LOW);
    }

    delay(500);
}

void movement() {
  pirInput = digitalRead(PIR);

  if(pirInput == HIGH){
    digitalWrite(Y_LED, HIGH);
    Serial.println(pirInput);
  }else{
    digitalWrite(Y_LED,LOW);
    Serial.println(pirInput);
  }
}


void loop() {
    temperature();
    light();
}
