import os
from glob import glob
from setuptools import setup

package_name = 'my_package'
data_files = [(os.path.join('share', package_name, 'protos'), glob(os.path.join('protos', '*.proto'))),
        (os.path.join('share', package_name, 'protos/meshes'), glob(os.path.join('protos/meshes', '*.stl'))),
        ]
data_files.append(('share/ament_index/resource_index/packages', ['resource/' + package_name]))
data_files.append(('share/' + package_name + '/launch', ['launch/pib_launch.py']))
data_files.append(('share/' + package_name + '/worlds', ['worlds/PibSim.wbt']))
data_files.append(('share/' + package_name + '/resource', ['resource/pib.urdf']))
data_files.append(('share/' + package_name, ['package.xml']))

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='snfeld',
    maintainer_email='user.name@mail.com',
    description='TODO: Package description',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pib_driver = my_package.pib_driver:main',
        ],
    },
)
