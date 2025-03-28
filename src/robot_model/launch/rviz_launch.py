import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    package_name = 'robot_model'
    urdf_name = "yuelu.urdf"

    pkg_share = FindPackageShare(package=package_name).find(package_name) 
    urdf_model_path = os.path.join(pkg_share, f'urdf/{urdf_name}')
    default_rviz_config_path = os.path.join(pkg_share ,'rviz/urdf.rviz')

    para_value = ParameterValue(Command(['xacro ', urdf_model_path]), value_type=str)
    rviz_arg = DeclareLaunchArgument(name='rvizconfig', default_value=str(default_rviz_config_path),
                                     description='Absolute path to rviz config file')

    robot_state_pub = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": para_value}]
    )

    joint_state_pub = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    rviz2 = Node(
        package="rviz2", 
        executable="rviz2",
        arguments=['-d', LaunchConfiguration('rvizconfig')]
    )

    return LaunchDescription([rviz_arg, robot_state_pub, joint_state_pub, rviz2])