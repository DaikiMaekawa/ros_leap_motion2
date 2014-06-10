#!/usr/bin/env python

import rospy
import Leap
import leap_listener

def main():
    rospy.init_node('leap_motion2')
    
    listener = leap_listener.LeapListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    
    while not rospy.is_shutdown():
        if controller.is_connected:
            frame = controller.frame()
            for hand in frame.hands:
                hand_type = "Left hand" if hand.is_left else "Right hand"
                print "  %s, id %d, position: %s" % (
                    hand_type, hand.id, hand.palm_position)

        rospy.sleep(0.01)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

