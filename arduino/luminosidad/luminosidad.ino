#define LDR A0
#define G_LED 2
float ldrInput;

void setup() {
  Serial.begin(9600);
  pinMode(G_LED, OUTPUT);
} 
 
void loop() {
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
