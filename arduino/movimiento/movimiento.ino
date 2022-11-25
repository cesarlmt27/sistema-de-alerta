//Código de la simulación en Tinkercad

#define PIR 13
#define LED 7
boolean pirInput;

void setup() {
    Serial.begin(9600);
    pinMode(LED, OUTPUT);
    pinMode(PIR, INPUT);
}

void loop() {
  pirInput = digitalRead(PIR);

  if(pirInput == HIGH){
    digitalWrite(LED, HIGH);
    Serial.println(pirInput);
  }else{
    digitalWrite(LED,LOW);
    Serial.println(pirInput);
  }
}
