import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    package_path = get_package_share_directory('h12_ros2_model')
    asset_path = f'{package_path}/assets'
    urdf_ros_path = f'{asset_path}/h1_2/h1_2_ros.urdf'
    rviz_config_path = f'{package_path}/rviz/default.rviz'

    with open(urdf_ros_path, 'r') as urdf_file:
        robot_description = urdf_file.read()

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),
        TimerAction(  # slight delay to ensure robot_description is set
            period=1.0,
            actions=[
                Node(
                    package='rviz2',
                    executable='rviz2',
                    name='rviz2',
                    arguments=['-d', rviz_config_path] if os.path.exists(rviz_config_path) else [],
                    output='screen'
                )
            ]
        )
    ])
