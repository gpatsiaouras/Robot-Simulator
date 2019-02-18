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
        self.sensors_values = []
        self.init_sensors()
        self.sensors_rects = []
        self.sensors_parameters = np.zeros((12, 2))
        # walls for sensor values
        self.walls = []
        self.walls_parameters = np.zeros((4, 2))

    def update_sensor_values(self):
        count = 0
        for angle in range(0, 360, 30):
            # sensor origin coords
            self.sensors_coords[count, 0] = self.position[0] + self.radius * np.cos(self.theta + np.radians(angle))
            self.sensors_coords[count, 1] = self.position[1] + self.radius * np.sin(self.theta + np.radians(angle))

            # sensor tips coords
            self.sensors_coords[count, 2] = self.position[0] + self.sens_radius * np.cos(self.theta + np.radians(angle))
            self.sensors_coords[count, 3] = self.position[1] + self.sens_radius * np.sin(self.theta + np.radians(angle))

            # sensors functions parameters
            # slope m
            self.sensors_parameters[count, 0] = (self.sensors_coords[count, 2] - self.sensors_coords[count, 3]) / \
                                                (self.sensors_coords[count, 0] - self.sensors_coords[count, 1])
            # intercept q
            self.sensors_parameters[count, 1] = self.sensors_coords[count, 1] - (
                    self.sensors_parameters[count, 0] * self.sensors_coords[count, 0])

            count = count + 1
        # print(self.sensors_parameters)

    def move(self):
        if self.left_wheel_velocity != self.right_wheel_velocity:
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

        # update sensors
        self.update_sensor_values()

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
        self.sensors_values = [200 for i in range(12)]
        self.sensors_coords = np.zeros((12, 4))
        self.sens_radius = 3 * self.radius

    def setObst(self, walls):
        self.walls = walls
        self.walls_parameters = np.zeros((len(walls), 2))
        c = 0
        for wall in walls:
            # slope m
            # TODO: change m and q calculation considering that now walls are lines
            self.walls_parameters[c, 0] = wall.bottomleft[0] - wall.bottomright[0] / wall.bottomleft[1] - wall.bottomright[1]
            # intercept q
            self.walls_parameters[c, 1] = wall.bottomleft[1] - (self.walls_parameters[c, 0] * wall.bottomleft[0])

    def check_sensors(self):
        for sensor in self.sensors_rects:
            for wall in self.walls:
                if sensor.colliderect(wall):
                    print(wall)
                    print(sensor)
