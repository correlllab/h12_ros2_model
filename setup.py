import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'h12_ros2_model'

# Top-level repo's canonical asset directory. This package is no longer
# standalone-buildable: it must live at <repo>/core_ws/src/h12_ros2_model so
# that ../../../assets/ resolves. See README.md.
HERE = os.path.dirname(os.path.abspath(__file__))
TOP_ASSETS_REL = os.path.join('..', '..', '..', 'assets')
TOP_ASSETS_ABS = os.path.normpath(os.path.join(HERE, TOP_ASSETS_REL))


def _files(*patterns):
    """Glob `patterns` (relative to HERE) and return paths still relative to HERE.

    colcon's ament_python builder asserts that data_files source paths are
    relative strings, so we glob via absolute paths but emit relative ones.
    """
    out = []
    for pat in patterns:
        abs_pat = pat if os.path.isabs(pat) else os.path.join(HERE, pat)
        for abs_path in glob(abs_pat):
            if os.path.isfile(abs_path):
                out.append(os.path.relpath(abs_path, HERE))
    return out


h1_2_meshes = _files(os.path.join(TOP_ASSETS_REL, 'meshes', 'h1_2', '*.STL'))
magpie_meshes = _files(os.path.join(TOP_ASSETS_REL, 'meshes', 'magpie', '*.stl'))

if not os.path.isdir(TOP_ASSETS_ABS):
    raise RuntimeError(
        f"h12_ros2_model expected top-level assets at {TOP_ASSETS_ABS} but "
        "the directory does not exist. This package must be built inside the "
        "Humanoid_Simulation workspace; standalone clones are not supported."
    )
if not h1_2_meshes:
    raise RuntimeError(f"No H1-2 meshes found under {TOP_ASSETS_ABS}/meshes/h1_2/")

# Stage URDFs/SRDFs in a build dir so we can rewrite the relative-path Pinocchio
# variants. Top-level URDFs use '../meshes/h1_2/...' (relative from ros_assets/);
# in our install they live at share/<pkg>/assets/h1_2/<name>.urdf alongside
# meshes at share/<pkg>/assets/h1_2/meshes/, so paths are rewritten to
# 'meshes/...' to resolve correctly under the share/ layout. The *_ros.urdf
# variants use package:// and are copied through unchanged.
STAGE_DIR = os.path.join(HERE, '_install_staging', 'h1_2')
os.makedirs(STAGE_DIR, exist_ok=True)
# Clear stale entries so renamed/removed top-level files don't linger.
for stale in os.listdir(STAGE_DIR):
    os.remove(os.path.join(STAGE_DIR, stale))

_top_descriptors = _files(
    os.path.join(TOP_ASSETS_REL, 'ros_assets', 'h1_2*.urdf'),
    os.path.join(TOP_ASSETS_REL, 'ros_assets', 'h1_2*.srdf'),
)
if not _top_descriptors:
    raise RuntimeError(f"No H1-2 URDF/SRDF found under {TOP_ASSETS_ABS}/ros_assets/")

h1_2_descriptors = []
for src_rel in _top_descriptors:
    src_abs = os.path.join(HERE, src_rel)
    name = os.path.basename(src_abs)
    dst_abs = os.path.join(STAGE_DIR, name)
    with open(src_abs, 'r') as f:
        content = f.read()
    if name.endswith('.urdf') and '_ros' not in name:
        # Pinocchio-flavor URDF: rewrite top-level-relative mesh paths so they
        # resolve against the share-layout location (meshes alongside the URDF).
        content = content.replace('../meshes/h1_2/', 'meshes/')
        content = content.replace('../meshes/magpie/', 'meshes/magpie/')
    with open(dst_abs, 'w') as f:
        f.write(content)
    h1_2_descriptors.append(os.path.relpath(dst_abs, HERE))

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
    ('share/' + package_name + '/assets/h1_2/meshes/magpie', magpie_meshes),
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
