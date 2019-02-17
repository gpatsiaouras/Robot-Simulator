import numpy as np


class Robot:
    def __init__(self, diameter, initial_theta, initial_position):
        # Robot specifications
        self.diameter = diameter
        self.radius = diameter / 2
        self.position = initial_position

        # Rotation is in rads
        self.theta = initial_theta

        # Velocity of wheel in pixes/time
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
        if self.left_wheel_velocity != self.right_wheel_velocity:
            # Calculate ω - angular velocity and change rotation of the robot
            angular_velocity = (self.left_wheel_velocity - self.right_wheel_velocity) / self.diameter

            # Keep theta from exploding
            self.theta %= 2*np.pi

            R = (self.diameter / 2) * (self.left_wheel_velocity + self.right_wheel_velocity) / (
                    self.left_wheel_velocity - self.right_wheel_velocity)

            ICCx = self.position[0] - R * np.sin(self.theta)
            ICCy = self.position[1] + R * np.cos(self.theta)

            matrix_a = np.matrix([[np.cos(angular_velocity), -np.sin(angular_velocity), 0], [np.sin(angular_velocity), np.cos(angular_velocity), 0], [0, 0, 1]])
            vector_a = np.array([self.position[0] - ICCx, self.position[1] - ICCy, self.theta])
            vector_b = np.array([ICCx, ICCy, angular_velocity])
            new_pos_rot = matrix_a.dot(vector_a) + vector_b

            self.position = [new_pos_rot.item((0, 0)), new_pos_rot.item((0, 1))]
            self.theta = new_pos_rot.item((0, 2))
        elif self.right_wheel_velocity != 0:
            self.position[0] = self.position[0] + (self.right_wheel_velocity * np.cos(self.theta))
            self.position[1] = self.position[1] + (self.right_wheel_velocity * np.sin(self.theta))

    def increment_left_wheel(self):
        if self.left_wheel_velocity + 1 <= self.MAX_SPEED:
            self.left_wheel_velocity += 1

    def decrement_left_wheel(self):
        if self.left_wheel_velocity - 1>= self.MIN_SPEED:
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
