#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import CompressedImage

class view_camera(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        self.sub_compressed_img = rospy.Subscriber("~compressed",CompressedImage,self.cbImg,queue_size=1)
    def cbImg(self,msg):
        rospy.loginfo("get img")
        np_arr = np.fromstring(msg.data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        cv2.imshow("camera",img)
        cv2.waitKey(1)
if __name__ == '__main__':
    rospy.init_node('view_camera',anonymous=False)
    view_camera = view_camera()
    rospy.spin()
