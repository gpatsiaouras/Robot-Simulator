import numpy as np

from localization.kalman import Kalman


class Robot:
    def __init__(self, diameter, initial_theta, initial_position, beacons):
        # Robot specifications
        self.diameter = diameter
        self.radius = int(diameter / 2)
        self.dead_reckoning_position = initial_position
        self.perceived_position = initial_position
        self.actual_position = initial_position
        self.sensor_max_radius = 170

        # Rotation is in rads
        self.dead_reckoning_theta = initial_theta
        self.perceived_theta = initial_theta
        self.actual_theta = initial_theta

        # Values between 100 and 1000 give reasonable trajectories
        # higher values result in less aggression
        self.aggression = 10
        self.MIN_AGGRESSION = 5
        self.MAX_AGGRESSION = 200
        self.THETA_NOISE = 0.1

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
        self.dead_reckoning_path = []
        self.actual_path = []
        self.corrected_path = []
        self.beacons_path = []

        # Kalman Filters
        self.kalman = Kalman(self)
        self.beacons_estimates_position = 0

    def move(self):
        self.check_beacons()

        if self.linear_velocity != 0 or self.angular_velocity != 0:
            new_dead_reckoning_position, new_dead_reckoning_theta = self.get_dead_reckoning_position()
            new_actual_position, new_actual_theta = self.get_actual_position()

            # update positions
            self.actual_position = new_actual_position
            self.dead_reckoning_position = new_dead_reckoning_position

            # update thetas
            self.actual_theta = new_actual_theta
            self.dead_reckoning_theta = new_dead_reckoning_theta

            # Save paths
            self.dead_reckoning_path.append(new_dead_reckoning_position)
            self.actual_path.append(new_actual_position)

            # Keep theta from exploding
            self.actual_theta %= 2 * np.pi
            self.dead_reckoning_theta %= 2 * np.pi

            self.kalman.prediction(np.array([[self.linear_velocity],
                                             [self.angular_velocity]]))
            state, covariance = self.kalman.correction(np.array(self.beacons_estimates_position))

            # self.corrected_path.append()
            self.perceived_position = [state.item(0), state.item(1)]
            self.perceived_theta = state.item(2)
            # self.perceived_theta = self.kalman.predicted_states_history[-1]

            print("kalman theta= ", self.perceived_theta, "         real theta= ", self.actual_theta)

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

                x, y = self.get_estimated_position_from_one_beacon_measurement([
                    distance,
                    bearing,
                    beacon_id
                ])
                theta = self.get_estimated_theta_from_one_beacon(x, y, beacon_id, bearing)
                estimated_positions.append(np.array([[x], [y], [theta]]))
                # print("Sensor {0}: {1:.2f} : {2:.2f}".format(beacon_id, distance, bearing))
        if len(estimated_positions) > 0:
            # self.beacons_estimates_position = estimated_positions[-1]
            self.beacons_estimates_position = np.average(estimated_positions, axis=0)
            self.beacons_path.append([estimated_positions[-1].item(0), estimated_positions[-1].item(1)])

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
        if self.aggression + 5 <= self.MAX_AGGRESSION:
            self.aggression += 5

    def decrease_noise_factor(self):
        if self.aggression - 5 >= self.MIN_AGGRESSION:
            self.aggression -= 5

    def stop_motors(self):
        self.angular_velocity = 0
        self.linear_velocity = 0

    def reset(self, theta, position):
        self.actual_theta = theta
        self.perceived_theta = theta
        self.dead_reckoning_theta = theta
        self.actual_position = position
        self.perceived_position = position
        self.dead_reckoning_position = position
        self.actual_path = []
        self.dead_reckoning_path = []
        self.beacons_path = []
        self.corrected_path = []
        self.kalman.predicted_states_history = []
        self.kalman.corrected_states_history = []
        self.linear_velocity = 0
        self.angular_velocity = 0

    def get_distance_from_beacon(self, beacon):
        return np.sqrt((self.actual_position[0] - beacon[0]) ** 2 + (self.actual_position[1] - beacon[1]) ** 2)

    def get_random_noise(self, aggression):
        return aggression * np.random.randint(-1, 1) / 1000

    def get_dead_reckoning_position(self):
        new_position = [
            self.dead_reckoning_position[0] + np.cos(self.dead_reckoning_theta) * self.linear_velocity,
            self.dead_reckoning_position[1] + np.sin(self.dead_reckoning_theta) * self.linear_velocity
        ]
        new_theta = self.dead_reckoning_theta + self.angular_velocity

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
    to use our perceived_theta that the robot thinks it has.
    The sensor model takes as input the beacon measurement triplet that has
    r (distance to beacon), φ (angle to beacon), s (id of beacon)
    """

    def get_estimated_position_from_one_beacon_measurement(self, beacon_triplet):
        x = self.beacons[beacon_triplet[2]][0] + np.cos(np.pi - beacon_triplet[1] - np.random.normal(self.actual_theta, self.THETA_NOISE)) * \
            beacon_triplet[0]
        y = self.beacons[beacon_triplet[2]][1] - np.sin(np.pi - beacon_triplet[1] - np.random.normal(self.actual_theta, self.THETA_NOISE)) * \
            beacon_triplet[0]

        return x, y

    # def get_estimated_theta_from_one_beacon(self, x, y, beacon_id, bearing):
    #     dy = self.beacons[beacon_id][1] - y
    #     dx = self.beacons[beacon_id][0] - x
    #
    #     a = np.arctan2(dy, dx)
    #     # print("\n\nalpha = ", a, "\n\n")
    #     return (2 * np.pi - a - bearing) % 2*np.pi

    def get_estimated_theta_from_one_beacon(self, x, y, beacon_id, bearing):
        dy = self.beacons[beacon_id][1] - y
        dx = self.beacons[beacon_id][0] - x
        # dy = self.beacons[beacon_id][1] - self.actual_position[1]
        # dx = self.beacons[beacon_id][0] - self.actual_position[0]

        a = np.arctan2(dy, dx)
        # print("\n\nalpha = ", a, "\n\n")
        # return (2 * np.pi - a - bearing) % 2*np.pi
        return (- bearing + a)
