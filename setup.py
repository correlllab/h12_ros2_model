import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'h12_ros2_model'

# Top-level repo's canonical asset directory. This package is no longer
# standalone-buildable: it must live at <repo>/core_ws/src/h12_ros2_model so
# that ../../../assets/ resolves. See README.md.
HERE = os.path.dirname(os.path.abspath(__file__))
TOP_ASSETS = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'assets'))


def _files(*patterns):
    out = []
    for p in patterns:
        out.extend(f for f in glob(p) if os.path.isfile(f))
    return out


h1_2_meshes = _files(os.path.join(TOP_ASSETS, 'meshes', 'h1_2', '*.STL'))
h1_2_descriptors = _files(
    os.path.join(TOP_ASSETS, 'ros_assets', 'h1_2*.urdf'),
    os.path.join(TOP_ASSETS, 'ros_assets', 'h1_2*.srdf'),
)

if not os.path.isdir(TOP_ASSETS):
    raise RuntimeError(
        f"h12_ros2_model expected top-level assets at {TOP_ASSETS} but the "
        "directory does not exist. This package must be built inside the "
        "Humanoid_Simulation workspace; standalone clones are not supported."
    )
if not h1_2_meshes:
    raise RuntimeError(f"No H1-2 meshes found under {TOP_ASSETS}/meshes/h1_2/")
if not h1_2_descriptors:
    raise RuntimeError(f"No H1-2 URDF/SRDF found under {TOP_ASSETS}/ros_assets/")

h1_2_local_extras = _files(
    'assets/h1_2/*.xml',
    'assets/h1_2/*.png',
    'assets/h1_2/README.md',
)

data_files = [
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    ('share/' + package_name + '/launch', glob('launch/*.py')),
    ('share/' + package_name + '/rviz', glob('rviz/*.rviz')),
    # H1-2 assets: meshes + URDFs/SRDFs come from the top-level canonical
    # location; *.xml / *.png / README.md remain submodule-only.
    ('share/' + package_name + '/assets/h1_2/meshes', h1_2_meshes),
    ('share/' + package_name + '/assets/h1_2', h1_2_descriptors + h1_2_local_extras),
    ('share/' + package_name + '/assets', _files(
        'assets/h1-2_tf.jpg',
        'assets/LICENSE',
    )),
]

setup(
    name=package_name,
    version='0.0.2',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    data_files=data_files,
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
