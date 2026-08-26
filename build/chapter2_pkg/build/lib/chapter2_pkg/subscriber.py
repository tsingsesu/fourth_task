import rclpy
from rclpy.node import Node 
from std_msgs.msg import Float64MultiArray

class Subscriber(Node):
    def __init__(self):
        super().__init__('my_subscriber')
        self.sub = self.create_subscription(Float64MultiArray,'data',self.callback,10)

    def callback(self,msg):
        seq = int(msg.data[0])
        angle = msg.data[1]
        voltage = msg.data[2]
        temperature = msg.data[3]
        print(f'第{seq}次前置测试：平衡误差{angle:.2f}°，核心电压 {voltage:.2f} V，核心温度 {temperature:.1f}℃')


def main():
    rclpy.init()
    node = Subscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()