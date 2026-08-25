import rclpy
from rclpy.node import Node #导入之后可以写出ros2 节点，发布者，订阅者，定时器
from geometry_msgs.msg import Twist#geometry_msgs消息功能包，包含几何相关信息
'''
geometry_msgs/
└─ msg/
   ├─ Twist.msg     # 原始消息定义文件！写着linear、angular字段
   ├─ Vector3.msg
   └─ Pose.msg

from geometry_msgs.msg import Twist
# 直接把Twist拿到当前作用域，后面直接写 Twist()
msg = Twist()

import geometry_msgs.msg
msg = geometry_msgs.msg.Twist()

'''

class TurtleControl(Node):
    def __init__(self):
        super().__init__('Tur_control')#以Node形式初始化，起名字，ros2 node list中会列出'Tur_control'
        self.publisher_  =  self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        '''
        左侧self.publisher_自定义变量名，以后用此名发布消息
        self.create_publisher(...)，rclpy自带的方法，现成的直接用
        三个参数：
        Twist 消息类型:Twist意味着控制速度

        '/turtle1/cmd_vel':topic list中列出的话题，使这段代码作用于海龟
        
        10:发布者(你的节点)发的速度指令,是先丢进一个小仓库,
        再送到订阅者(海龟)。10 = 这个小仓库最多暂存 10 条还未来得及送出去的消息。
        改小:只保留最近消息，丢弃老消息
        ''' 
        self.timer = self.create_timer(0.1,self.timer_callback)#定时器，每隔0.1s执行time_callback函数
        self.get_logger().info(f'Tur_control,启动! ')


    def timer_callback(self):
        msg = Twist()#初始化
        msg.linear.x = 2.0
        msg.angular.z = 1.5
        self.publisher_.publish(msg)#每0.1s被唤醒，按照self.publisher_的规定格式发布

        count = self.publisher_.get_subscription_count()
        if count == 0:
            self.get_logger().warn(f'还没有节点接收速度指令!')
        else:
            self.get_logger().info(f'已连接 {count} 个接收者(turtlesim),海龟应开始画圆')
        '''
        确切地检测小海龟到底有没有接收到Control命令
        只报Tur_control启动不能保证小海龟真的接收到发布者发布的消息
        '''

def main():
    rclpy.init()#ros2环境初始化
    node = TurtleControl()
    '''
    如果这里采用node = TurtleControl('Tur_control')
    则类中必须改为
    def __init__(self,node_name):
        super().__init__(node_name)
    '''
    rclpy.spin(node)#持续运行
    node.destroy_node()#销毁节点
    rclpy.shutdown()#清除环境 