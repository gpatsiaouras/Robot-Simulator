import numpy as np


class Robot:
    def __init__(self, diameter, initial_rotation, initial_position):
        # Robot specifications
        self.diameter = diameter
        self.radius = diameter / 2
        self.rotation = initial_rotation
        self.position = initial_position

        # Velocity of wheel
        self.MAX_SPEED = 10
        self.MIN_SPEED = -10
        self.left_wheel_velocity = 0
        self.right_wheel_velocity = 0

        # Sensors
        # 12 sensors perimetrically, 30o degrees between them
        # sensor 0 is the one in front of the robot.
        # Values go from 0 to 200, 200 being out of reach
        self.distance_sensors = [200 for i in range(12)]

    def update_sensor_values(self):
        pass

    def move(self):
        # Calculate ω - angular velocity and change rotation of the robot
        angular_velocity = (self.right_wheel_velocity - self.left_wheel_velocity) / self.diameter
        self.rotation = self.rotation + angular_velocity

        if self.left_wheel_velocity != self.right_wheel_velocity:
            R = (self.diameter / 2) * (self.left_wheel_velocity + self.right_wheel_velocity) / (
                        self.right_wheel_velocity - self.left_wheel_velocity)

            ICC = [self.position[0] - R * np.sin(self.rotation), self.position[1] + R * np.cos(self.rotation)]

            matrixA = np.matrix([[np.cos(angular_velocity), -np.sin(angular_velocity), 0],[np.sin(angular_velocity), np.cos(angular_velocity), 0],[0, 0, 1]])
            vectorA = np.array([self.position[0] - ICC[0], self.position[1] - ICC[1], self.rotation])
            vectorB = np.array([ICC[0], ICC[1], self.rotation])
            print(matrixA)
            print(vectorA)
            print(vectorB)
            new_pos_rot = matrixA.dot(vectorA) + vectorB
            self.position = [new_pos_rot.item((0, 0)), new_pos_rot.item((0, 1))]
            self.rotation = new_pos_rot.item((0, 2))
        elif self.right_wheel_velocity != 0:
            self.position[0] = self.position[0] + np.cos(self.right_wheel_velocity)
            self.position[1] = self.position[1] + np.sin(self.right_wheel_velocity)

    def increment_left_wheel(self):
        if self.left_wheel_velocity + 1 <= self.MAX_SPEED and self.left_wheel_velocity >= self.MIN_SPEED:
            self.left_wheel_velocity += 1

    def decrement_left_wheel(self):
        if self.left_wheel_velocity + 1 <= self.MAX_SPEED and self.left_wheel_velocity >= self.MIN_SPEED:
            self.left_wheel_velocity -= 1

    def increment_right_wheel(self):
        if self.right_wheel_velocity + 1 <= self.MAX_SPEED and self.right_wheel_velocity >= self.MIN_SPEED:
            self.right_wheel_velocity += 1

    def decrement_right_wheel(self):
        if self.right_wheel_velocity + 1 <= self.MAX_SPEED and self.right_wheel_velocity >= self.MIN_SPEED:
            self.right_wheel_velocity -= 1

    def increment_both_wheels(self):
        self.increment_left_wheel()
        self.increment_right_wheel()

    def decrement_both_wheels(self):
        self.decrement_left_wheel()
        self.decrement_right_wheel()
