import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    safety_zone_arg = DeclareLaunchArgument(
        'safety_zone',
        default_value='2.0',
        description='Safety distance buffer radius'
    )
    
    robot_priority_arg = DeclareLaunchArgument(
        'robot_priority',
        default_value='4',
        description='Priority value for robot_0'
    )
    
    robot_x_arg = DeclareLaunchArgument(
        'robot_x',
        default_value='1.0',
        description='Initial X position of robot_0'
    )
    
    robot_y_arg = DeclareLaunchArgument(
        'robot_y',
        default_value='1.0',
        description='Initial Y position of robot_0'
    )

    fleet_emulator_node = Node(
        package='fleet_emulator2',
        executable='robot_emulator_node',
        name='fleet_emulator',
        output='screen'
    )

    traffic_manager_node = Node(
        package='fleet_emulator2',
        executable='traffic_manager_node',
        name='traffic_manager',
        output='screen',
        parameters=[{
            'safety_zone': LaunchConfiguration('safety_zone'),
            'my_priority': LaunchConfiguration('robot_priority'),
            'my_start_x': LaunchConfiguration('robot_x'),
            'my_start_y': LaunchConfiguration('robot_y')
        }]
    )

    return LaunchDescription([
        safety_zone_arg,
        robot_priority_arg,
        robot_x_arg,
        robot_y_arg,
        fleet_emulator_node,
        traffic_manager_node
    ])