#!/usr/bin/env python
import csv
import rospy
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import sys
import select
import termios
import tty
import tf

if_clear = False
tol1 = 0.3
tol2 = 0.3
tol3 = 0.3
tol4 = 0.3
cmd_vel = Twist()
foward = -0.45
backward = -0.45
left = 0.3
right = 0.3
cmd = None

commands = {
    'q': 'circle',
    'w': 'dou',
    'e': 'tri',
    'r': 'rotate',
    't': 'go',
    'y': 'back',
    'd': 'dance'
}

counter = {'q':0, 'w':0, 'y':0, 't':0}

def shutdown():
    rospy.loginfo("Stop Talker")
    rospy.sleep(1)

pub = rospy.Publisher('chatter', String, queue_size=1)
rospy.init_node('talker', anonymous=True)
listener = tf.TransformListener()
settings = termios.tcgetattr(sys.stdin)
rate = rospy.Rate(10.0) 

while not rospy.is_shutdown():
    try:

        # subscribe message from openni_depth_frame
        (trans,rot) = listener.lookupTransform('/right_elbow_1','/openni_depth_frame',  rospy.Time(0))
        (trans1,rot1) = listener.lookupTransform('/right_hand_1','/openni_depth_frame',  rospy.Time(0))
        
        (trans2,rot2) = listener.lookupTransform('/left_elbow_1','/openni_depth_frame',  rospy.Time(0))
        (trans3,rot3) = listener.lookupTransform('/left_hand_1','/openni_depth_frame',  rospy.Time(0))
        
        euler = tf.transformations.euler_from_quaternion(rot)
        euler1 = tf.transformations.euler_from_quaternion(rot1)
        euler2 = tf.transformations.euler_from_quaternion(rot2)
        euler3 = tf.transformations.euler_from_quaternion(rot3)
        
        # print('right elbow', euler[1]) 
        print('right hand', trans1[1])
        # print('left elbow', euler2[1])
        print('left hand', trans3[1])
        
        if (trans1[1] > foward-tol1) and (trans1[1] < foward+tol1):
        
            # cmd = commands['q']
            # counter['q'] += 1
            # print('CIRCLE')
            pass
            
        elif (trans3[1] > backward-tol2) and (trans3[1] < backward+tol2): 
        
            # cmd = commands['w']
            counter['w'] += 1
            print('DOU')
            
        elif (trans1[1] > left-tol3) and (trans1[1] < left+tol3):
        
            # cmd = commands['y']
            counter['y'] += 1
            print('BACK')
            
        elif (trans3[1] > right-tol4) and (trans3[1] < right+tol4):
            
            # cmd = commands['t']
            counter['t'] += 1
            print('GO')
            
        else:
        
            cmd = 'nothing'
            print('Waiting For Input')
    # except:
    #     pass
    
        
        # conut the number
        for key, value in counter.items():
            if value >= 10:
                cmd = commands[key]
                # print('cmd', cmd)
                # set clear flag
                if_clear = True
                break
        
        # clear counter
        if if_clear:
            if_clear = False
            for key, value in counter.items():
                counter[key] = 0
                # cmd = None

        print(cmd)
        pub.publish(cmd)
        cmd = None
        rate.sleep()
        
    except:
        pass




rospy.loginfo("COMPLETE")
