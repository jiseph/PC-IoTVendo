/* How to use a Force sensitive resistor to fade an LED with Arduino
   More info: http://www.ardumotive.com/how-to-use-a-force-sensitive-resistor-en.html 
   Dev: Michalis Vasilakis // Date: 22/9/2015 // www.ardumotive.com  */
   

//Constants:
const int ledPin = 3;     //pin 3 has PWM funtion
const int sensorPin = A0; //pin A0 to read analog input
//Variables:
int value; //save analog value
const int buzzer = 9; //buzzer to arduino pin 9


void setup(){
  
  pinMode(ledPin, OUTPUT);  //Set pin 3 as 'output' 
  Serial.begin(9600);       //Begin serial communication
  pinMode(buzzer, OUTPUT); // Set buzzer - pin 9 as an output

}

void loop(){
  
  value = analogRead(sensorPin);       //Read and save analog value from potentiometer
  if (value >= 60)
  {
    Serial.println(value);
    noTone(buzzer);     // Stop sound...
  }
  else if (value <= 60)//Print value
  {
    Serial.println(value);
    tone(buzzer, 1000); // Send 1KHz sound signal...
  }
  value = map(value, 0, 1023, 0, 255); //Map value 0-1023 to 0-255 (PWM)
  analogWrite(ledPin, value);          //Send PWM value to led
  delay(300);
}

