import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MonPublisher(Node):
    def __init__(self):
        super().__init__('mon_publisher')
        self.pub = self.create_publisher(String, 'chatter_perso', 10)
        self.timer = self.create_timer(1.0, self.publier)
        self.n = 0

    def publier(self):
        msg = String()
        msg.data = f'Bonjour robot {self.n}'
        self.pub.publish(msg)
        self.get_logger().info(f'Publié : {msg.data}')
        self.n += 1


def main():
    rclpy.init()
    node = MonPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()
