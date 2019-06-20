#!/usr/bin/env python
import rospy
import cv2
import sys
import logging as log
import datetime as dt
import numpy

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from face_follower.msg import rlist
from time import sleep

class image_converter:

    def __init__(self):

        rospy.init_node('image_converter', anonymous=True)
        rospy.loginfo("recognizer started")
        print "1................................................"

        # Configure acoustic model
        self._Cascade_Classifier = "~cascade_classifier"
        if rospy.has_param(self._Cascade_Classifier):
            cascPath = rospy.get_param(self._Cascade_Classifier)
        else:
            rospy.logwarn("parameters need to be set to start recognizer.")
            return

        self._coordinates = "~coordinates"
        print rospy.has_param(self._coordinates)
        if rospy.has_param(self._coordinates):
            coordinates = rospy.get_param(self._coordinates)
            self.publ = rospy.Publisher(coordinates, rlist, queue_size=10)

        self.bridge = CvBridge()
        self.faceCascade = cv2.CascadeClassifier(cascPath)
        
        #Where to publish
        self._output_image_topic = "~image_topic_output"
        print rospy.has_param(self._output_image_topic)
        if rospy.has_param(self._output_image_topic):
            output_image_topic = rospy.get_param(self._output_image_topic)
            self.image_pub = rospy.Publisher(output_image_topic,Image, queue_size=10)
      
        #Where to subscribe
        self._input_image_topic = "~image_topic_input"
        print rospy.has_param(self._input_image_topic)
        if rospy.has_param(self._input_image_topic):
            input_image_topic = rospy.get_param(self._input_image_topic)
            self.image_sub = rospy.Subscriber(input_image_topic, Image, self.callback)


    def callback(self,data):
        try:
            frame = self.bridge.imgmsg_to_cv2(data, "bgr8")
            var = rlist()
            var.header.stamp = rospy.Time.now()
        except CvBridgeError as e:
            print(e)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        if len(faces):
            rospy.loginfo("I see a face %d",len(faces))
            rospy.logdebug("Partial: %s" + str(faces))

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                var.data = [x, y, w, h]
                self.publ.publish(var)
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.circle(frame, (x+(w/2), y+(h/2)), 5, 255,-1)
        else:
        	self.publ.publish(var)

        try:
          self.image_pub.publish(self.bridge.cv2_to_imgmsg(frame, "bgr8"))
        except CvBridgeError as e:
          print(e)

    
if __name__ == '__main__':
    rospy.loginfo("simple_face_detection ...........")
    print "................................................"

    ic = image_converter()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()