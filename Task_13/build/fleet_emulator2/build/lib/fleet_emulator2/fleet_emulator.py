import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Int32
from rclpy.executors import SingleThreadedExecutor

class LifecycleRobotEmulator(Node):
    def __init__(self, node_name, default_x, default_y, default_theta, default_prio, dx, dy):
        super().__init__(node_name)
        
        self.declare_parameter('x', default_x)
        self.declare_parameter('y', default_y)
        self.declare_parameter('theta', default_theta)
        self.declare_parameter('priority', default_prio)
        self.declare_parameter('dx', dx)
        self.declare_parameter('dy', dy)
        self.declare_parameter('publish_rate', 10.0)

        self.pose_msg = Pose2D()
        self.prio_msg = Int32()
        
        self.x = self.get_parameter('x').value
        self.y = self.get_parameter('y').value
        self.theta = self.get_parameter('theta').value
        self.dx = self.get_parameter('dx').value
        self.dy = self.get_parameter('dy').value
        self.prio_msg.data = self.get_parameter('priority').value

        self.pose_pub = self.create_publisher(Pose2D, f'/{node_name}/pose', 10)
        self.prio_pub = self.create_publisher(Int32, f'/{node_name}/priority', 10)

        rate = self.get_parameter('publish_rate').value
        self.timer = self.create_timer(1.0 / rate, self.on_timer_tick)
        
        self.get_logger().info(f"Initialized {node_name} at ({self.x:.2f}, {self.y:.2f}) with priority {self.prio_msg.data}")

    def on_timer_tick(self):
        self.x += self.dx
        self.y += self.dy

        self.pose_msg.x = self.x
        self.pose_msg.y = self.y
        self.pose_msg.theta = self.theta
        self.pose_pub.publish(self.pose_msg)
        self.prio_pub.publish(self.prio_msg)

def main(args=None):
    rclpy.init(args=args)
    
    executor = SingleThreadedExecutor()
    
    robots_init_data = [
        ("robot_1", 1.5,  1.5,  0.0,  5, -0.01, -0.01),
        ("robot_2", 2.3,  2.3,  1.57, 8, -0.05, -0.05),
        ("robot_3", 1.1,  1.1,  3.14, 2,  0.01,  0.01),
    ]
    
    nodes = []
    try:
        for name, x, y, theta, prio, dx, dy in robots_init_data:
            node = LifecycleRobotEmulator(name, x, y, theta, prio, dx, dy)
            nodes.append(node)
            executor.add_node(node)
        
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        for node in nodes:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()