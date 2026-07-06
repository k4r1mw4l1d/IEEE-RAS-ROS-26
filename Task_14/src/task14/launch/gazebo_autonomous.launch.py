from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    pkg = get_package_share_directory("task14")

    world = os.path.join(pkg, "worlds", "task14_world.sdf")

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py"
            )
        ),
        launch_arguments={
            "gz_args": world
        }.items(),
    )

    spawn = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-file",
            "/opt/ros/jazzy/share/turtlebot3_gazebo/models/turtlebot3_burger/model.sdf",
            "-name",
            "burger",
            "-x",
            "0",
            "-y",
            "0",
            "-z",
            "0.1",
        ],
        output="screen",
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
            "/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist",
            "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
            "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
        ],
        output="screen",
    )

    controller = Node(
        package="task14",
        executable="autonomous_mover",
        output="screen",
    )

    return LaunchDescription([
        gazebo,
        spawn,
        bridge,
        controller,
    ])
