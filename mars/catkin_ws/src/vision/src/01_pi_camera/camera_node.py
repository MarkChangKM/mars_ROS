#!/usr/bin/env python
import io
import thread
import yaml
from picamera import PiCamera
from picamera.array import PiRGBArray
import rospkg
import rospy
from sensor_msgs.msg import CompressedImage
from sensor_msgs.srv import SetCameraInfo, SetCameraInfoResponse


class CameraNode(object):

    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing......" % (self.node_name))
        self.image_msg = CompressedImage()

        # Setup PiCamera
        self.camera = PiCamera()
        self.camera.framerate = 12
        self.camera.resolution = (320, 240)

        # For intrinsic calibration
        self.frame_id = rospy.get_namespace().strip('/') + "/camera_optical_frame"

        self.has_published = False
        self.pub_img = rospy.Publisher("~image/compressed", CompressedImage, queue_size=1)
        self.stream = io.BytesIO()
        self.is_shutdown = False
        rospy.loginfo("[%s] Initialized." % (self.node_name))

    def startCapturing(self):
        rospy.loginfo("[%s] Start capturing." % (self.node_name))
        while not self.is_shutdown and not rospy.is_shutdown():
            gen = self.grabAndPublish(self.stream, self.pub_img)
            try:
                self.camera.capture_sequence(gen, 'jpeg', use_video_port=True, splitter_port=0)
            except StopIteration:
                pass
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
