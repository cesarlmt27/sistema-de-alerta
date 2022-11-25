#define TEMP_SENSOR A0
#define R_LED 4
float tempValue;
float tempInput;

void setup() {
  Serial.begin(9600);
  pinMode(R_LED, OUTPUT);
  pinMode(TEMP_SENSOR, INPUT);
}

void loop() {
  tempInput = analogRead(TEMP_SENSOR);
  tempValue = (((5.0/1024.0) * tempInput) * 100.0) - 50.0;

  if(tempValue >= 20) {
   digitalWrite(R_LED, HIGH);
  }else{
    digitalWrite(R_LED, LOW);
  }
  delay(500);
}
