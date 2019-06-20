#!/usr/bin/env python
from __future__ import print_function
import rospy
from face_follower.msg import rlist
from std_msgs.msg import UInt16
from pid import pid
import numpy as np
import time

class follower:
    def __init__(self):
        rospy.init_node('follow_face', anonymous=True)
        # real_drone = bool(rospy.get_param('~real_drone', 'false'))

        rospy.Subscriber("/face_tracker/bbox", rlist, self.maintain_coords)
        self.timer = rospy.Timer(rospy.Duration(2), self.timer_callback, True)

        self.servo_down_pub = rospy.Publisher('servo_down', UInt16, queue_size=10)
        self.servo_up_pub = rospy.Publisher('servo_up', UInt16, queue_size=10)

        # servo angles
        self.up = 90
        self.down = 110

        # set default servo angles
        self.servo_down_pub.publish(self.down)
        self.servo_up_pub.publish(self.up)

        # init pid
        self.pid = pid()

        
    def maintain_coords(self, data):
        """
        callback to keep the face in the center

            get coords
            get current angle
            # get center of image - 640 / 2
            apply pid for maintaining center
        """
        f = self.pid.pid_step(np.array(data.data)) + 90

        print(f)
        self.down = f[0]
        self.up = f[1]
        self.servo_pub()
        
        self.timer.shutdown()
        self.timer = rospy.Timer(rospy.Duration(2), self.timer_callback, True)

    def servo_pub(self):
        self.servo_down_pub.publish(self.down)
        self.servo_up_pub.publish(self.up)

    def timer_callback(self, event):
        print("no face being detected")
        # servo_down_pub.publish(90)
        # servo_up_pub.publish(110)
        # sd.set_servo_angles(90, 110)

if __name__ == '__main__' :

    rospy.loginfo("Starting follower.......")
    it = follower()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")