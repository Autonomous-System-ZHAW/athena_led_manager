from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    led_manager_node = Node(
        package="athena_led_manager",
        executable="led_manager",
        name="led_manager",
        output="screen",
    )

    return LaunchDescription([led_manager_node])
