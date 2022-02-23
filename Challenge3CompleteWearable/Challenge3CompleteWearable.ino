/*
 * Global variables
 */
 

int ax = 0; int ay = 0; int az = 0;  // Acceleration values recorded from the readAccelSensor() function

int ppg = 0;                         // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0;                  // Time of last sample (in Sampling tab)
bool sending;                        // bool to check if sending data

unsigned long buzz_start = millis(); // track start time of buzzing
bool buzzing = false;                // tracks if buzz is active
bool weather = false;                // tracks if weather should be displayed for pushbutton cycling
bool the_time = true;                // tracks if time should be displayed for pushbutton cycling
bool date = false;                   // tracks if date should be displayed for pushbutton cycling

String logged_time;
String logged_date;
String logged_wx;

/*
 * Initialize the various components of the wearable
 */
void setup() {
  button_setup();
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  sending = false;
  writeDisplay("Sleep", 0, true);
  setupMotor();
  Serial.begin(9600);
}

/*
 * The main processing loop
 */
void loop() {

  // Displays messages from PC
  String command = receiveMessage();
  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true);
  }
  else if(command.substring(0, 6) == "Time: ") {
    logged_time = command;
    Serial.println(logged_time);
    if (the_time) { // check if time is to be displayed
      writeDisplay("                 ", 0, false);
      writeDisplay(command.c_str(), 0, false);
    }
  }
  else if (command.substring(0, 6) == "Date: ") {
    logged_date = command;
    Serial.println(logged_date);
    if (date) { // check if date is to be displayed
      writeDisplay("                 ", 0, false);
      writeDisplay(command.c_str(), 0, false);
    }
  }
  else if (command.substring(0, 4) == "WX: ")  {
    logged_wx = command;
    Serial.println(logged_wx);
    if (weather) { // check if weather is to be displayed
      writeDisplay("                 ", 0, false);
      writeDisplay(command.c_str(), 0, false);
    }
  }
  else if(command.substring(0, 7) == "Steps: ") {
    writeDisplay(command.c_str(), 1, false);
  }
  else if(command.substring(0, 4) == "HR: ") {
    writeDisplay(command.c_str(), 2, false);
  }

  // checks pushbutton to cycle between time, date, and weather
  if (button_pressed()) { 
    if (the_time) { // switch to date being displayed
      the_time = false;
      date = true;
      writeDisplay("                 ", 0, false);
      writeDisplay(logged_date.c_str(), 0, false);
    }
    else if (date) { // switch to weather being displayed
      date = false;
      weather = true;
      writeDisplay("                 ", 0, false);
      writeDisplay(logged_wx.c_str(), 0, false);
    }
    else if (weather) {
      weather = false;
      the_time = true;
      writeDisplay("                 ", 0, false);
      writeDisplay(logged_time.c_str(), 0, false);
    }
  }

  // Idle detector
  if(command == "User Inactive") {
    sending = true;
    writeDisplay("User Inactive", 0, false);
    if (buzzing) {
      if (millis() - buzz_start > 1000) {
        deactivateMotor();
        buzzing = false;
      }
    }
    else if (!buzzing) {
      activateMotor(127);
      buzz_start = millis();
//      buzzing = true;
    }
  }

  // sends samples to python  via bluetooth for processing. 
  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    response += "," + String(ppg);
    sendMessage(response);
  }
}
