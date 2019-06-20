import csv
import rospy
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist

import tf

tol = 0.3 #the tolerance in which I can move my elbow in a given direction and still get a reading
tol1= 0.1 #the tolerance in which I can move my hand in a given direction and still get a reading
cmd_vel = Twist()
foward = -0.4 #the x-axis orientation for my right elbow that needs to be met for the robot to move foward
backward = -0.5 #the x-axis orientation for my right elbow that needs to be met for the robot to move backward
left = 0.4714 #the x-axis orientation for my left hand that needs to be met for the robot to move left
right = 0.4609 #the x-axis orientation for my right hand that needs to be met for the robot to move right

rospy.init_node('quat2rpy') #initialized a node named quat2rpy
listener = tf.TransformListener() #starts a listener that looks for the transforms that are published by the /tf topic
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1) #publishes a command velocity command to the turtle 1 listener. This will change depending on what type of platform you are trying to interface with (ex. TurtleSim, TurtleBot, GVR Bot)

rate = rospy.Rate(10.0) #refreshes the command at a rate of 10 Hz

while not rospy.is_shutdown(): #starts a while loop that runs while rospy is still running
    try:
        (trans,rot) = listener.lookupTransform('/right_elbow_1','/openni_depth_frame',  rospy.Time(0)) #a function that collects the translation and rotation data published by the /tf node for the coordinate axis fixed to my left (the camera's right) elbow
        
        (trans1,rot1) = listener.lookupTransform('/right_hand_1','/openni_depth_frame',  rospy.Time(0)) #a function that collects the data translation and rotation data published by the /tf node for the coordinate axis fixed to my left (the camera's right) hand
        
        (trans2,rot2) = listener.lookupTransform('/left_elbow_1','/openni_depth_frame',  rospy.Time(0)) #a function that collects the data translation and rotation data published by the /tf node for the coordinate axis fixed to my right (the camera's left) elbow
        
        (trans3,rot3) = listener.lookupTransform('/left_hand_1','/openni_depth_frame',  rospy.Time(0))#a function that collects the data translation and rotation data published by the /tf node for the coordinate axis fixed to my right (the camera's left) hand
        
        euler = tf.transformations.euler_from_quaternion(rot) #a function that transforms the stored rotation data (that is in quaternion) into useable data in the form of roll, pitch, and yaw for my left (the camera's right) elbow
        
        euler1 = tf.transformations.euler_from_quaternion(rot1) #a function that transforms the stored rotation data (that is in quaternion) into useable data in the form of roll, pitch, and yaw for my left (the camera's right) hand
        
        euler2 = tf.transformations.euler_from_quaternion(rot2) #a function that transforms the stored rotation data (that is in quaternion) into useable data in the form of roll, pitch, and yaw for my right (the camera's left) elbow
        
        euler3 = tf.transformations.euler_from_quaternion(rot3)#a function that transforms the stored rotation data (that is in quaternion) into useable data in the form of roll, pitch, and yaw for my right (the camera's left) hand
        
        #print(euler) 
        #print(trans1)
        #print(euler2)
        #print(trans3)
        
        if (euler[1] > foward-tol) and (euler[1] < foward+tol): #checks to see if my body position is in the correct orientation based on the given x-axis position and the tolerance for the pose. Based off of my left elbow (camera's right)
        
            cmd_vel.linear.x=1.0 #if this conditional passes it moves the robot forward at a rate of 1.0 m/s
            print('FOWARD')
            
        elif (euler2[1] > backward-tol) and (euler2[1] < backward+tol): #checks to see if my body position is in the correct orientation based on the given x-axis position and the tolerance for the pose. Based off of my left hand (camera's right)
        
            cmd_vel.linear.x=-1.0 #if this conditional passes it moves the robot backward at a rate of 1.0 m/s
            print('BACKWARD')
            
        elif (trans1[1] > left-tol1) and (trans1[1] < left+tol1): #checks to see if my body position is in the correct orientation based on the given x-axis position and the tolerance for the pose. Based off of my right elbow (camera's left)
        
            cmd_vel.angular.z=1.0 #if this conditional passes it turns the robot to the left at a rate of 1.0 rad/s
            print('TURN LEFT')
            
        elif (trans3[1] > right-tol1) and (trans3[1] < right+tol1): #checks to see if my body position is in the correct orientation based on the given x-axis position and the tolerance for the pose. Based off of my right hand (camera's left)
            
            cmd_vel.angular.z=-1.0 #if this conditional passes it turns the robot to the right at a rate of 1.0 rad/s
            print('TURN RIGHT')
            
        else:
        
        #if neither conditional statement is being satisfied then the command velocity for the robot is set to 0 m/s and the robot will not move until a conditional is met
            cmd_vel.linear.x=0 
            cmd_vel.angular.z=0
            print('Waiting For Input')
            
        pub.publish(cmd_vel) #publishes the command velocity to the node that is listening on the robot or simulation
        
    except:
        pass




rospy.loginfo("COMPLETE")
