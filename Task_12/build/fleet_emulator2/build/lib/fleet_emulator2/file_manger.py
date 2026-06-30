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

class FleetTracker:
    def __init__(self):
        self.pose = None
        self.priority = None

    def update_pose(self, msg):
        self.pose = msg

    def update_priority(self, msg):
        self.priority = msg.data

    @property
    def is_valid(self):
        return self.pose is not None and self.priority is not None


class TrafficManager(Node):
    def __init__(self):
        super().__init__(MY_ROBOT_ID)

        self.my_x        = MY_START_X
        self.my_y        = MY_START_Y
        self.my_theta    = MY_THETA
        self.my_priority = MY_PRIORITY
        
        self._pose_msg = Pose2D()
        self._prio_msg = Int32()
        self._prio_msg.data = self.my_priority

        self.pose_pub = self.create_publisher(Pose2D, f'/{MY_ROBOT_ID}/pose', 10)
        self.priority_pub = self.create_publisher(Int32, f'/{MY_ROBOT_ID}/priority', 10)

        self.fleet = {}
        for rid in FLEET_ROBOT_IDS:
            tracker = FleetTracker()
            self.fleet[rid] = tracker
            
            self.create_subscription(Pose2D, f'/{rid}/pose', tracker.update_pose, 10)
            self.create_subscription(Int32, f'/{rid}/priority', tracker.update_priority, 10)

        self.timer = self.create_timer(1.0 / PUBLISH_RATE, self.tick)
        self.get_logger().info(f"[{MY_ROBOT_ID}] Operational. Safety Zone: {SAFETY_ZONE}m")

    def tick(self):
        self._pose_msg.x = self.my_x
        self._pose_msg.y = self.my_y
        self._pose_msg.theta = self.my_theta
        self.pose_pub.publish(self._pose_msg)
        self.priority_pub.publish(self._prio_msg)

        any_danger = False

        for rid, tracker in self.fleet.items():
            if not tracker.is_valid:
                continue

            dx = tracker.pose.x - self.my_x
            dy = tracker.pose.y - self.my_y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < SAFETY_ZONE and tracker.priority > self.my_priority:
                self.get_logger().warn(
                    f"[YIELD] {rid} detected at {distance:.2f}m with higher priority ({tracker.priority})"
                )
                any_danger = True

        if not any_danger:
            self.get_logger().info("[CLEAR] Path is clear.", throttle_duration_sec=2.0)


def main():
    rclpy.init()
    node = TrafficManager()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nAborting environment Execution")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()