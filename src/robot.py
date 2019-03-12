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
        self.sensors_parameters = np.zeros((12, 2))
        self.init_sensors()

        # obstacles for sensor values
        self.obstacles_coords = []
        self.obstacles_parameters = np.zeros((4, 2))

        # Collision Data (for evolution algorithm)
        self.collisions = 0

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

        for obstacle_id in range(len(self.obstacles_parameters)):
            # print("Obstacle {0}: {1}".format(obstacle_id, self.obstacles_parameters[obstacle_id][0]))
            # Vertical Obstacle
            if np.isinf(self.obstacles_parameters[obstacle_id][0]):
                distance = np.abs(self.position[0] - self.obstacles_coords[obstacle_id][0])
                is_inside_the_limits_of_the_line = [
                    self.obstacles_coords[obstacle_id][3] < self.position[1] < self.obstacles_coords[obstacle_id][1]]
            # Horizontal Obstacle
            elif self.obstacles_parameters[obstacle_id][0] == 0:
                distance = np.abs(self.position[1] - self.obstacles_coords[obstacle_id][1])
                is_inside_the_limits_of_the_line = [
                    self.obstacles_coords[obstacle_id][2] > self.position[0] > self.obstacles_coords[obstacle_id][0]]
            else:
                distance = np.abs(-self.obstacles_parameters[obstacle_id][0] * self.position[0] + self.position[1] -
                                  self.obstacles_parameters[obstacle_id][1]) / \
                           np.sqrt((-self.obstacles_parameters[obstacle_id][0]) ** 2 + 1)
                is_inside_the_limits_of_the_line = False

            if is_inside_the_limits_of_the_line and distance <= self.radius + 10:
                velocity_hor = np.cos(self.theta) * (self.right_wheel_velocity + self.left_wheel_velocity) / 2
                velocity_ver = np.sin(self.theta) * (self.right_wheel_velocity + self.left_wheel_velocity) / 2

                if self.obstacles_parameters[obstacle_id][0] == 0:
                    # self.velocity_ver = 0
                    cap_ver = 0
                if np.isinf(self.obstacles_parameters[obstacle_id][0]):
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

    def set_obstacles(self, obstacles_coords, obstacles_params):
        self.obstacles_coords = obstacles_coords
        self.obstacles_parameters = obstacles_params

    def check_sensors(self):
        for sensor_id in range(len(self.sensors_coords)):
            for obstacle_id in range(len(self.obstacles_coords)):
                intersection_point = self.getIntersectingPoint(self.sensors_coords[sensor_id],
                                                               self.obstacles_coords[obstacle_id])

                if intersection_point:
                    self.sensors_values[sensor_id] = np.sqrt(
                        (intersection_point[0] - self.sensors_coords[sensor_id, 0]) ** 2 + (
                                intersection_point[1] - self.sensors_coords[sensor_id, 1]) ** 2)

                    if self.sensors_values[sensor_id] < 100:
                        self.sensors_coords[sensor_id, 2] = intersection_point[0]
                        self.sensors_coords[sensor_id, 3] = intersection_point[1]

    def check_collision(self):
        for obstacle_id in range(len(self.obstacles_parameters)):
            if np.isinf(self.obstacles_parameters[obstacle_id][0]):
                distance = np.abs(self.position[0] - self.obstacles_coords[obstacle_id][0])
                if self.position[1] < min(self.obstacles_coords[obstacle_id][1], self.obstacles_coords[obstacle_id][3]):
                    is_not_in_range = False
                elif self.position[1] > max(self.obstacles_coords[obstacle_id][1], self.obstacles_coords[obstacle_id][3]):
                    is_not_in_range = False
                else:
                    is_not_in_range = True
            elif self.obstacles_parameters[obstacle_id][0] == 0:
                distance = np.abs(self.position[1] - self.obstacles_coords[obstacle_id][1])
                if self.position[0] < min(self.obstacles_coords[obstacle_id][0], self.obstacles_coords[obstacle_id][2]):
                    is_not_in_range = False
                elif self.position[0] > max(self.obstacles_coords[obstacle_id][0], self.obstacles_coords[obstacle_id][2]):
                    is_not_in_range = False
                else:
                    is_not_in_range = True
            else:
                distance = np.abs(-self.obstacles_parameters[obstacle_id][0] * self.position[0] + self.position[1] -
                                  self.obstacles_parameters[obstacle_id][1]) / \
                           np.sqrt((-self.obstacles_parameters[obstacle_id][0]) ** 2 + 1)
                is_not_in_range = True

            if is_not_in_range and distance <= self.radius:
                return True
        return False

    def getIntersectingPoint(self, line1, line2):
        """ If the given lines are intersecting, return the position of this intersection, otherwise false """

        line1_p1 = [line1[0], line1[1]]
        line1_p2 = [line1[2], line1[3]]
        line2_p1 = [line2[0], line2[1]]
        line2_p2 = [line2[2], line2[3]]

        # Check if a line intersection is possible within range
        if ((line1_p1[0] > line2_p1[0] and line1_p1[0] > line2_p2[0] and line1_p2[0] > line2_p1[0] and line1_p2[0] >
             line2_p2[0]) or
                (line1_p1[0] < line2_p1[0] and line1_p1[0] < line2_p2[0] and line1_p2[0] < line2_p1[0] and line1_p2[0] <
                 line2_p2[0]) or
                (line1_p1[1] > line2_p1[1] and line1_p1[1] > line2_p2[1] and line1_p2[1] > line2_p1[1] and line1_p2[1] >
                 line2_p2[1]) or
                (line1_p1[1] < line2_p1[1] and line1_p1[1] < line2_p2[1] and line1_p2[1] < line2_p1[1] and line1_p2[1] <
                 line2_p2[1])):
            return False

        # Get axis differences
        diffX = (line1_p1[0] - line1_p2[0], line2_p1[0] - line2_p2[0])
        diffY = (line1_p1[1] - line1_p2[1], line2_p1[1] - line2_p2[1])

        # Get intersection
        d = np.linalg.det([diffX, diffY])
        if d == 0:
            return False
        det = (np.linalg.det([line1_p1, line1_p2]), np.linalg.det([line2_p1, line2_p2]))
        x = np.linalg.det([det, diffX]) / d
        y = np.linalg.det([det, diffY]) / d

        # Check if it is within range
        margin = 0.0001
        if (x < min(line1_p1[0], line1_p2[0]) - margin or
                x > max(line1_p1[0], line1_p2[0]) + margin or
                y < min(line1_p1[1], line1_p2[1]) - margin or
                y > max(line1_p1[1], line1_p2[1]) + margin or
                x < min(line2_p1[0], line2_p2[0]) - margin or
                x > max(line2_p1[0], line2_p2[0]) + margin or
                y < min(line2_p1[1], line2_p2[1]) - margin or
                y > max(line2_p1[1], line2_p2[1]) + margin):
            return False

        return x, y
