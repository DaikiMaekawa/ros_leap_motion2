#!/usr/bin/env python

import rospy
from leap_motion2.msg import LeapData
from leap_motion2.msg import Hand

import Leap
import leap_listener

def convert_frame_to_msg(frame):
    leap_data_msg = LeapData()
    for hand in frame.hands:
        hand_msg = Hand()
        
        hand_type = "Left hand" if hand.is_left else "Right hand"
        print "  %s, id %d, position: %s" % (
            hand_type, hand.id, hand.palm_position)

        normal = hand.palm_normal
        direction = hand.direction
        pos = hand.palm_position
    
        hand_msg.direction.x = direction.x
        hand_msg.direction.y = direction.y
        hand_msg.direction.z = direction.z
        hand_msg.normal.x = normal.x
        hand_msg.normal.y = normal.y
        hand_msg.normal.z = normal.z
        hand_msg.palmpos.x = pos.x
        hand_msg.palmpos.y = pos.y
        hand_msg.palmpos.z = pos.z

        hand_msg.ypr.x = direction.pitch * Leap.RAD_TO_DEG
        hand_msg.ypr.y = normal.yaw * Leap.RAD_TO_DEG
        hand_msg.ypr.z = direction.roll * Leap.RAD_TO_DEG

        leap_data_msg.hands.append(hand_msg)
    
    return leap_data_msg

def main():
    rospy.init_node('leap_motion2')
    pub = rospy.Publisher("leapmotion2/data", LeapData)
    
    listener = leap_listener.LeapListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    
    while not rospy.is_shutdown():
        if controller.is_connected:
            frame = controller.frame()
            msg = convert_frame_to_msg(frame) 
            pub.publish(msg)

        rospy.sleep(0.01)
    else:
        controller.remove_listener(listener)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

