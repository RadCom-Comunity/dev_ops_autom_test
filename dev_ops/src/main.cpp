#include <Arduino.h>

// put function declarations here:
int myFunction(int, int);

void setup() {
  // put your setup code here, to run once:
  int result = myFunction(2, 3);
}

void loop() {
  int count = 0;
  for (size_t i = 0; i < count; i++)
  {
    Serial.println(i);
  }
  
}

// put function definitions here:
int myFunction(int x, int y) {
  return x + y;
}