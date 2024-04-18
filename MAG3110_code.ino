#include <Wire.h>
#include <SPI.h>
#include <RF22.h>
#include <RF22Router.h>

#define MY_ADDRESS 1 // define my unique address
#define DESTINATION_ADDRESS_1 2 // define who I can talk to
#define DESTINATION_ADDRESS_2 3 // define who I can talk to
#define MAG_ADDR  0x0E //7-bit address for the MAG3110, doesn't change
RF22Router rf22(MY_ADDRESS); // initiate the class to talk to my radio with MY_ADDRESS
int number_of_bytes=0; // will be needed to measure bytes of message

float throughput=0; // will be needed for measuring throughput
int flag_measurement=0;

int counter=0;
int initial_time=0;
int final_time=0;

// named constant for the pin the sensor is connected to
const int sensorPin = A0; // will be needed to measure something from pin A0

void setup()
{
  Wire.begin();        // join i2c bus (address optional for master)
  Serial.begin(9600);  // start serial for output
  config();            // turn the MAG3110 on
    Serial.begin(9600); // to be able to view the results in the computer's monitor
  if (!rf22.init()) // initialize my radio
    Serial.println("RF22 init failed");
  // Defaults after init are 434.0MHz, 0.05MHz AFC pull-in, modulation FSK_Rb2_4Fd36
  if (!rf22.setFrequency(434.0)) // set the desired frequency
    Serial.println("setFrequency Fail");
  rf22.setTxPower(RF22_TXPOW_20DBM); // set the desired power for my transmitter in dBm
  //1,2,5,8,11,14,17,20 DBM
  rf22.setModemConfig(RF22::OOK_Rb40Bw335  ); // set the desired modulation
  //modulation

  // Manually define the routes for this network
  rf22.addRouteTo(DESTINATION_ADDRESS_1, DESTINATION_ADDRESS_1); // tells my radio card that if I want to send data to DESTINATION_ADDRESS_1 then I will send them directly to DESTINATION_ADDRESS_1 and not to another radio who would act as a relay
  for(int pinNumber = 4; pinNumber<6; pinNumber++) // I can use pins 4 to 6 as digital outputs (in the example to turn on/off LEDs that show my status)
  {
    pinMode(pinNumber,OUTPUT);
    digitalWrite(pinNumber, LOW);
  }
  delay(1000); // delay for 1 s
}

void loop()
{
  print_values();
  counter=0;
  initial_time=millis();
  int sensorVal = analogRead(sensorPin); // measure something
  Serial.print("My measurement is: ");
  Serial.println(sensorVal); // and show it on Serial

// the following variables are used in order to transform my integer measured value into a uint8_t variable, which is proper for my radio
  char data_read[RF22_ROUTER_MAX_MESSAGE_LEN];
  uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
  memset(data_read, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  memset(data_send, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);    
  sprintf(data_read, "%d", sensorVal); // I'm copying the measurement sensorVal into variable data_read
  data_read[RF22_ROUTER_MAX_MESSAGE_LEN - 1] = '\0'; 
  memcpy(data_send, data_read, RF22_ROUTER_MAX_MESSAGE_LEN); // now I'm copying data_read to data_send
  number_of_bytes=sizeof(data_send); // I'm counting the number of bytes of my message
  Serial.print("Number of Bytes= ");
  Serial.println(number_of_bytes);  // and show the result on my monitor

  // just demonstrating that the string I will send, after those transformation from integer to char and back remains the same
  int sensorVal2=0;
  sensorVal2=atoi(data_read);
  Serial.print("The string I'm ready to send is= ");
  Serial.println(sensorVal2);
  if (rf22.sendtoWait(data_send, sizeof(data_send), DESTINATION_ADDRESS_1) != RF22_ROUTER_ERROR_NONE) // I'm sending the data in variable data_send to DESTINATION_ADDRESS_1... cross fingers
  {
    Serial.println("sendtoWait failed"); // for some reason I have failed
  }
  else
  {
    counter=counter+1;
    Serial.println("sendtoWait Successful"); // I have received an acknowledgement from DESTINATION_ADDRESS_1. Data have been delivered!
  }
  final_time=millis();
  throughput=(float)counter*number_of_bytes*1000.0/(final_time-initial_time); // *1000 is because time is measured in ms. This is not the communication throughput, but rather each measurement-circle throughput.
  Serial.print("Throughput=");
  Serial.print(throughput);
  Serial.println("Bytes/s");
  Serial.print("Initial time= ");  
  Serial.print(initial_time);
  Serial.print("     Final time= ");  
  Serial.println(final_time);

  delay(500);
}

void config(void)
{
  Wire.beginTransmission(MAG_ADDR); // transmit to device 0x0E
  Wire.write(0x11);             // cntrl register2
  Wire.write(0x80);             // write 0x80, enable auto resets
  Wire.endTransmission();       // stop transmitting
  delay(15); 
  Wire.beginTransmission(MAG_ADDR); // transmit to device 0x0E
  Wire.write(0x10);             // cntrl register1
  Wire.write(1);                // write 0x01, active mode
  Wire.endTransmission();       // stop transmitting
}

void print_values(void)
{
  Serial.print("x=");
  Serial.print(read_x());
  Serial.print(",");  
  Serial.print("y=");    
  Serial.print(read_y());
  Serial.print(",");       
  Serial.print("z=");    
  Serial.println(read_z());
}

int mag_read_register(int reg)
{
  int reg_val;
  
  Wire.beginTransmission(MAG_ADDR); // transmit to device 0x0E
  Wire.write(reg);              // x MSB reg
  Wire.endTransmission();       // stop transmitting
  delayMicroseconds(2); //needs at least 1.3us free time between start and stop
  
  Wire.requestFrom(MAG_ADDR, 1); // request 1 byte
  while(Wire.available())    // slave may write less than requested
  { 
    reg_val = Wire.read(); // read the byte
  }
  
  return reg_val;
}

int mag_read_value(int msb_reg, int lsb_reg)
{
  int val_low, val_high;  //define the MSB and LSB
  val_high = mag_read_register(msb_reg);
  delayMicroseconds(2); //needs at least 1.3us free time between start and stop
  val_low = mag_read_register(lsb_reg);
  int out = (val_low|(val_high << 8)); //concatenate the MSB and LSB
  return out;
}

int read_x(void)
{
  return mag_read_value(0x01, 0x02);
}

int read_y(void)
{
  return mag_read_value(0x03, 0x04);
}

int read_z(void)
{
  return mag_read_value(0x05, 0x06);
}