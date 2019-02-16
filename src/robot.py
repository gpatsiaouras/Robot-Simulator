class Robot:
    def __init__(self, diameter, wheel_radius, initial_rotation, initial_position):
        # Robot specifications
        self.diameter = diameter
        self.radius = diameter / 2
        self.wheel_radius = wheel_radius
        self.rotation = initial_rotation

        self.position = initial_position

        # Motor variables
        self.MAX_SPEED = 100
        self.MIN_SPEED = -100
        self.left_wheel_speed = 0
        self.right_wheel_speed = 0

        # Sensors
        # 12 sensors perimetrically, 30o degrees between them
        # sensor 0 is the one in front of the robot.
        # Values go from 0 to 200, 200 being out of reach
        self.distance_sensors = [200 for i in range(12)]

    def update_sensor_values(self):
        pass

    def move(self, x, y):
        self.position[0] += x
        self.position[1] += y

    def increment_left_wheel(self):
        if self.left_wheel_speed + 10 <= self.MAX_SPEED and self.left_wheel_speed >= self.MIN_SPEED:
            self.left_wheel_speed += 10

    def decrement_left_wheel(self):
        if self.left_wheel_speed + 10 <= self.MAX_SPEED and self.left_wheel_speed >= self.MIN_SPEED:
            self.left_wheel_speed -= 10

    def increment_right_wheel(self):
        if self.right_wheel_speed + 10 <= self.MAX_SPEED and self.right_wheel_speed >= self.MIN_SPEED:
            self.right_wheel_speed += 10

    def decrement_right_wheel(self):
        if self.right_wheel_speed + 10 <= self.MAX_SPEED and self.right_wheel_speed >= self.MIN_SPEED:
            self.right_wheel_speed -= 10

    def increment_both_wheels(self):
        self.increment_left_wheel()
        self.increment_right_wheel()

    def decrement_both_wheels(self):
        self.decrement_left_wheel()
        self.decrement_right_wheel()
