from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'chapter3_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),#resource/chapter3_pkg，在ros2 launch chapter3_pkg test.launch.py中的chapter3_pkg发挥作用 
        ('share/' + package_name, ['package.xml']),

        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),#装launch文件路径，让launch文件能够被找到，在ros2 launch chapter3_pkg test.launch.py中的test.launch.py发挥作用 
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        #把config/params.yaml安装到install/.../share，提供路径
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lhl87',
    maintainer_email='tsingsesu@163.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'publisher = chapter3_pkg.publisher:main',
            'subscriber = chapter3_pkg.subscriber:main',

        ],
    },
)
