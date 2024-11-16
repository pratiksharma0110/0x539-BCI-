#define fp1_pin A0
#define fp2_pin A1

#define GAIN 10



void setup(){

  Serial.begin(115200);

}
  
void loop(){
  float fp1 = analogRead(fp1_pin);
  float fp2 = analogRead(fp2_pin);

  float cmmr = (fp1 - fp2) * GAIN;
  
  Serial.println(cmmr);
  

  if (Serial.available()) {
    String command = Serial.readStringUntil('\n'); 

    if (command == "HIGH") {
      digitalWrite(10, HIGH);
    } else if (command == "LOW") {
      digitalWrite(10, LOW); 
    }
  }
}


