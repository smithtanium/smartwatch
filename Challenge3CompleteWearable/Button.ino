#define BUTTON_PIN 14
bool button_state = HIGH; 
unsigned int button_start = millis();

void button_setup() {
  pinMode(BUTTON_PIN, INPUT);
}

bool button_pressed() {
  if (digitalRead(BUTTON_PIN) == LOW && button_state == HIGH) {
    button_start = millis();
    button_state = LOW;
  }
  else if (button_state == LOW && millis() - button_start > 200) {
    button_state = HIGH;
    return true;
  }
  else if (digitalRead(BUTTON_PIN) == HIGH) {
    button_state = HIGH;
  }
  return false;
}
