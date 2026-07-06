#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class AutonomousMover(Node):

    def __init__(self):
        super().__init__("autonomous_mover")

        self.publisher = self.create_publisher(Twist, "/cmd_vel", 10)
        self.timer = self.create_timer(0.1, self.control_loop)

        self.state = 0
        self.counter = 0

        self.get_logger().info("Autonomous Mover Started")

    def control_loop(self):
        msg = Twist()

        if self.state == 0:
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.counter += 1
            if self.counter >= 150:
                self.counter = 0
                self.state = 1

        elif self.state == 1:
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.counter += 1
            if self.counter >= 31:
                self.counter = 0
                self.state = 2

        elif self.state == 2:
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.counter += 1
            if self.counter >= 80:
                self.counter = 0
                self.state = 3

        elif self.state == 3:
            msg.linear.x = 0.0
            msg.angular.z = -0.5
            self.counter += 1
            if self.counter >= 31:
                self.counter = 0
                self.state = 4

        elif self.state == 4:
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.counter += 1
            if self.counter >= 150:
                self.counter = 0
                self.state = 5

        elif self.state == 5:
            msg.linear.x = 0.0
            msg.angular.z = -0.5
            self.counter += 1
            if self.counter >= 31:
                self.counter = 0
                self.state = 6

        elif self.state == 6:
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.counter += 1
            if self.counter >= 150:
                self.counter = 0
                self.state = 7

        elif self.state == 7:
            msg.linear.x = 0.0
            msg.angular.z = -0.5
            self.counter += 1
            if self.counter >= 31:
                self.counter = 0
                self.state = 8

        elif self.state == 8:
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.counter += 1
            if self.counter >= 80:
                self.counter = 0
                self.state = 9
                

        elif self.state == 9:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = AutonomousMover()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    stop = Twist()
    node.publisher.publish(stop)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()