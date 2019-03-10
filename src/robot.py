import numpy as np
from math import hypot as hyp

from numpy.linalg import LinAlgError


class Robot:
    def __init__(self, diameter, initial_theta, initial_position):
        # Robot specifications
        self.diameter = diameter
        self.radius = int(diameter / 2)
        self.position = initial_position

        # Rotation is in rads
        self.theta = initial_theta

        # Velocity of wheel in pixes/time
        self.MAX_SPEED = 10
        self.MIN_SPEED = -10
        self.left_wheel_velocity = 0
        self.right_wheel_velocity = 0

        # Sensors
        self.sensors_values = []
        self.sensors_rects = []
        self.sensors_parameters = np.zeros((12, 2))
        self.init_sensors()

        # walls for sensor values
        self.walls = []
        self.walls_parameters = np.zeros((4, 2))

        # Collision Data (for evolution algorithm)
        self.collisions = 0

        self.robot_rect = None

    def update_sensor_values(self):
        count = 0
        for angle in range(0, 360, 30):
            # sensor origin coords
            self.sensors_coords[count, 0] = self.position[0] + self.radius * np.cos(self.theta + np.radians(angle))
            self.sensors_coords[count, 1] = self.position[1] + self.radius * np.sin(self.theta + np.radians(angle))

            # sensor tips coords
            self.sensors_coords[count, 2] = self.position[0] + self.sens_radius * np.cos(self.theta + np.radians(angle))
            self.sensors_coords[count, 3] = self.position[1] + self.sens_radius * np.sin(self.theta + np.radians(angle))

            self.sensors_values[count] = hyp(self.sensors_coords[count, 2] - self.sensors_coords[count, 0],
                                             self.sensors_coords[count, 3] - self.sensors_coords[count, 1])

            # sensors functions parameters
            # slope a
            self.sensors_parameters[count, 0] = (self.sensors_coords[count, 3] - self.sensors_coords[count, 1]) / \
                                                (self.sensors_coords[count, 2] - self.sensors_coords[count, 0])
            # intercept b
            self.sensors_parameters[count, 1] = self.sensors_coords[count, 1] - (
                    self.sensors_parameters[count, 0] * self.sensors_coords[count, 0])

            count = count + 1

    def move(self):
        # Store old position before applying kinematics
        old_position = [self.position[0], self.position[1]]

        if self.left_wheel_velocity != self.right_wheel_velocity:
            # if self.left_wheel_velocity != self.right_wheel_velocity:
            # Calculate ω - angular velocity and change rotation of the robot
            angular_velocity = (self.left_wheel_velocity - self.right_wheel_velocity) / self.diameter

            # Keep theta from exploding
            self.theta %= 2 * np.pi

            R = (self.diameter / 2) * (self.left_wheel_velocity + self.right_wheel_velocity) / (
                    self.left_wheel_velocity - self.right_wheel_velocity)

            ICCx = self.position[0] - R * np.sin(self.theta)
            ICCy = self.position[1] + R * np.cos(self.theta)

            matrix_a = np.matrix([[np.cos(angular_velocity), -np.sin(angular_velocity), 0],
                                  [np.sin(angular_velocity), np.cos(angular_velocity), 0], [0, 0, 1]])
            vector_a = np.array([self.position[0] - ICCx, self.position[1] - ICCy, self.theta])
            vector_b = np.array([ICCx, ICCy, angular_velocity])
            new_pos_rot = matrix_a.dot(vector_a) + vector_b

            self.position = [new_pos_rot.item((0, 0)), new_pos_rot.item((0, 1))]
            self.theta = new_pos_rot.item((0, 2))
        elif self.right_wheel_velocity != 0:
            self.position[0] = self.position[0] + (self.right_wheel_velocity * np.cos(self.theta))
            self.position[1] = self.position[1] + (self.right_wheel_velocity * np.sin(self.theta))

        # Move the pygame rectangle object so that the check collision can evaluate with the new position
        self.robot_rect.move_ip(self.position[0] - old_position[0], self.position[1] - old_position[1])

        # Check if the new move caused a collision
        if self.check_collision():
            # Undo the move
            self.position = old_position
            # Move according to collision handling algorithm
            self.move_with_wall()
            # Increment collisions counter
            self.collisions += 1

        # update sensors
        self.update_sensor_values()

    def move_with_wall(self):
        cap_hor = 1
        cap_ver = 1
        velocity_hor = 0
        velocity_ver = 0

        for wall in self.walls:
            if self.robot_rect.colliderect(wall):
                velocity_hor = np.cos(self.theta) * (self.right_wheel_velocity + self.left_wheel_velocity) / 2
                velocity_ver = np.sin(self.theta) * (self.right_wheel_velocity + self.left_wheel_velocity) / 2

                if wall.width > 5:
                    # self.velocity_ver = 0
                    cap_ver = 0
                if wall.height > 5:
                    # self.velocity_hor = 0
                    cap_hor = 0

                velocity_hor = velocity_hor * cap_hor
                velocity_ver = velocity_ver * cap_ver

        self.position[0] = self.position[0] + velocity_hor
        self.position[1] = self.position[1] + velocity_ver

    def increment_left_wheel(self):
        if self.left_wheel_velocity + 1 <= self.MAX_SPEED:
            self.left_wheel_velocity += 1

    def decrement_left_wheel(self):
        if self.left_wheel_velocity - 1 >= self.MIN_SPEED:
            self.left_wheel_velocity -= 1

    def increment_right_wheel(self):
        if self.right_wheel_velocity + 1 <= self.MAX_SPEED:
            self.right_wheel_velocity += 1

    def decrement_right_wheel(self):
        if self.right_wheel_velocity - 1 >= self.MIN_SPEED:
            self.right_wheel_velocity -= 1

    def increment_both_wheels(self):
        self.increment_left_wheel()
        self.increment_right_wheel()

    def decrement_both_wheels(self):
        self.decrement_left_wheel()
        self.decrement_right_wheel()

    def stop_motors(self):
        self.right_wheel_velocity = 0
        self.left_wheel_velocity = 0

    def init_sensors(self):
        # 12 sensors perimetrically, 30o degrees between them
        # sensor 0 is the one in front of the robot.
        # Values go from 0 to 200, 200 being out of reach
        self.sensors_values = [0 for i in range(12)]
        self.sensors_coords = np.zeros((12, 4))
        # self.sens_radius = 3 * self.radius
        self.sens_radius = 100 + self.radius
        self.update_sensor_values()

    def setObst(self, walls, walls_params):
        self.walls = walls
        self.walls_parameters = walls_params

    def check_sensors(self):
        for sensor in range(len(self.sensors_rects)):
            for wall in range(len(self.walls)):
                if self.sensors_rects[sensor].colliderect(self.walls[wall]):
                    wall_params = self.walls_parameters[wall]
                    sensor_params = self.sensors_parameters[sensor]
                    a = np.array([[wall_params[0], 1], [sensor_params[0], 1]])
                    b = np.array([wall_params[1], sensor_params[1]])

                    if wall_params[0] != float('inf'):
                        # print("sensor coord: ", self.sensors_coords[sensor])
                        # print("sensor params: ", self.sensors_parameters[sensor])
                        # print("wall params: ", self.walls_parameters[wall])
                        try:
                            intersection_coord = np.linalg.solve(a, b)
                            intersection_coord[0] = -intersection_coord[0]
                        except LinAlgError:
                            # print("no collision between wall ", wall, " and sensor ", sensor)
                            return

                    else:
                        intersection_coord = [self.walls[wall][0],
                                              sensor_params[0] * self.walls[wall][0] + sensor_params[1]]

                    self.sensors_values[sensor] = np.sqrt(
                        (intersection_coord[0] - self.sensors_coords[sensor, 0]) ** 2 + (
                                intersection_coord[1] - self.sensors_coords[sensor, 1]) ** 2)

                    if self.sensors_values[sensor] < 100:
                        self.sensors_coords[sensor, 2] = intersection_coord[0]
                        self.sensors_coords[sensor, 3] = intersection_coord[1]

    def check_collision(self):
        count_collisions = 0
        for wall in self.walls:
            if self.robot_rect.colliderect(wall):
                count_collisions += 1
        if count_collisions > 0:
            return True
        return False
