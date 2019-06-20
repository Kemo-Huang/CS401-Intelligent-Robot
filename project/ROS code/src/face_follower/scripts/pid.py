#!/usr/bin/env python
"""Generic PID implimentation."""
import rospy
from std_msgs.msg import Empty
from std_msgs.msg import Float64
import numpy as np
import time

pub_bot = rospy.Publisher('plot_bottom', Float64, queue_size=5)
pub_top = rospy.Publisher('plot_top', Float64, queue_size=5)

class pid(object):
    """docstring for pid"""
    def __init__(self, kp=0.05, kd=0.0, ki=0.04, set_array=[320, 240]):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.set_array = set_array
        self.last_time = 0
        self.integral = 0
        self.derivative = 0
        self.last_error = 0
        
    def set_set_array(self, set_array):
        self.set_array = set_array

    def get_set_array(self):
        return self.set_array

    def pid_step(self, data):
        current_time = time.time()
        dt = current_time - self.last_time
        if dt > 0.3:
            dt = 0.3
            self.integral = 0.0

        error = self.set_array - np.array([data[0], data[1]])

        # publish errors for plotting.
        pub_bot.publish(error[0])
        pub_top.publish(error[1])

        self.integral += error * dt
        self.derivative = (error - self.last_error) / dt

        f = self.kp * error + self.ki * \
            self.integral + self.kd * self.derivative

        self.last_error = error
        self.last_time = current_time

        f[1] = -f[1]

        f = np.clip(f, -90, 90)

        return f
