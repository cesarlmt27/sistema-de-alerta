#include <ESP8266WiFi.h>

String ssid = "";
String password = "";

byte counter = 0;
byte limit = 20;

void setup() {
  Serial.begin(9600);
  Serial.println();

  WiFi.begin(ssid, password);

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

void loop() {}
