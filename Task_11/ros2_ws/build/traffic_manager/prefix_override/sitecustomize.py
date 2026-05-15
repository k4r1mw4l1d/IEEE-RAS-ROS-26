import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/karims/Desktop/IEEE-RAS-ROS-26/Task_11/ros2_ws/install/traffic_manager'
