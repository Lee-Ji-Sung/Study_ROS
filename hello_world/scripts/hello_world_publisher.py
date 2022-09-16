#!/usr/bin/env python
# license removed for brevity


import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10) # chatter <- topic 이름
    rospy.init_node('talker', anonymous=True)   # talker <- node 이름 / anonymous <- 노드의 이름이 여러개인 경우, 자동으로 번호 붙여주는 기능
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():  # shutdown 되기 전까지 무한 루프
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)    # loginfo <-- 터미널 상에 출력
        pub.publish(hello_str)      # publish <-- 실제 publish 하는 기능
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
