# Author: Karim Walid
# Date: 15/5/2026

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Int32
import math


FLEET_ROBOT_IDS = ["robot_1", "robot_2", "robot_3"]

MY_ROBOT_ID  = "robot_0"
MY_START_X   = 1.0
MY_START_Y   = 1.0
MY_THETA     = 0.0
MY_PRIORITY  = 4

SAFETY_ZONE  = 2.0
PUBLISH_RATE = 10

class TrafficManager(Node):
    def __init__(self):
        super().__init__(MY_ROBOT_ID)

        self.my_x        = MY_START_X
        self.my_y        = MY_START_Y
        self.my_theta    = MY_THETA
        self.my_priority = MY_PRIORITY
        self.fleet = {
            rid: {'pose': None, 'priority': None}
            for rid in FLEET_ROBOT_IDS
        }
        self.pose_pub = self.create_publisher(
            Pose2D,
            f'/{MY_ROBOT_ID}/pose',
            10
        )

        self.priority_pub = self.create_publisher(
            Int32,
            f'/{MY_ROBOT_ID}/priority',
            10
        )
        for rid in FLEET_ROBOT_IDS:
            self.create_subscription(
                Pose2D,
                f'/{rid}/pose',
                self._make_pose_callback(rid),
                10
            )
            self.create_subscription(
                Int32,
                f'/{rid}/priority',
                self._make_priority_callback(rid),
                10
            )
            self.timer = self.create_timer(1.0 / PUBLISH_RATE, self.tick)

        self.get_logger().info(
            f"[{MY_ROBOT_ID}] started — "
            f"pos=({MY_START_X},{MY_START_Y}) "
            f"priority={MY_PRIORITY} "
            f"safety_zone={SAFETY_ZONE}m"
        )

    def _make_pose_callback(self, robot_id):
        def callback(msg):
            self.fleet[robot_id]['pose'] = msg
        return callback

    def _make_priority_callback(self, robot_id):
        def callback(msg):
            self.fleet[robot_id]['priority'] = msg.data
        return callback
    
    def tick(self):
        self._broadcast_self()
        self._yielding_protocol()

    def _broadcast_self(self):
        pose_msg       = Pose2D()
        pose_msg.x     = self.my_x
        pose_msg.y     = self.my_y
        pose_msg.theta = self.my_theta
        self.pose_pub.publish(pose_msg)

        priority_msg      = Int32()
        priority_msg.data = self.my_priority
        self.priority_pub.publish(priority_msg)

    def _yielding_protocol(self):
        any_danger = False

        for rid, data in self.fleet.items():
            pose     = data['pose']
            priority = data['priority']

            if pose is None or priority is None:
                continue

            dx       = pose.x - self.my_x
            dy       = pose.y - self.my_y
            distance = math.sqrt(dx**2 + dy**2)

            in_safety_zone  = distance < SAFETY_ZONE
            higher_priority = priority > self.my_priority

            if in_safety_zone and higher_priority:
                self.get_logger().warn(
                    f"[DANGER] {rid} is {distance:.2f}m away "
                    f"(priority {priority} > mine {self.my_priority}) — YIELDING"
                )
                any_danger = True
            else:
                reason = (
                    f"dist={distance:.2f}m"
                    if not in_safety_zone
                    else f"priority {priority} <= mine {self.my_priority}"
                )
                self.get_logger().info(
                    f"[CLEAR]  {rid} — {reason}"
                )

        if not any_danger:
            self.get_logger().info(
                "[CLEAR] All paths clear — no yielding needed."
            )


def main():
    rclpy.init()
    node = TrafficManager()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
	print("Abort")
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
