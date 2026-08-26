import rclpy
from rclpy.node import Node 
from std_msgs.msg import Float64MultiArray , String

class Subscriber(Node):
    def __init__(self):
        super().__init__('my_subscriber')
        self.count = 0
        self.warningmsg = 0
        self.sum = 0
        self.sub = self.create_subscription(Float64MultiArray,'data',self.print_callback,10)
        self.sub2 = self.create_subscription(String, 'status', self.status_callback, 10) 
        self.sub3 = self.create_subscription(Float64MultiArray,'data',self.check_callback,10)


    def print_callback(self,msg):
        seq = int(msg.data[0])
        angle = msg.data[1]
        voltage = msg.data[2]
        temperature = msg.data[3]
        print(f'第{seq}次前置测试：平衡误差{angle:.2f}°，核心电压 {voltage:.2f} V，核心温度 {temperature:.1f}℃')

    def check_callback(self,msg):
        angle = msg.data[1]
        voltage = msg.data[2]
        temperature = msg.data[3]
        self.count += 1 

        if angle > 5.0 or angle < -5.0 or voltage < 11 or temperature > 42.0:
            self.warningmsg = self.warningmsg + 1

        if angle >= 0:
            self.sum = self.sum + angle
        if angle < 0:
            self.sum = self.sum - angle

    def status_callback(self, msg):#msg是形参，和发布端取的名字无关系
        if msg.data == 'done':
            print(f'前置测试完成：共收到{self.count}条有效状态')
            print(f'有效状态数量 = {self.count-self.warningmsg}')
            print(f'平衡偏差绝对值总和 = {self.sum:.2f}')
            print(f'风险状态数量 = {self.warningmsg}') 


def main():
    rclpy.init()
    node = Subscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()