#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <Servo.h> 
#include <ros.h>
#include <std_msgs/UInt16.h>

ros::NodeHandle  nh;

Servo servo_up;
Servo servo_down;

void servo_down_cb( const std_msgs::UInt16& cmd_msg){
  // set servo angle, should be from 0-180  
  servo_down.write(cmd_msg.data);
  // toggle led
  digitalWrite(13, HIGH-digitalRead(13));
}

void servo_up_cb( const std_msgs::UInt16& cmd_msg){
  // set servo angle, should be from 0-180  
  servo_up.write(cmd_msg.data);
  // toggle led
  digitalWrite(13, HIGH-digitalRead(13));
}


ros::Subscriber<std_msgs::UInt16> sub_down("servo_down", servo_down_cb);
ros::Subscriber<std_msgs::UInt16> sub_up("servo_up", servo_up_cb);

void setup(){
  pinMode(13, OUTPUT);

  nh.initNode();
  nh.subscribe(sub_down);
  nh.subscribe(sub_up);

  servo_up.attach(3);
  servo_down.attach(9);
}

void loop(){
  nh.spinOnce();
  delay(1);
}
