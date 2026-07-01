import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/karims/Desktop/IEEE-RAS-ROS-26/Task_13/install/fleet_emulator2'
