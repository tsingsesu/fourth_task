import rclpy
import random
from rclpy.node import Node 
from std_msgs.msg import Float64MultiArray

class Publisher(Node):
    def __init__(self):
        super().__init__('my_publisher')
        self.pub = self.create_publisher(Float64MultiArray,'data',10)


    def timer_callback(self):
        pass

def main():
    rclpy.init()
    node = Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()