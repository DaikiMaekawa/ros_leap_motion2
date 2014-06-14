#!/usr/bin/env python

import rospy
from leap_motion2.msg import Hand

import Leap
import leap_listener

def publish_hands_data(pub, frame):
    for hand in frame.hands:
        hand_msg = Hand()
        
        hand_type = "left_hand" if hand.is_left else "right_hand"
        #print "  %s, id %d, position: %s" % (
        #    hand_type, hand.id, hand.palm_position)

        hand_msg.header.frame_id = hand_type
        
        normal = hand.palm_normal
        direction = hand.direction
        pos = hand.palm_position
    
        hand_msg.direction.x = direction.x
        hand_msg.direction.y = direction.y
        hand_msg.direction.z = direction.z
        hand_msg.normal.x = normal.x
        hand_msg.normal.y = normal.y
        hand_msg.normal.z = normal.z
        hand_msg.palmpos.x = pos.x * 0.01
        hand_msg.palmpos.y = pos.y * 0.01
        hand_msg.palmpos.z = pos.z * 0.01

        #hand_msg.ypr.x = direction.pitch * Leap.RAD_TO_DEG
        #hand_msg.ypr.y = normal.yaw * Leap.RAD_TO_DEG
        #hand_msg.ypr.z = direction.roll * Leap.RAD_TO_DEG
        
        hand_msg.ypr.x = direction.pitch * Leap.RAD_TO_DEG
        hand_msg.ypr.y = normal.roll * Leap.RAD_TO_DEG
        hand_msg.ypr.z = direction.yaw * Leap.RAD_TO_DEG

        print "ypr: "
        print hand_msg.ypr

        pub.publish(hand_msg)

def main():
    rospy.init_node('leap_motion2')
    pub = rospy.Publisher("leapmotion2/data", Hand)
    
    listener = leap_listener.LeapListener()
    controller = Leap.Controller()
    controller.add_listener(listener)

    rate = rospy.Rate(100)
    
    while not rospy.is_shutdown():
        if controller.is_connected:
            frame = controller.frame()
            hands = publish_hands_data(pub, frame) 

        rate.sleep()
    else:
        controller.remove_listener(listener)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

