# Author: Karim Walid
# Date: 15/5/2026

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Int32

ROBOTS = [
    ("robot_1",   0.0,  0.0,  0.0,   5,        0.02,  0.0),
    ("robot_2",   5.0,  5.0,  1.57,  8,       -0.02,  0.0),
    ("robot_3",  -3.0,  4.0,  3.14,  3,        0.0,   0.02),
]

PUBLISH_RATE_HZ = 10

class RobotEmulator(Node):
    def __init__(self, robot_id, x, y, theta, priority, dx, dy):
        super().__init__(robot_id)
        self.robot_id = robot_id
        self.x        = x
        self.y        = y
        self.theta    = theta
        self.priority = priority
        self.dx       = dx
        self.dy       = dy

        self.pose_pub = self.create_publisher(
            Pose2D,
            f'/{robot_id}/pose',
            10
        )

        self.priority_pub = self.create_publisher(
            Int32,
            f'/{robot_id}/priority',
            10
        )

        period = 1.0 / PUBLISH_RATE_HZ
        self.timer = self.create_timer(period, self.broadcast)

        self.get_logger().info(
            f"[{robot_id}] started — pos=({x:.1f},{y:.1f}) priority={priority}"
        )

    def broadcast(self):
        self.x += self.dx
        self.y += self.dy

        pose_msg       = Pose2D()
        pose_msg.x     = self.x
        pose_msg.y     = self.y
        pose_msg.theta = self.theta
        self.pose_pub.publish(pose_msg)

        priority_msg      = Int32()
        priority_msg.data = self.priority
        self.priority_pub.publish(priority_msg)


if __name__ == '__main__':
    rclpy.init()

    nodes = []
    for (rid, x, y, theta, prio, dx, dy) in ROBOTS:
        node = RobotEmulator(rid, x, y, theta, prio, dx, dy)
        nodes.append(node)

    from rclpy.executors import MultiThreadedExecutor
    executor = MultiThreadedExecutor()
    for node in nodes:
        executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        for node in nodes:
            node.destroy_node()
        rclpy.shutdown()

