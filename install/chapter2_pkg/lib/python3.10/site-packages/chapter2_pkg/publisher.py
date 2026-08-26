import rclpy
import random
from rclpy.node import Node 
from std_msgs.msg import Float64MultiArray , String

class Publisher(Node):
    def __init__(self):
        super().__init__('my_publisher')
        self.pub = self.create_publisher(Float64MultiArray,'data',10)
        self.timer = self.create_timer(1.0,self.timer_callback)
        self.seq = 0
        self.status_pub = self.create_publisher(String , 'status',10)

    def timer_callback(self):
        self.seq = self.seq + 1
        msg = Float64MultiArray()
        msg.data = [
            float(self.seq),
            random.uniform(-7.0,7.0),
            random.uniform(10.5,12.6),
            random.uniform(25.0,48.0),
        ]
        self.pub.publish(msg)

        if self.seq >= 10:
            end = String()
            end.data = 'done'
            self.status_pub.publish(end)
            self.get_logger().info('已发完10组并发送结束信号')
            self.timer.cancel() 


def main():
    rclpy.init()
    node = Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()