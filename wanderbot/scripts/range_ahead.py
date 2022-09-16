#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

# BEGIN MEASUREMENT
def scan_callback(msg):
  range_ahead = msg.ranges[len(msg.ranges)/2]
  #closest_range = min(msg.ranges)
  print("range ahead : %0.1f" % range_ahead)
  # END MEASUREMENT


rospy.init_node('range_ahead')
scan_sub = rospy.SubscribeListener('scan', LaserScan, scan_callback)
rospy.spin()


