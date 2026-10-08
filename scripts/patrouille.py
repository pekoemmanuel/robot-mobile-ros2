import math

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

# Points de passage : (x, y, orientation en radians), dans le repère de la carte
POINTS = [
    (2.5, -2.5, 0.0),
    (2.5, 2.5, 1.57),
    (0.0, 2.5, 3.14),
    (-2.5, -0.5, -1.57),
    (0.0, 0.0, 0.0),
]


def fabriquer_pose(nav, x, y, yaw):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = nav.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.orientation.z = math.sin(yaw / 2.0)
    pose.pose.orientation.w = math.cos(yaw / 2.0)
    return pose


def main():
    rclpy.init()
    nav = BasicNavigator()
    # Le robot est déjà localisé : on n'attend que la navigation
    nav.waitUntilNav2Active(localizer='robot_localization')

    try:
        for numero, (x, y, yaw) in enumerate(POINTS, start=1):
            nav.info(f'Point {numero}/{len(POINTS)} : x={x} y={y}')
            nav.goToPose(fabriquer_pose(nav, x, y, yaw))
            while not nav.isTaskComplete():
                retour = nav.getFeedback()
                if retour:
                    reste = retour.distance_remaining
                    nav.info(f'  distance restante : {reste:.2f} m')
            resultat = nav.getResult()
            if resultat == TaskResult.SUCCEEDED:
                nav.info('  atteint')
            else:
                nav.error(f'  échec ou annulation : {resultat}')
                break
    except KeyboardInterrupt:
        nav.cancelTask()

    nav.info('Patrouille terminée')
    rclpy.shutdown()


if __name__ == '__main__':
    main()
