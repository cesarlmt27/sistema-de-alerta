//Código de la simulación en Tinkercad

#define PIR 13
#define Y_LED 7
boolean pirInput;

void setup() {
    Serial.begin(9600);
    pinMode(Y_LED, OUTPUT);
    pinMode(PIR, INPUT);
}

void loop() {
  pirInput = digitalRead(PIR);

  if(pirInput == HIGH){
    digitalWrite(Y_LED, HIGH);
    Serial.println(pirInput);
  }else{
    digitalWrite(Y_LED,LOW);
    Serial.println(pirInput);
  }
}
