cmake_minimum_required(VERSION 2.8.3)
project(leap_motion2)

find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs geometry_msgs message_generation)

add_message_files(
    FILES 
    LeapData.msg
    Hand.msg
)

generate_messages(DEPENDENCIES
    std_msgs
    geometry_msgs
)

catkin_package(
    INCLUDE_DIRS include
    CATKIN_DEPENDS roscpp rospy std_msgs message_runtime
)

include_directories(include
    ${catkin_INCLUDE_DIRS}
)

install(PROGRAMS 
    scripts/leap_motion2_node.py scripts/leap_listener.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

