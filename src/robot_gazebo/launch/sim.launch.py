import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    desc_pkg = get_package_share_directory('robot_description')
    gz_pkg = get_package_share_directory('robot_gazebo')
    ros_gz_sim = get_package_share_directory('ros_gz_sim')

    xacro_file = os.path.join(desc_pkg, 'urdf', 'mon_robot.urdf.xacro')
    world_file = os.path.join(gz_pkg, 'worlds', 'monde_simple.sdf')
    bridge_file = os.path.join(gz_pkg, 'config', 'bridge.yaml')

    robot_description = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': '-r ' + world_file}.items(),
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_file, 'use_sim_time': True}],
        output='screen',
    )

    # Apparition retardée : laisse à Gazebo le temps de démarrer sur une machine lente
    spawn = TimerAction(period=10.0, actions=[
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-world', 'monde_simple', '-topic', 'robot_description',
                       '-name', 'mon_robot', '-z', '0.05'],
        ),
    ])

    return LaunchDescription([gazebo, rsp, bridge, spawn])
