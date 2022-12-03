#include <ESP8266WiFi.h>
#include "myNetwork.h"

byte counter = 0;
byte limit = 20;

void setup() {
  Serial.begin(115200);
  Serial.println();

  WiFi.begin(ssid, password); // "ssid" y "password" son String que están declarados en "myNetwork.h"

  Serial.print("Connecting");
  
  while(WiFi.status() != WL_CONNECTED && counter < limit) {
    counter++;
    delay(500);
    Serial.print(".");  
  }

  Serial.println();
  
  if(counter < limit) {
    Serial.print("Connected to: ");
    Serial.println(WiFi.SSID());

    Serial.print("IP: ");
    Serial.println(WiFi.localIP());

    Serial.print("MAC Address: ");
    Serial.println(WiFi.macAddress());
  }else {
    Serial.print("Connection failed");
  }
}


void receive() {
  if(Serial.available()) {
    Serial.write(Serial.read());
  }

}


void loop() {
  receive();
}
