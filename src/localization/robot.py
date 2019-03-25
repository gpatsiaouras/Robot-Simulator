import numpy as np


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

        # Values between 100 and 1000 give reasonable trajectories
        # higher values result in less aggression
        self.aggression = 200
        self.MIN_AGGRESSION = 1
        self.MAX_AGGRESSION = 1000

        # Velocities
        self.MAX_SPEED_LINEAR = 5
        self.MIN_SPEED_LINEAR = -5
        self.MAX_SPEED_ANGULAR = 1
        self.MIN_SPEED_ANGULAR = -1
        self.linear_velocity = 0
        self.angular_velocity = 0

        # Environment beacons
        self.beacons = beacons
        # Measurement triplet
        # [distance_from_beacon, bearing, signature]
        self.intercepting_beacons_triplets = []

        # Path followed
        self.noiseless_path = []
        self.actual_path = []
        self.beacons_path = []

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
        self.intercepting_beacons_triplets = []
        estimated_positions = []
        for beacon_id in range(len(self.beacons)):
            distance = self.get_distance_from_beacon(self.beacons[beacon_id]) + self.get_random_noise(self.aggression)
            bearing = self.get_bearing_from_beacon(beacon_id) + self.get_random_noise(self.aggression)
            if distance <= self.sensor_max_radius:
                self.intercepting_beacons_triplets.append([
                    distance,
                    bearing,
                    beacon_id
                ])

                x, y, theta = self.get_estimated_position_from_one_beacon_measurement([
                    distance,
                    bearing,
                    beacon_id
                ])
                estimated_positions.append([x, y])
                # print("Sensor {0}: {1:.2f} : {2:.2f}".format(beacon_id, distance, bearing))
        if len(estimated_positions):
            self.beacons_path.append(np.average(estimated_positions, axis=0))

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

    def increase_noise_factor(self):
        if self.aggression + 10 <= self.MAX_AGGRESSION:
            self.aggression += 10

    def decrease_noise_factor(self):
        if self.aggression - 10 >= self.MIN_AGGRESSION:
            self.aggression -= 10

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
        self.beacons_path = []
        self.linear_velocity = 0
        self.angular_velocity = 0

    def get_distance_from_beacon(self, beacon):
        return np.sqrt((self.actual_position[0] - beacon[0]) ** 2 + (self.actual_position[1] - beacon[1]) ** 2)

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
        actual_linear_velocity = self.linear_velocity + self.get_random_noise(self.aggression)
        actual_angular_velocity = self.angular_velocity + self.get_random_noise(self.aggression)

        new_position = [
            self.actual_position[0] + np.cos(self.actual_theta) * actual_linear_velocity,
            self.actual_position[1] + np.sin(self.actual_theta) * actual_linear_velocity
        ]
        new_theta = self.actual_theta + actual_angular_velocity

        return new_position, new_theta

    def get_bearing_from_beacon(self, beacon_id):
        return np.arctan2(
            self.beacons[beacon_id][1] - self.actual_position[1],
            self.beacons[beacon_id][0] - self.actual_position[0]
        ) - self.actual_theta

    """
    In order to estimate the position from only one beacon we are going
    to use our noiseless_theta that the robot thinks it has.
    The sensor model takes as input the beacon measurement triplet that has
    r (distance to beacon), φ (angle to beacon), s (id of beacon)
    """

    def get_estimated_position_from_one_beacon_measurement(self, beacon_triplet):
        x = self.beacons[beacon_triplet[2]][0] + np.cos(np.pi - beacon_triplet[1] - self.noiseless_theta) * beacon_triplet[0]
        y = self.beacons[beacon_triplet[2]][1] - np.sin(np.pi - beacon_triplet[1] - self.noiseless_theta) * beacon_triplet[0]

        return x, y, beacon_triplet[1]
