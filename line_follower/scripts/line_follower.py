#!/usr/bin/env python

from re import L
import rospy
import numpy as np
import cv2
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge

bridge = CvBridge()
g_twist = None


def img_callback(msg):
  img = bridge.compressed_imgmsg_to_cv2(msg, 'bgr8')
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

  lower_yellow = np.array([20, 100, 100])
  upper_yellow = np.array([30, 255, 255])
  mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

  h, w, d = img.shape
  search_top = 3*h/4
  search_bot = 3*h/4 + 20
  mask[0:search_top, 0:w] = 0
  mask[search_bot:h, 0:w] = 0

  M = cv2.moments(mask)
  if M['m00'] > 0:
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(img, (cx, cy), 20, (0, 0, 255), -1)
    err = cx - w/2
    g_twist.linear.x = 0.07
    g_twist.angular.z = -float(err)/100
    cv2.imshow('Line detected', img)
    cv2.waitKey(3)


if __name__ == '__main__':
  img_topic = '/camera/image/compressed'

  rospy.init_node('line_follower')
  twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
  rospy.SubscribeListener(img_topic, CompressedImage, img_callback)


  rate = rospy.Rate(10)
  g_twist = Twist()
  while not rospy.is_shutdown():
    twist_pub.publish(g_twist)
    rate.sleep()
  rospy.spin()

