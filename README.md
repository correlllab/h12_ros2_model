# h12_ros2_model

ROS2 package of h12 robot description.

## File

- Robot description files are located under `assets/` directory.
- `assets/h1_2/h1_2.urdf` contains description with relative mesh path, suitable for libraries like Pinocchio.
- `assets/h1_2/h1_2_ros.urdf` contains description with package mesh path, suitable for ROS integration.

## Dependencies

- This package depends on `robot_description_publisher`, `joint_state_publisher` and `joint_state_publisher_gui`
- Taking ros2 humble as an example, you can install these dependencies by:

    ```bash
    sudo apt install ros-humble-robot-state-publisher
    sudo apt install ros-humble-joint-state-publisher
    sudo apt install ros-humble-joint-state-publisher-gui
    ```

## Usage

- Building this package in your workscape and all the assets will be available at run time.

    ```python
    from ament_index_python.packages import get_package_share_directory

    package_path = get_package_share_directory('h12_ros2_model')
    print(f'Asset file: {package_path}/assets/{asset_file}')
    ```

- Running `ros2 launch h12_ros2_model robot_description_launch.py` will start the `robot_state_publisher` node,
  the `joint_state_publisher_gui` node and `rviz` to visualize the robot.
- In `rviz`, you can view the robot by adding a `RobotModel` visualization and subscribe to `robot_description` topic.
- On actual robot, you may want to implement your own joint state publisher to track the real joint positions.
