#!/usr/bin/env python
import os.path
from pi_camera.camera_info import load_camera_info_2
import rospkg
import rospy
from sensor_msgs.msg import CameraInfo, CompressedImage, Image


class CamInfoReader(object):

    def __init__(self):
        self.node_name = rospy.get_name()
        # Load parameters
        self.config = self.setupParam("~config", "baseline")
        self.image_type = self.setupParam("~image_type", "compressed")

        # Setup publisher
        self.pub_camera_info = rospy.Publisher("~camera_info", CameraInfo, queue_size=1)

        # Get path to calibration yaml file
        self.camera_info_msg = None
        self.cali_file = "/camera_calibration/marsbot.yaml"

        # Shutdown if no calibration file not found
        if not os.path.isfile(self.cali_file):
            rospy.signal_shutdown("Found no calibration file ... aborting")

        # Print out and prepare message
        rospy.loginfo("[%s] Using calibration file: %s" % (self.node_name, self.cali_file))
        self.camera_info_msg = load_camera_info_2(self.cali_file)
        self.camera_info_msg.header.frame_id = rospy.get_namespace() + "camera_optical_frame"
        rospy.loginfo("[%s] CameraInfo: %s" % (self.node_name, self.camera_info_msg))
        img_type = CompressedImage if self.image_type == "compressed" else Image
        typemsg = "CompressedImage" if self.image_type == "compressed" else "Image"
        rospy.logwarn("[%s] ==============%s", self.node_name, typemsg)
        self.sub_img_compressed = rospy.Subscriber("~compressed_image", img_type, self.cbCompressedImage, queue_size=1)

    def cbCompressedImage(self, msg):
        if self.camera_info_msg is not None:
            self.camera_info_msg.header.stamp = msg.header.stamp
            self.pub_camera_info.publish(self.camera_info_msg)

    def setupParam(self, param_name, default_value):
        value = rospy.get_param(param_name, default_value)
        rospy.set_param(param_name, value)  #Write to parameter server for transparancy
        rospy.loginfo("[%s] %s = %s " % (self.node_name, param_name, value))
        return value

    def on_shutdown(self):
        rospy.loginfo("[%s] Shutdown." % (self.node_name))


if __name__ == '__main__':
    rospy.init_node('cam_info_reader', anonymous=False)
    node = CamInfoReader()
    rospy.on_shutdown(node.on_shutdown)
    rospy.spin()
