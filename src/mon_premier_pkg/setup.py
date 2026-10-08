from setuptools import find_packages, setup

package_name = 'mon_premier_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='peko',
    maintainer_email='284374573+pekoemmanuel@users.noreply.github.com',
    description='Premiers noeuds ROS 2',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher = mon_premier_pkg.publisher:main',
            'subscriber = mon_premier_pkg.subscriber:main',
        ],
    },
)
