import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():#产生launch描述

    params_yaml = os.path.join(
        get_package_share_directory('chapter3_pkg'),'config','params.yaml'
    )#得到配置文件绝对路径，与setup.py line16~17有联系，从install/.../share中找params.yaml

    '''填actions，当ros2 launch chapter3_pkg test.launch.py时，执行以下内容
    return返回给ros2 launch 的系统库(launch_ros NodeAction)    
    '''
    return LaunchDescription([
        #先后执行以下两个Node
        # 发布节点
        Node(
            package='chapter3_pkg',#第一个参数功能包名字
            executable='publisher',#第二个参数可执行文件名字
            name='my_publisher',#必须和yaml中的名字对应
            parameters=[params_yaml],#应用和yaml中的名字对应的yaml参数
            output='screen',#日志，输出到屏幕
        ),
        # 订阅节点
        Node(
            package='chapter3_pkg',
            executable='subscriber',
            name='my_subscriber',
            parameters=[params_yaml],
            output='screen',
        ),
        '''
        这里只是产生清单，真正负责执行的是ros2 launch 的系统库(launch_ros NodeAction)
        '''
    ])