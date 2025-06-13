import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'h12_ros2_model'

data_files = [
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    ('share/' + package_name + '/launch', glob('launch/*.py')),
]
'''
Access assets in the share directory of the package.

Example usage:

```python
from ament_index_python.packages import get_package_share_directory

package_path = get_package_share_directory('h12_ros2_model')
print(f'Asset file: {package_path}/assets/{asset_file}')
```
'''
for path in glob('assets/**/*', recursive=True):
    if os.path.isfile(path):  # Skip directories
        install_path = os.path.join('share', package_name, os.path.dirname(path))
        data_files.append((install_path, [path]))

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tonyzyt2000',
    maintainer_email='zhangyt2000@gmail.com',
    description='ROS2 package of h12 robot description',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
