#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include "networkData.h"

String data;

WiFiClient client;
HTTPClient http;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println();

  WiFi.begin(ssid, password); // "ssid" y "password" son String que están declarados en "networkData.h"

  Serial.print("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  
  Serial.print("Connected to: ");
  Serial.println(WiFi.SSID());

  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  Serial.print("MAC Address: ");
  Serial.println(WiFi.macAddress());

}


void receive() {
  if(Serial.available()) {
    data = Serial.readString();
    data = data + "&serialInput=" + String(WiFi.macAddress());
    send(data);
  }
}

void send(String data) {
  if(WiFi.status() == WL_CONNECTED) {
    http.begin(client, host);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    
    int responseCode = http.POST(data);

    Serial.println(data);

    if(responseCode > 0 || responseCode == -11) {
      digitalWrite(LED_BUILTIN, LOW);
      Serial.print("HTTP Response code: ");
      Serial.println(responseCode);
      String payload = http.getString();
      Serial.println(payload);
    }else {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.print("Error code: ");
      Serial.println(responseCode);
    }
    
    http.end();

  }else {
    Serial.println("Wi-Fi Disconnected");
  }
}


void loop() {
  if(WiFi.status() == WL_CONNECTED) {
    delay(1000);
    receive();
  }else {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("Wi-Fi Disconnected");
    delay(2000);
  }  
}
