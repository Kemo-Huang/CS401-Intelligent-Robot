#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import sys
import select
import termios
import tty

commands = {
    'q': 'circle',
    'w': 'dou',
    'e': 'tri',
    'r': 'rotate',
    't': 'go',
    'y': 'back',
    'd': 'dance',
    ',': 'left',
    '.': 'right',
    'm': 'left_back',
    '/': 'right_back'
}


def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def shutdown():
    rospy.loginfo("Stop Talker")
    rospy.sleep(1)


if __name__ == '__main__':
    try:
        settings = termios.tcgetattr(sys.stdin)
        pub = rospy.Publisher('chatter', String, queue_size=1)
        rospy.init_node('talker', anonymous=True)
        rospy.on_shutdown(shutdown)
        rate = rospy.Rate(10)  # 10hz

        while not rospy.is_shutdown():
            key = getKey()
            if key in commands.keys():
                cmd = commands[key]
            else:
                cmd = 'nothing'
            print(cmd)
            pub.publish(cmd)
            rate.sleep()
            
    except rospy.ROSInterruptException as e:
        print(e)
