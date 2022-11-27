#include <dht.h>

#define TEMP_SENSOR 12
#define R_LED 4
dht DHT;

void setup() {
  Serial.begin(9600);
  pinMode(R_LED, OUTPUT);
}

void loop() {
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

  Serial.print(DHT.humidity, 1);
  Serial.print(",\t");
  Serial.println(DHT.temperature, 1);

  delay(2000);
}
