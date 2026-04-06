import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def _launch_setup(context):
    model = LaunchConfiguration("model").perform(context)

    package_path = get_package_share_directory("h12_ros2_model")
    asset_path = f"{package_path}/assets"
    urdf_filename = "h1_2_ros.urdf" if model == "inspire" else "h1_2_handless_ros.urdf"
    urdf_ros_path = f"{asset_path}/h1_2/{urdf_filename}"
    rviz_config_path = f"{package_path}/rviz/default.rviz"

    with open(urdf_ros_path, "r") as urdf_file:
        robot_description = urdf_file.read()

    return [
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            parameters=[{"robot_description": robot_description}],
            output="screen",
        ),
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            name="joint_state_publisher_gui",
            output="screen",
        ),
        TimerAction(
            period=1.0,
            actions=[
                Node(
                    package="rviz2",
                    executable="rviz2",
                    name="rviz2",
                    arguments=["-d", rviz_config_path]
                    if os.path.exists(rviz_config_path)
                    else [],
                    output="screen",
                )
            ],
        ),
    ]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "model",
                default_value="handless",
                choices=["handless", "inspire"],
                description="Robot model variant",
            ),
            OpaqueFunction(function=_launch_setup),
        ]
    )
