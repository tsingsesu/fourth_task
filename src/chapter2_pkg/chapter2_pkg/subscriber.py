import rclpy
from rclpy.node import Node 
from std_msgs.msg import Float64MultiArray , String

class Subscriber(Node):
    def __init__(self):
        super().__init__('my_subscriber')
        self.finished = False #，指示器，rclpy.spin()会使终端无法自动结束，因此手动检测任务是否完成
        self.count = 0#得到的数据总数（去除异常error数据）
        self.warningmsg = 0#风险数据数量
        self.effectivemsg = 0#有效数据数量
        self.deviation_sum = 0#平衡偏差绝对值总和
        self.last_seq = 0#前一个数据序号，用于检测数据序号是否连续
        self.gap_num  = 0#跳号（不连续）次数
        self.sub = self.create_subscription(Float64MultiArray,'data',self.statistics_callback,10)#以Float64MultiArray形式订阅消息，同时调用统计函数进行处理
        self.sub2 = self.create_subscription(String, 'status', self.status_callback, 10)#接收消息发布完成

    def error_check(self,msg):#先对数据进行筛选，剔除异常数据

        if len(msg.data) != 4:#剔除格式异常数据
            self.get_logger().error(f'格式错误：数据长度={len(msg.data)}不为4,已丢弃')
            return None
        
        seq = int(msg.data[0])
        angle = msg.data[1]
        voltage = msg.data[2]
        temperature = msg.data[3]

        if (angle > 7.0 or angle < -7.0 
            or voltage < 10.5 or voltage >12.6 
            or temperature > 48.0 or temperature < 25.0):#剔除内容异常数据
            self.get_logger().error(f'数据异常:角度{angle:.2f}° \
            电压{voltage:.2f}V 温度{temperature:.2f}℃ 超出范围,已丢弃')
            return None

        if seq != self.last_seq + 1:#检测序号是否连续
            self.get_logger().error(f'序号出现跳号:本应 {self.last_seq+1},实际 {seq},仍计入统计')
            self.gap_num = self.gap_num + 1
        self.last_seq = seq
        return seq, angle, voltage, temperature

    def statistics_callback(self,msg):#统计函数
        realmsg = self.error_check(msg)#先对接听到的数据进行筛选
        if realmsg is None:
            return
        seq, angle, voltage, temperature, = realmsg#解包

        self.get_logger().info(f'第{seq}次前置测试：平衡误差{angle:.2f}°，核心电压 {voltage:.2f} V，核心温度 {temperature:.1f}℃')

        self.count += 1 #统计总数

        if angle > 5.0 or angle < -5.0 or voltage < 11 or temperature > 42.0:#统计风险数据
            self.warningmsg = self.warningmsg + 1

        if angle >= 0:#计算角度偏差绝对值之和
            self.deviation_sum = self.deviation_sum + angle
        if angle < 0:
            self.deviation_sum = self.deviation_sum - angle

    def status_callback(self, msg):#发布统计信息函数
        if msg.data == 'done':
            self.effectivemsg = self.count-self.warningmsg
            log = self.get_logger()
            log.info(f'前置测试完成：共收到{self.count}条状态')
            log.info(f'其中共收到：{self.effectivemsg}条有效状态（无风险）')
            log.info(f'平衡偏差绝对值总和：{self.deviation_sum:.2f}°')
            log.info(f'平均平衡偏差：{self.deviation_sum/self.count:.2f}°')
            if self.warningmsg > 0:
                log.warn(f'存在风险的状态：{self.warningmsg}条')  
            else:
                log.info(f'无存在风险的状态')

            if self.gap_num > 0:
                log.warn(f'出现序号不连续：{self.gap_num}次')
            else:
                log.info(f'序号均连续')
            log.info(f'测试数据已经记录')
            self.finished = True

def main():
    rclpy.init()
    node = Subscriber()
    while rclpy.ok() and not node.finished:#wsl中rclpy.spin()会使终端无法自动结束，因此手动检测任务是否完成
        rclpy.spin_once(node, timeout_sec=0.2)
    node.destroy_node()
    rclpy.shutdown()


