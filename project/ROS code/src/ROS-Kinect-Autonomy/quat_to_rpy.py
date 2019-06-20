#!/usr/bin/env python
import csv
import rospy
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist

import tf

tol = 0.75
cmd_vel = Twist()
foward = -2.95
backward = 3.25
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
        
                
    except:
        pass




rospy.loginfo("COMPLETE")
