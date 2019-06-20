#!/usr/bin/env python
import csv
import rospy
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist

import tf

tol = 0.3
tol1= 0.1
cmd_vel = Twist()
foward = -0.4
backward = -0.5
left = 0.4714
right = 0.4609

rospy.init_node('quat2rpy')
listener = tf.TransformListener()
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(10.0) 

while not rospy.is_shutdown():
    try:
        (trans,rot) = listener.lookupTransform('/right_elbow_1','/openni_depth_frame',  rospy.Time(0))
        (trans1,rot1) = listener.lookupTransform('/right_hand_1','/openni_depth_frame',  rospy.Time(0))
        
        (trans2,rot2) = listener.lookupTransform('/left_elbow_1','/openni_depth_frame',  rospy.Time(0))
        (trans3,rot3) = listener.lookupTransform('/left_hand_1','/openni_depth_frame',  rospy.Time(0))
        
        euler = tf.transformations.euler_from_quaternion(rot)
        euler1 = tf.transformations.euler_from_quaternion(rot1)
        euler2 = tf.transformations.euler_from_quaternion(rot2)
        euler3 = tf.transformations.euler_from_quaternion(rot3)
        
        #print(euler) 
        #print(trans1)
        #print(euler2)
        #print(trans3)
        
        if (euler[1] > foward-tol) and (euler[1] < foward+tol):
        
            cmd_vel.linear.x=1.0
            print('FOWARD')
            
        elif (euler2[1] > backward-tol) and (euler2[1] < backward+tol): 
        
            cmd_vel.linear.x=-1.0
            print('BACKWARD')
            
        elif (trans1[1] > left-tol1) and (trans1[1] < left+tol1):
        
            cmd_vel.angular.z=1.0
            print('TURN LEFT')
            
        elif (trans3[1] > right-tol1) and (trans3[1] < right+tol1):
            
            cmd_vel.angular.z=-1.0
            print('TURN RIGHT')
            
        else:
        
            cmd_vel.linear.x=0
            cmd_vel.angular.z=0
            print('Waiting For Input')
            
        pub.publish(cmd_vel)
        
    except:
        pass




rospy.loginfo("COMPLETE")
