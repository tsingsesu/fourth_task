import rclpy
import random
from rclpy.node import Node 
from std_msgs.msg import Float64MultiArray , String

class Publisher(Node):
    def __init__(self):
        super().__init__('my_publisher')
        self.finished = False
        
        self.declare_parameter('test_count',5)#声明
        self.declare_parameter('publish_period',0.5)

        self.test_count = self.get_parameter('test_count').value#读取
        self.publish_period = self.get_parameter('publish_period').value

        if self.test_count < 1:
            self.get_logger().error(f'测试数据数量不能小于1,当前{self.test_count},已重置为5')
            self.test_count = 5

        if self.publish_period <= 0:
            self.get_logger().error(f'发布周期必须>0,当前{self.publish_period},已重置为0.5')
            self.publish_period = 0.5
        
        self.pub = self.create_publisher(Float64MultiArray,'data',10)
        self.timer = self.create_timer(self.publish_period,self.timer_callback)#发布周期改为参数
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

        if self.seq >= self.test_count:#测试数据发布数量改为参数
            self.timer.cancel()
            self.done_timer = self.create_timer(0.3, self.send_done)

    def send_done(self):
        end = String()
        end.data = 'done'
        self.status_pub.publish(end)
        self.get_logger().info('已发完10组并发送结束信号')
        self.done_timer.cancel()
        self.finished = True

def main():
    rclpy.init()
    node = Publisher()
    while rclpy.ok() and not node.finished:
        rclpy.spin_once(node, timeout_sec=0.2)
    node.destroy_node()
    rclpy.shutdown()
