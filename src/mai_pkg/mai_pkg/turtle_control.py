import rclpy
from rclpy.node import Node 
from geometry_msgs.msg import Twist

class TurtleControl(Node):
    def __init__(self):
        super().__init__('Tur_control')
        self.publisher_  =  self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1,self.timer_callback)#定时器，每隔0.1s执行time_callback函数
        self.get_logger().info(f'Tur_control,启动! ')

    def timer_callback(self):#每0.1s被唤醒
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.5
        self.publisher_.publish(msg)#按照self.publisher_的规定格式发布

        count = self.publisher_.get_subscription_count()
        if count == 0:
            self.get_logger().warn(f'还没有节点接收速度指令!')
        else:
            self.get_logger().info(f'已连接 {count} 个接收者(turtlesim),海龟应开始画圆')


def main():
    rclpy.init()
    node = TurtleControl()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()