import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    params_yaml = os.path.join(
        get_package_share_directory('chapter3_pkg'),'config','params.yaml'
    )#得到配置文件绝对路径

    #声明
    test_count = LaunchConfiguration('test_count')
    publish_period = LaunchConfiguration('publish_period')
    balance_threshold = LaunchConfiguration('balance_threshold')
    low_voltage_threshold = LaunchConfiguration('low_voltage_threshold')
    high_temp_threshold = LaunchConfiguration('high_temp_threshold')

    return LaunchDescription([
        DeclareLaunchArgument('test_count', default_value='5', description='测试数据数量'),
        DeclareLaunchArgument('publish_period', default_value='0.5', description='发布周期'),
        DeclareLaunchArgument('balance_threshold', default_value='5.0', description='平衡偏差阈值'),
        DeclareLaunchArgument('low_voltage_threshold', default_value='11.0', description='低电压阈值'),
        DeclareLaunchArgument('high_temp_threshold', default_value='42.0', description='高温阈值'),

        # 发布节点:先加载 YAML,再用 launch 参数覆盖(后面覆盖优先)
        Node(
            package='chapter3_pkg',
            executable='publisher',
            name='my_publisher',
            parameters=[
                params_yaml,
                {'test_count': test_count, 'publish_period': publish_period},
            ],
            output='screen',
        ),
        # 订阅节点
        Node(
            package='chapter3_pkg',
            executable='subscriber',
            name='my_subscriber',
            parameters=[
                params_yaml,
                {'balance_threshold': balance_threshold,
                 'low_voltage_threshold': low_voltage_threshold,
                 'high_temp_threshold': high_temp_threshold},
            ],
            output='screen',
        ),
    ])