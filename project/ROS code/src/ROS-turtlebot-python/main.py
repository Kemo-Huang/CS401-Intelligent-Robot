#!/usr/bin/env python

'''
Copyright (c) 2019, Aaron Tian
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from math import radians

mms = None

# curr_cmd_idx = 0 # Current command index
# moving = False
# move_state = 0 # 0: stand, 1: go_circle, 2: cxk, 3: tri, 4:rotate, 5: go_master, 6: turn_back
# moves = []
# times = []
# 0: stand, 1: go_circle, 2: cxk_left, 3: cxk_right, 4: tri_move, 5: tri_turn, 6: rotate, 7: go_straight, 8: turn_half
# 9: right_45, 10: reverse_45, 11: left_45, 12: rleft_45
# for i in range(times(0)):
# while rospy.is_shutdown():
#     mms.cmd_vel.publish(moves[0])
#     mms.r.sleep()


class Movements():

    def __init__(self):
        self.moving = False
        self.move_state = 0  # 0: stand, 1: go_circle, 2: cxk, 3: tri, 4:rotate
        self.moves = []
        self.times = []
        self.init_cmds()
        rospy.init_node('Movements', anonymous=False)
        rospy.Subscriber('chatter', String, self.callback)
        # rospy.loginfo("To stop TurtleBot CTRL + C")
        rospy.on_shutdown(self.shutdown)
        self.cmd_vel = rospy.Publisher(
            'cmd_vel_mux/input/navi', Twist, queue_size=10)
        self.r = rospy.Rate(10)  # 10Hz = 0.1s
        while not rospy.is_shutdown():
            rospy.loginfo("Waiting for msg...")
            if not self.moving:
                self.cmd_vel.publish(self.moves[0])
                self.r.sleep()
            else:
                rospy.loginfo("Movement started.")
                if self.move_state == 1:
                    self.do_cmd(1)
                elif self.move_state == 2:
                    for i in range(0, 6):
                        self.do_cmd(2)
                        self.do_cmd(3)
                elif self.move_state == 3:
                    for i in range(0, 3):
                        self.do_cmd(4)
                        self.do_cmd(5)
                elif self.move_state == 4:
                    self.do_cmd(6)
                elif self.move_state == 5:
                    self.do_cmd(7)
                elif self.move_state == 6:
                    self.do_cmd(8)
                    self.do_cmd(7)
                    self.do_cmd(8)
                elif self.move_state == 7:
                    self.dance()
                elif self.move_state in (8, 9, 10, 11):
                    self.do_cmd(self.move_state+1)
                self.moving = False
                rospy.loginfo("Movement ended.")
        # rospy.spin()

    def do_cmd(self, move):
        for i in range(0, self.times[move]):
            self.cmd_vel.publish(self.moves[move])
            self.r.sleep()

    def dance(self):
        self.do_cmd(9)
        self.do_cmd(10)
        self.do_cmd(11)
        self.do_cmd(12)
        for i in range(0, 8):
            self.do_cmd(2)
            self.do_cmd(3)
        self.do_cmd(6)
        for i in range(0, 8):
            self.do_cmd(2)
            self.do_cmd(3)
        self.move_func(0, 4, 80)
        self.move_func(0.3, 0, 10)
        self.move_func(-0.3, 0, 10)
        # self.do_cmd(0)
        self.move_func(0, 0, 40)
        self.move_func(0, 4, 80)

    def move_func(self, v, w, t):
        tempt_cmd = Twist()
        tempt_cmd.linear.x = v
        tempt_cmd.angular.z = w
        for i in range(0, t):
            self.cmd_vel.publish(tempt_cmd)
            self.r.sleep()

    def init_cmds(self):
        stand_cmd = Twist()
        stand_cmd.linear.x = 0
        stand_cmd.angular.z = 0
        self.moves.append(stand_cmd)
        self.times.append(0)

        circle_cmd = Twist()
        circle_cmd.linear.x = 0.2
        circle_cmd.angular.z = 1.04
        self.moves.append(circle_cmd)
        self.times.append(70)

        cxk_left = Twist()
        cxk_left.linear.x = 0
        cxk_left.angular.z = 0.8
        self.moves.append(cxk_left)
        self.times.append(3)

        cxk_right = Twist()
        cxk_right.linear.x = 0
        cxk_right.angular.z = -0.8
        self.moves.append(cxk_right)
        self.times.append(3)

        tri_move = Twist()
        tri_move.linear.x = 0.3
        self.moves.append(tri_move)
        self.times.append(20)

        tri_turn = Twist()
        tri_turn.linear.x = 0
        tri_turn.angular.z = radians(75)
        self.moves.append(tri_turn)
        self.times.append(20)

        rotate_cmd = Twist()
        rotate_cmd.linear.x = 0
        rotate_cmd.angular.z = 1.04
        self.moves.append(rotate_cmd)
        self.times.append(80)

        go_straight = Twist()
        go_straight.linear.x = 0.3
        self.moves.append(go_straight)
        self.times.append(40)

        half_turn = Twist()
        half_turn.linear.x = 0
        half_turn.angular.z = 1.04
        self.moves.append(half_turn)
        self.times.append(40)

        right_45 = Twist()
        right_45.linear.x = 0.2
        right_45.angular.z = 0.3
        self.moves.append(right_45)
        self.times.append(20)

        reverse_45 = Twist()
        reverse_45.linear.x = -0.2
        reverse_45.angular.z = -0.3
        self.moves.append(reverse_45)
        self.times.append(20)

        left_45 = Twist()
        left_45.linear.x = 0.2
        left_45.angular.z = -0.3
        self.moves.append(left_45)
        self.times.append(20)

        lreverse_45 = Twist()
        lreverse_45.linear.x = -0.2
        lreverse_45.angular.z = 0.3
        self.moves.append(lreverse_45)
        self.times.append(20)

    def shutdown(self):
        rospy.loginfo("Stop TurtleBot")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

    def callback(self, data):
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        if data.data == 'circle':
            self.moving = True
            self.move_state = 1
        elif data.data == 'dou':
            self.moving = True
            self.move_state = 2
        elif data.data == 'tri':
            self.moving = True
            self.move_state = 3
        elif data.data == 'rotate':
            self.moving = True
            self.move_state = 4
        elif data.data == 'go':
            self.moving = True
            self.move_state = 5
        elif data.data == 'back':
            self.moving = True
            self.move_state = 6
        elif data.data == 'dance':
            self.moving = True
            self.move_state = 7
        elif data.data == 'left':
            self.moving = True
            self.move_state = 8
        elif data.data == 'left_back':
            self.moving = True
            self.move_state = 9
        elif data.data == 'right':
            self.moving = True
            self.move_state = 10
        elif data.data == 'right_back':
            self.moving = True
            self.move_state = 11


if __name__ == "__main__":
    # try:
    mms = Movements()
    # except:
    # rospy.loginfo("Movements node terminated.")
