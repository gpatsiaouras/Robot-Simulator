import numpy as np


class Robot:
    def __init__(self, diameter, initial_theta, initial_position, beacons):
        # Robot specifications
        self.diameter = diameter
        self.radius = int(diameter / 2)
        self.position = initial_position
        self.sensor_max_radius = 170

        # Rotation is in rads
        self.theta = initial_theta

        # Velocities
        self.MAX_SPEED_LINEAR = 5
        self.MIN_SPEED_LINEAR = -5
        self.MAX_SPEED_ANGULAR = 1
        self.MIN_SPEED_ANGULAR = -1
        self.linear_velocity = 0
        self.angular_velocity = 0

        # Environment beacons
        self.beacons = beacons
        self.intercepting_beacons_positions = []

        # Path followed
        self.path = []

    def move(self):
        self.check_beacons()
        if self.linear_velocity != 0 and self.angular_velocity == 0:
            self.position[0] = self.position[0] + np.cos(self.theta) * self.linear_velocity
            self.position[1] = self.position[1] + np.sin(self.theta) * self.linear_velocity
            self.path.append([self.position[0], self.position[1]])
        else:
            # Keep theta from exploding
            self.theta %= 2 * np.pi
            self.theta = self.theta + self.angular_velocity

    def check_beacons(self):
        self.intercepting_beacons_positions = []
        for beacon in self.beacons:
            if self.beacon_is_in_range(beacon):
                self.intercepting_beacons_positions.append([beacon[0], beacon[1]])

    def increment_linear_velocity(self):
        self.angular_velocity = 0
        if self.linear_velocity + 1 <= self.MAX_SPEED_LINEAR:
            self.linear_velocity += 1

    def decrement_linear_velocity(self):
        if self.linear_velocity - 1 >= self.MIN_SPEED_LINEAR:
            self.linear_velocity -= 1

    def increment_angular_velocity(self):
        if self.angular_velocity + 0.05 <= self.MAX_SPEED_ANGULAR:
            self.angular_velocity += 0.05

    def decrement_angular_velocity(self):
        if self.angular_velocity - 0.05 >= self.MIN_SPEED_ANGULAR:
            self.angular_velocity -= 0.05

    def stop_motors(self):
        self.angular_velocity = 0
        self.linear_velocity = 0

    def reset(self, theta, position):
        self.theta = theta
        self.position = position
        self.path = []
        self.linear_velocity = 0
        self.angular_velocity = 0

    def beacon_is_in_range(self, beacon):
        if np.sqrt((self.position[0] - beacon[0]) ** 2 + (self.position[1] - beacon[1]) ** 2) <= self.sensor_max_radius:
            return True
        return False
