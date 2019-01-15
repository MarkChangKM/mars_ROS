#!/usr/bin/env python
import rospy
import math

from duckietown_msgs.msg import WheelsCmdStamped
from sensor_msgs.msg import Joy

class joystick_wheel_control(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing " %(self.node_name))

        self.joy = None

        # Publications
        self.pub_car_cmd = rospy.Publisher("wheels_cmd_executed", WheelsCmdStamped, queue_size=1)

        # Subscriptions
        self.sub_joy_ = rospy.Subscriber("joy", Joy, self.cbJoy, queue_size=1)

    def cbJoy(self, joy_msg):
        self.joy = joy_msg
        self.publishControl()

    def publishControl(self):
        car_cmd_msg = WheelsCmdStamped()
        car_cmd_msg.header.stamp = self.joy.header.stamp
        if self.joy.axes[1]>=0:
            if self.joy.axes[0]>=0:
                car_cmd_msg.vel_left = self.joy.axes[1]/1.1
                car_cmd_msg.vel_right = (self.joy.axes[1]+0.7*self.joy.axes[0])/1.1
            else:
                car_cmd_msg.vel_left = (self.joy.axes[1]-0.7*self.joy.axes[0])/1.1
                car_cmd_msg.vel_right = self.joy.axes[1]/1.1
        else:
            if self.joy.axes[0]>=0:
                car_cmd_msg.vel_left = self.joy.axes[1]/1.1
                car_cmd_msg.vel_right = (self.joy.axes[1]-0.7*self.joy.axes[0])/1.1
            else:
                car_cmd_msg.vel_left = (self.joy.axes[1]+0.7*self.joy.axes[0])/1.1
                car_cmd_msg.vel_right = self.joy.axes[1]/1.1
        if car_cmd_msg.vel_left>1:
            car_cmd_msg.vel_left=1
        elif car_cmd_msg.vel_left<-1:
            car_cmd_msg.vel_left=-1
        if car_cmd_msg.vel_right>1:
            car_cmd_msg.vel_right=1
        elif car_cmd_msg.vel_right<-1:
            car_cmd_msg.vel_right=-1
        self.pub_car_cmd.publish(car_cmd_msg)

if __name__ == "__main__":
    rospy.init_node("joystick_wheel_control",anonymous=False)
    joystick_wheel_control = joystick_wheel_control()
    rospy.spin()
