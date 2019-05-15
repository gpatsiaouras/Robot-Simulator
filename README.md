# Autonomous Robotic Systems - Robot Simulator

## Description
Robot simulator featuring a differential robot developed in python from scratch using pygame library.

The robot layout was a two wheel robot with 12 proximity sensors placed in a 360 layout. The robot thus have a panoramic
view of it's environment while moving. In order to autonomously move the robot a Artificial Neural Network was deployed.
The input of the network was the values of these 12 proximity sensors and the output was the velocity
of the left and right wheel. 

During the development we were required to develop two major algorithms:
1. Evolutionary algorithm that was envolving the weights of the ANN used for the movement of the robot so that 
the movement is collision-free. The EA uses an evaluation function that penalties the algorithm when the robot collides
with walls or is going to slow, thus encouraging movement. Also the path of the robot is monitoring in order to make the 
robot explore as much of the room that it has as possible.
2. Localization algorithm implemented to place the robot on the map without the robot knowing where it is. The map contained
beacons that the robot could see with a laser sensor and based on that information calculate the position where it is. 
The data used was the odometry information from the wheels of the robot and the laser sensor.

## Run
To run cd inside the src directory and execute the first command for evolution algorithm and second for localization

    python3.6 evolution/main.py
    python3.6 localization/main.py
