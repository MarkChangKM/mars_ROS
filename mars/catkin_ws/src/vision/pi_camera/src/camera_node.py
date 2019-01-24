#!/usr/bin/env python
import io
import thread
import yaml
from picamera import PiCamera
from picamera.array import PiRGBArray
import rospkg
import rospy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Bool


class CameraNode(object):

    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing......" % (self.node_name))

        self.framerate_high = self.setupParam("~framerate_high", 30.0)
        self.framerate_low = self.setupParam("~framerate_low", 15.0)
        self.res_w = self.setupParam("~res_w", 640)
        self.res_h = self.setupParam("~res_h", 480)

        self.image_msg = CompressedImage()

        # Setup PiCamera
        self.camera = PiCamera()
        self.framerate = self.framerate_high  # default to high
        self.camera.framerate = self.framerate
        self.camera.resolution = (self.res_w, self.res_h)

        # For intrinsic calibration
        self.cali_file_folder = "/camera_calibration/"
        self.frame_id = rospy.get_namespace().strip('/') + "/camera_optical_frame"

        self.has_published = False
        self.pub_img = rospy.Publisher("~image/compressed", CompressedImage, queue_size=1)
        self.sub_switch_high = rospy.Subscriber("~framerate_high_switch", Bool, self.cbSwitchHigh, queue_size=1)

        self.stream = io.BytesIO()
        self.is_shutdown = False
        rospy.loginfo("[%s] Initialized." % (self.node_name))

    def cbSwitchHigh(self, switch_msg):
        print switch_msg
        if switch_msg.data and self.framerate != self.framerate_high:
            self.framerate = self.framerate_high
            self.update_framerate = True
        elif not switch_msg.data and self.framerate != self.framerate_low:
            self.framerate = self.framerate_low
            self.update_framerate = True


    def startCapturing(self):
        rospy.loginfo("[%s] Start capturing." % (self.node_name))
        while not self.is_shutdown and not rospy.is_shutdown():
            gen = self.grabAndPublish(self.stream, self.pub_img)
            try:
                self.camera.capture_sequence(gen, 'jpeg', use_video_port=True, splitter_port=0)
            except StopIteration:
                pass
            self.camera.framerate = self.framerate
            self.update_framerate = False
        self.camera.close()
        rospy.loginfo("[%s] Capture Ended." % (self.node_name))

    def grabAndPublish(self, stream, publisher):
        while not self.is_shutdown and not rospy.is_shutdown():
            yield stream
            # Construct image_msg
            # Grab image from stream
            stamp = rospy.Time.now()
            stream.seek(0)
            stream_data = stream.getvalue()
            # Generate compressed image
            image_msg = CompressedImage()
            image_msg.format = "jpeg"
            image_msg.data = stream_data
            image_msg.header.stamp = stamp
            image_msg.header.frame_id = self.frame_id
            publisher.publish(image_msg)

            # Clear stream
            stream.seek(0)
            stream.truncate()

            if not self.has_published:
                rospy.loginfo("[%s] Published the first image." % (self.node_name))
                self.has_published = True
            rospy.sleep(rospy.Duration.from_sec(0.001))

    def setupParam(self, param_name, default_value):
        value = rospy.get_param(param_name, default_value)
        rospy.set_param(param_name, value)  #Write to parameter server for transparancy
        rospy.loginfo("[%s] %s = %s " % (self.node_name, param_name, value))
        return value

    def onShutdown(self):
        rospy.loginfo("[%s] Closing camera." % (self.node_name))
        self.is_shutdown = True
        rospy.loginfo("[%s] Shutdown." % (self.node_name))

if __name__ == '__main__':
    rospy.init_node('camera_node', anonymous=False)
    camera_node = CameraNode()
    rospy.on_shutdown(camera_node.onShutdown)
    thread.start_new_thread(camera_node.startCapturing, ())
    rospy.spin()
