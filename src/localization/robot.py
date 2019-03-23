import numpy as np

# Values between 100 and 1000 give reasonable trajectories
# higher values result in more aggression
AGGRESSION = 600


class Robot:
    def __init__(self, diameter, initial_theta, initial_position, beacons):
        # Robot specifications
        self.diameter = diameter
        self.radius = int(diameter / 2)
        self.noiseless_position = initial_position
        self.actual_position = initial_position
        self.sensor_max_radius = 170

        # Rotation is in rads
        self.noiseless_theta = initial_theta
        self.actual_theta = initial_theta

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
        self.noiseless_path = []
        self.actual_path = []

    def move(self):
        self.check_beacons()

        if self.linear_velocity != 0 or self.angular_velocity != 0:
            new_noiseless_position, new_noiseless_theta = self.get_noiseless_position()
            new_actual_position, new_actual_theta = self.get_actual_position()

            # update positions
            self.actual_position = new_actual_position
            self.noiseless_position = new_noiseless_position

            # update thetas
            self.actual_theta = new_actual_theta
            self.noiseless_theta = new_noiseless_theta

            # Save paths
            self.noiseless_path.append(new_noiseless_position)
            self.actual_path.append(new_actual_position)

            # Keep theta from exploding
            self.actual_theta %= 2 * np.pi
            self.noiseless_theta %= 2 * np.pi

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
        self.actual_theta = theta
        self.noiseless_theta = theta
        self.actual_position = position
        self.noiseless_position = position
        self.actual_path = []
        self.noiseless_path = []
        self.linear_velocity = 0
        self.angular_velocity = 0

    def beacon_is_in_range(self, beacon):
        if np.sqrt((self.actual_position[0] - beacon[0]) ** 2 + (
                self.actual_position[1] - beacon[1]) ** 2) <= self.sensor_max_radius:
            return True
        return False

    def get_random_noise(self, aggression):
        return np.random.randint(-2, 2) / aggression

    def get_noiseless_position(self):
        new_position = [
            self.noiseless_position[0] + np.cos(self.noiseless_theta) * self.linear_velocity,
            self.noiseless_position[1] + np.sin(self.noiseless_theta) * self.linear_velocity
        ]
        new_theta = self.noiseless_theta + self.angular_velocity

        return new_position, new_theta

    def get_actual_position(self):
        # Add noise to the trajectory of the robot
        actual_linear_velocity = self.linear_velocity + self.get_random_noise(AGGRESSION)
        actual_angular_velocity = self.angular_velocity + self.get_random_noise(AGGRESSION)

        new_position = [
            self.actual_position[0] + np.cos(self.actual_theta) * actual_linear_velocity,
            self.actual_position[1] + np.sin(self.actual_theta) * actual_linear_velocity
        ]
        new_theta = self.actual_theta + actual_angular_velocity

        return new_position, new_theta
