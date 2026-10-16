# 🤖 Projet Robot Mobile - ROS 2 Jazzy & Nav2

Ce dépôt contient l'architecture complète pour la simulation, la cartographie et la navigation autonome d'un robot mobile différentiel sous **Ubuntu 24.04** avec **ROS 2 Jazzy** et **Gazebo Sim**.

## 📊 Aperçu de la Patrouille Autonome (HD)

Voici la démonstration de la patrouille autonome sur 5 points de contrôle avec évitement dynamique d'un obstacle mobile dans l'arène :

![Patrouille Autonome Haute Définition](docs/patrouille_hd.gif)

## 🛠️ Architecture du Projet & Dépendances
Le projet s'appuie sur les outils et packages officiels de l'écosystème ROS 2 :
* **ROS 2 Jazzy Desktop** (Outils de base et RViz2)
* **Gazebo Sim / ros_gz** (Simulation physique et capteurs)
* **Xacro** (Modélisation du robot en URDF)
* **Slam Toolbox** (Cartographie 2D synchrone/asynchrone)
* **Nav2 Bringup** (Pile de navigation autonome)
* **Colcon** (Gestionnaire de compilation du workspace)

## 🚀 Protocole d'Exécution (Séquence de Test)

Pour valider le comportement du robot, exécutez successivement les commandes ou utilisez les raccourcis configurés sur le Bureau :

1. **Lancement de la simulation physique (Arène Gazebo) :**
   ```bash
   ros2 launch robot_gazebo sim.launch.py
   ```

2. **Démarrage de la pile autonome Nav2 et chargement de la carte :**
   ```bash
   ros2 launch nav2_bringup bringup_launch.py map:=\(HOME/robot_ws/src/robot_gazebo/maps/arene.yaml params_file:=\)HOME/robot_ws/src/robot_gazebo/config/nav2_params.yaml use_sim_time:=true
   ```

3. **Activation de l'obstacle mobile dynamique :**
   ```bash
   python3 ~/robot_ws/scripts/obstacle_mobile.py --ros-args -p use_sim_time:=true
   ```

4. **Calibrage automatique de la pose initiale du robot (0,0) :**
   ```bash
   ros2 topic pub --once /initialpose geometry_msgs/msg/PoseWithCovarianceStamped "{header: {frame_id: map}, pose: {pose: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {w: 1.0}}}}"
   ```

5. **Exécution de la série de 5 patrouilles consécutives :**
   ```bash
   python3 ~/robot_ws/scripts/patrouille.py --ros-args -p use_sim_time:=true
   ```
