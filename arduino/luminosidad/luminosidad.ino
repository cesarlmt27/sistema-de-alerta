void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);
  pinMode(4, OUTPUT);
} 
 
void loop() {
  int valorLDR = analogRead(A0);

  if(valorLDR >= 600) {
    digitalWrite(4, HIGH);
    Serial.print("LED ON");
    Serial.println(valorLDR);
    delay(1000);
  }
  
  else {
    digitalWrite(4, LOW);
    Serial.println("LED OFF");
    Serial.println(valorLDR);
    delay(1000);
  }
}
