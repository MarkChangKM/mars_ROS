#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Bool

class red_circle_direct(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        self.sub_compressed_img = rospy.Subscriber("~compressed",CompressedImage,self.cbImg,queue_size=1)
        self.pub_direction = rospy.Publisher("direction",Bool,queue_size=10)
    def cbImg(self,msg):
        rospy.loginfo("get img")
        np_arr = np.fromstring(msg.data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        blur = cv2.GaussianBlur(img,(5,5),0)
        hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
        low_red = np.array([165,100,40])
        up_red = np.array([180,255,255])
        mask = cv2.inRange(hsv,low_red, up_red)
        canny = cv2.Canny(mask,50,150)
        _,contours,hierarchy = cv2.findContours(canny,1,2)
        if contours:
            c = max(contours, key = cv2.contourArea)
            (x,y),area = cv2.minEnclosingCircle(c)
            if x>=160:
                self.pub_direction.publish(True)
            else:
                self.pub_direction.publish(False)
if __name__ == '__main__':
    rospy.init_node('red_circle_direct',anonymous=False)
    redcircledirect = red_circle_direct()
    rospy.spin()
