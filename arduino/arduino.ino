#include <LiquidCrystal.h>

LiquidCrystal lcd(2,3,4,5,7,8);

String current = "Welcome {user} to {club name} club!";
String temp = "";

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(10);
  lcd.begin(16,1);
  lcd.print(current); 
}

void loop() {  
  while (Serial.available()) {
    current = Serial.readString();
    Serial.print(current);
    lcd.clear();
    lcd.print(current);
  }
  
  delay(250);
  lcd.scrollDisplayLeft();
}
