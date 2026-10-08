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
NB_ESSAIS = 3  # tentatives par point avant d'abandonner


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
    # Le robot est déjà localisé : on attend seulement la navigation
    nav.waitUntilNav2Active(localizer='robot_localization')
    debut = nav.get_clock().now()

    try:
        for numero, (x, y, yaw) in enumerate(POINTS, start=1):
            atteint = False
            for essai in range(1, NB_ESSAIS + 1):
                nav.info(f'Point {numero}/{len(POINTS)} : x={x} y={y} '
                         f'(essai {essai}/{NB_ESSAIS})')
                nav.goToPose(fabriquer_pose(nav, x, y, yaw))
                while not nav.isTaskComplete():
                    pass
                resultat = nav.getResult()
                if resultat == TaskResult.SUCCEEDED:
                    nav.info('  atteint')
                    atteint = True
                    break
                nav.error(f'  échec : {resultat}, nettoyage des cartes de coûts')
                nav.clearAllCostmaps()
            if not atteint:
                nav.error('  point abandonné, fin de la patrouille')
                break
    except KeyboardInterrupt:
        nav.cancelTask()

    duree = (nav.get_clock().now() - debut).nanoseconds / 1e9
    nav.info(f'Durée totale (temps simulé) : {duree:.1f} s')
    nav.info('Patrouille terminée')
    rclpy.shutdown()


if __name__ == '__main__':
    main()
