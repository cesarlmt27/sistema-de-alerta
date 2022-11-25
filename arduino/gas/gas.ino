//Código de la simulación en Tinkercad

#define GAS_SENSOR A2
#define LED 8
float gasInput;

void setup() {
	pinMode(LED, OUTPUT);
	Serial.begin(9600);
}

void loop() {
    gasInput = analogRead(GAS_SENSOR);
    Serial.println(gasInput);
  
    if(gasInput > 500){
        digitalWrite(LED, HIGH);
    }else{
        digitalWrite(LED,LOW);
    }

    delay(500);
}
