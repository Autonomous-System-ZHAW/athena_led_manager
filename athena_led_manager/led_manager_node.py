import rclpy
from rclpy.node import Node
from athena_custom_msgs_pkg.msg import SystemMode, LedColor

from athena_common.utils import SYSTEM_MODE_COLOR_CODE


class LEDManagerNode(Node):
    def __init__(self):
        super().__init__("led_manager_node")
        self.current_mode = None
        self.blink_state = False

        self.create_subscription(SystemMode, "/system_mode", self.led_mode_callback, 10)
        self.led_code_publisher = self.create_publisher(LedColor, "/led/color", 10)

        self.blink_timer = self.create_timer(
            0.5,
            self.blink_callback,
        )

    def led_mode_callback(self, msg):
        self.current_mode = msg.mode
        self.get_logger().info(f"Received system mode: {self.current_mode}")

        if self.current_mode == SystemMode.EMERGENCY:
            return

        color = SYSTEM_MODE_COLOR_CODE.get(self.current_mode)

        if color is None:
            self.get_logger().warn(f"No LED color defined for mode {self.current_mode}")
            return

        self.publish_color(color)

    def blink_callback(self):
        if self.current_mode != SystemMode.EMERGENCY:
            return

        self.blink_state = not self.blink_state

        if self.blink_state:
            color = SYSTEM_MODE_COLOR_CODE[SystemMode.EMERGENCY]
        else:
            color = SYSTEM_MODE_COLOR_CODE[SystemMode.OFF]

        self.publish_color(color)

    def publish_color(self, color):
        msg = LedColor()

        msg.r = color[0]
        msg.g = color[1]
        msg.b = color[2]
        msg.w = color[3]

        self.led_code_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = LEDManagerNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
