import rclpy
from rclpy.node import Node 


class Subscriber(Node):
    def __init__(self):
        super().__init__('my_subscriber')



def main():
    rclpy.init()
    node = Subscriber()
    rclpy.spin(node)
    node.destroy_node()

    rclpy.shutdown()