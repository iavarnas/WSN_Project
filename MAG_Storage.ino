#include <SparkFun_MAG3110.h>

MAG3110 mag = MAG3110(); //Instantiate MAG3110

const int maxDataPoints = 100; // Maximum number of data points to store
int xCoordinates[maxDataPoints]; // Array to store X-axis coordinates
int currentIndex = 0; // Index to keep track of the current position in the array

void setup() {
  Serial.begin(9600);//ok

  Wire.begin();             //setup I2C bus
  Wire.setClock(400000);    // I2C fast mode, 400kHz

  mag.initialize(); //Initializes the mag sensor
  mag.start();      //Puts the sensor in active mode          
}

void loop() {

  int x, y, z;
  
  //Only read data when it's ready
  if(mag.dataReady()) {
    //Read the data
    mag.readMag(&x, &y, &z);
    
    // Store the X-axis coordinate
    storeCoordinate(x);
    
    // Check if we've reached the maximum number of data points
    if (currentIndex >= maxDataPoints) {
      printCoordinates(); // Print all gathered coordinates
      currentIndex = 0; // Reset the index
    }
    
    delay(500);
  }
}

void storeCoordinate(int x) {
  // Store the X-axis coordinate in the array if there's still space
  if (currentIndex < maxDataPoints) {
    xCoordinates[currentIndex] = x;
    currentIndex++;
  }
}

void printCoordinates() {
  Serial.println("Stored X-axis coordinates:");
  for (int i = 0; i < maxDataPoints; i++) {
    Serial.print("X");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(xCoordinates[i]);
  }
  Serial.println("--------");
}
