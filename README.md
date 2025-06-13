# h12_ros2_model

ROS2 package of h12 robot description.

## File

- Robot description files are located under `assets/` directory.
- `assets/h1_2/h1_2.urdf` contains description with relative mesh path, suitable for libraries like Pinocchio.
- `assets/h1_2/h1_2_ros.urdf` contains description with package mesh path, suitable for ROS integration.

## Usage

- Building this package in your workscape and all the assets will be available at run time.

    ```python
    from ament_index_python.packages import get_package_share_directory

    package_path = get_package_share_directory('h12_ros2_model')
    print(f'Asset file: {package_path}/assets/{asset_file}')
    ```

- Running `ros2 launch h12_ros2_model robot_description_launch.py` will start the `robot_state_publisher` node.
  On the actual system, this should be called on the robot itself just once.
- In `rviz`, you can view the robot by adding a `RobotModel` visualization and subscribe to `robot_description` topic.
