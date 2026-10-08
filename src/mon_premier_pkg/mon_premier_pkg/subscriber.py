import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MonSubscriber(Node):
    def __init__(self):
        super().__init__('mon_subscriber')
        self.create_subscription(String, 'chatter_perso', self.recevoir, 10)

    def recevoir(self, msg):
        self.get_logger().info(f'Reçu : {msg.data}')


def main():
    rclpy.init()
    node = MonSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()
