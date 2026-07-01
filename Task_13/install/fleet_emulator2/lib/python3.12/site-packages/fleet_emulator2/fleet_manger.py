import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Int32
import math

FLEET_ROBOT_IDS = ["robot_1", "robot_2", "robot_3"]

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
        super().__init__('robot_0')

        self.declare_parameter('my_start_x', 1.0)
        self.declare_parameter('my_start_y', 1.0)
        self.declare_parameter('my_theta', 0.0)
        self.declare_parameter('my_priority', 4)
        self.declare_parameter('safety_zone', 2.0)
        self.declare_parameter('publish_rate', 10.0)

        self.my_x = self.get_parameter('my_start_x').value
        self.my_y = self.get_parameter('my_start_y').value
        self.my_theta = self.get_parameter('my_theta').value
        self.my_priority = self.get_parameter('my_priority').value
        self.safety_zone = self.get_parameter('safety_zone').value
        
        self.pose_msg = Pose2D()
        self.prio_msg = Int32()
        self.prio_msg.data = self.my_priority

        self.pose_pub = self.create_publisher(Pose2D, '/robot_0/pose', 10)
        self.priority_pub = self.create_publisher(Int32, '/robot_0/priority', 10)

        self.fleet = {}
        for rid in FLEET_ROBOT_IDS:
            tracker = FleetTracker()
            self.fleet[rid] = tracker
            self.create_subscription(Pose2D, f'/{rid}/pose', tracker.update_pose, 10)
            self.create_subscription(Int32, f'/{rid}/priority', tracker.update_priority, 10)

        rate = self.get_parameter('publish_rate').value
        self.timer = self.create_timer(1.0 / rate, self.tick)
        self.get_logger().info(f"[robot_0] Operational. Safety Zone: {self.safety_zone}m")

    def tick(self):
        self.pose_msg.x = self.my_x
        self.pose_msg.y = self.my_y
        self.pose_msg.theta = self.my_theta
        self.pose_pub.publish(self.pose_msg)
        self.priority_pub.publish(self.prio_msg)

        any_danger = False

        for rid, tracker in self.fleet.items():
            if not tracker.is_valid:
                continue

            dx = tracker.pose.x - self.my_x
            dy = tracker.pose.y - self.my_y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < self.safety_zone and tracker.priority > self.my_priority:
                self.get_logger().warn(
                    f"[DANGER] {rid} detected at {distance:.2f}m with higher priority ({tracker.priority}) — YIELDING"
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