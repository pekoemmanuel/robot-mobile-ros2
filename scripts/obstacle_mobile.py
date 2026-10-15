import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.signals import SignalHandlerOptions

VITESSE = 0.3        # m/s
DUREE_TRAJET = 8.0   # secondes (temps simulé) dans chaque sens : 2,4 m


class ObstacleMobile(Node):
    def __init__(self):
        super().__init__('obstacle_mobile')
        self.pub = self.create_publisher(Twist, '/obstacle/cmd_vel', 10)
        self.debut = None
        self.create_timer(0.1, self.publier)

    def publier(self):
        maintenant = self.get_clock().now()
        if self.debut is None:
            self.debut = maintenant
        t = (maintenant - self.debut).nanoseconds / 1e9
        sens = -1.0 if int(t // DUREE_TRAJET) % 2 == 0 else 1.0
        msg = Twist()
        msg.linear.y = sens * VITESSE
        self.pub.publish(msg)


def main():
    rclpy.init(signal_handler_options=SignalHandlerOptions.NO)
    noeud = ObstacleMobile()
    try:
        rclpy.spin(noeud)
    except KeyboardInterrupt:
        pass
    noeud.pub.publish(Twist())  # arrête l'obstacle
    noeud.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
