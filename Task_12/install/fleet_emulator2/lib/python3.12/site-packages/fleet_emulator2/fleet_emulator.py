import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Int32
from rclpy.executors import SingleThreadedExecutor

FLEET_CONFIG = {
    "robot_1": {"x": 1.5,  "y": 1.5,  "theta": 0.0,  "prio": 5, "dx": -0.01, "dy": -0.01},
    "robot_2": {"x": 2.3,  "y": 2.3,  "theta": 1.57, "prio": 8, "dx": -0.05, "dy": -0.05},
    "robot_3": {"x": 1.1,  "y": 1.1,  "theta": 3.14, "prio": 2, "dx": 0.01,  "dy": 0.01},
}

class LifecycleRobotEmulator(Node):
    def __init__(self, node_name, config):
        super().__init__(node_name)
        
        self.declare_parameter('x', config['x'])
        self.declare_parameter('y', config['y'])
        self.declare_parameter('theta', config['theta'])
        self.declare_parameter('priority', config['prio'])
        self.declare_parameter('dx', config['dx'])
        self.declare_parameter('dy', config['dy'])
        self.declare_parameter('publish_rate', 10.0)

        self._pose_msg = Pose2D()
        self._prio_msg = Int32()
        
        self._x = self.get_parameter('x').value
        self._y = self.get_parameter('y').value
        self._theta = self.get_parameter('theta').value
        self._dx = self.get_parameter('dx').value
        self._dy = self.get_parameter('dy').value
        self._prio_msg.data = self.get_parameter('priority').value

        self.pose_pub = self.create_publisher(Pose2D, f'/{node_name}/pose', 10)
        self.prio_pub = self.create_publisher(Int32, f'/{node_name}/priority', 10)

        rate = self.get_parameter('publish_rate').value
        self.timer = self.create_timer(1.0 / rate, self.on_timer_tick)
        
        self.get_logger().info(f"Initialized {node_name} at ({self._x:.2f}, {self._y:.2f})")

    def on_timer_tick(self):
        self._x += self._dx
        self._y += self._dy

        self._pose_msg.x = self._x
        self._pose_msg.y = self._y
        self._pose_msg.theta = self._theta
        self.pose_pub.publish(self._pose_msg)

        self.prio_pub.publish(self._prio_msg)


def main(args=None):
    rclpy.init(args=args)
    
    executor = SingleThreadedExecutor()
    nodes = []

    try:
        for name, config in FLEET_CONFIG.items():
            node = LifecycleRobotEmulator(name, config)
            nodes.append(node)
            executor.add_node(node)
        
        executor.spin()
        
    except KeyboardInterrupt:
        print("\nShutting down robot emulation environment...")
    finally:
        for node in nodes:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()