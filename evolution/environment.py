import numpy as np
import pygame


class Environment:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BROWN = (222, 184, 135)
    LIGHTYELLOW = (250, 235, 215)
    LIGHTGREEN = (144, 238, 144)
    ROBOT_DIAMETER = 50
    DUST_DOTS_COLOR = LIGHTGREEN
    DUST_DOT_WIDTH = 3
    PADDING = 50

    def __init__(self, width=800, height=800, obstacles=None, robot=None, pygame_enabled=False):
        """
        :param width:           Width of window
        :param height:          Height of window
        :param obstacles:       list of lists where each sublist is [x_from, x_to, y_from, y_to]
        :param robot:           Robot Object
        """

        # initialize dimension of the world
        self.width = width
        self.height = height
        self.pygame_enabled = pygame_enabled

        if self.pygame_enabled:
            pygame.init()
            pygame.font.init()
            self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

            self.gameDisplay = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption('Differential Robot Simulator')
            self.clock = pygame.time.Clock()

        # initialize robot
        self.robot = robot

        # Initialize dust
        self.dust_dots_intensity = 4
        self.dust_matrix_width = int(self.width / self.dust_dots_intensity)
        self.dust_matrix_height = int(self.height / self.dust_dots_intensity)
        self.dust_total = self.dust_matrix_width * self.dust_matrix_height

        # Zero(0) means that there is dust.
        # Minus one (-1) means that robot passed by this spot so there is not dust anymore
        self.dust_matrix = np.ones((self.dust_matrix_width, self.dust_matrix_height))

        self.dust_coverage = 1  # 100% dust coverage when we start
        self.ground_coverage = 1 - self.dust_coverage
        if self.pygame_enabled:
            self.dust_point = [[None for j in range(self.dust_matrix_width)] for i in range(self.dust_matrix_height)]

        # OBSTACLES

        if self.pygame_enabled:
            # initialize walls object (rects)
            self.obstacles_rects = []

        # obstacle coordinates, handy for wall collision
        self.obstacles_coord = obstacles

        # If no coordinates are passed, initialize empty room (with border walls)
        if self.obstacles_coord is None:
            self.obstacles_coord = [
                [0 + self.PADDING, 0 + self.PADDING, self.width - self.PADDING, 0 + self.PADDING],
                [self.width - self.PADDING, 0 + self.PADDING, self.width - self.PADDING,self.height - self.PADDING],
                [self.width - self.PADDING, self.height - self.PADDING, 0 + self.PADDING,self.height - self.PADDING],
                [0 + self.PADDING, self.height - self.PADDING, 0 + self.PADDING, 0 + self.PADDING]
            ]

        # obstacles parameters, handy for sensor values
        self.obstacles_parameters = np.zeros((len(self.obstacles_coord), 2))

        # Add obstacles
        self.add_obstacles()

    def reset(self):
        self.dust_matrix = np.ones((self.dust_matrix_width, self.dust_matrix_height))
        self.dust_coverage = 1  # 100% dust coverage when we start
        self.ground_coverage = 1 - self.dust_coverage

    def add_obstacles(self):
        # obstacles parameters
        for count, obst in enumerate(self.obstacles_coord):
            # sensors functions parameters

            # slope m
            if self.obstacles_coord[count][3] - self.obstacles_coord[count][1] == 0:
                self.obstacles_parameters[count][0] = 0
            else:
                if self.obstacles_coord[count][2] - self.obstacles_coord[count][0] == 0:
                    self.obstacles_parameters[count][0] = float('inf')
                else:
                    self.obstacles_parameters[count][0] = (self.obstacles_coord[count][3] - self.obstacles_coord[count][
                        1]) / ((self.obstacles_coord[count][2] -
                                self.obstacles_coord[count][0]))

            # intercept q
            self.obstacles_parameters[count][1] = self.obstacles_coord[count][1] - (
                    self.obstacles_parameters[count][0] * self.obstacles_coord[count][0])

            if self.pygame_enabled:
                # draw current wall and store Rect object
                curr_wall = pygame.draw.line(self.gameDisplay, self.BLACK,
                                             (self.obstacles_coord[count][0], self.obstacles_coord[count][1]),
                                             (self.obstacles_coord[count][2], self.obstacles_coord[count][3]), 5)
                self.obstacles_rects.append(curr_wall)

            # print("############################ INIT WALLS COORD + PARAMS ############################")
            # print(self.obstacles_coord)
            # print(self.obstacles_parameters)

    def reset_background(self):
        # Draw everything white
        self.gameDisplay.fill(self.WHITE)

    def calculate_dust_and_ground_coverage(self):
        dust_on_screen = np.count_nonzero(self.dust_matrix)
        self.dust_coverage = dust_on_screen / self.dust_total
        self.ground_coverage = 1 - self.dust_coverage

    def draw_dust(self):
        # By knowing the position of the robot and it's radius we can mark all of the dust point in the matrix
        # that the robot "touches"
        # But instead of checking all of the dots of the grid and their distance to the robot we just check the closest
        # ones to it by taking the position of the robot dividing by the dot intensity to bring the robot to the same
        # cartesian system as the dots and then we go -10 +10 up and down and only check this part.
        for i in range(int(self.robot.position[0]) // self.dust_dots_intensity - 10,
                       int(self.robot.position[0]) // self.dust_dots_intensity + 10, 1):
            for j in range(int(self.robot.position[1]) // self.dust_dots_intensity - 10,
                           int(self.robot.position[1]) // self.dust_dots_intensity + 10, 1):
                pythagorian_distance = np.sqrt((self.robot.position[0] - i * self.dust_dots_intensity) ** 2 + (
                        self.robot.position[1] - j * self.dust_dots_intensity) ** 2)
                if pythagorian_distance < self.robot.radius:
                    self.dust_matrix[i][j] = 0

        # Draw this dot if the dust_matrix has the value 1 and pygame is enabled
        if self.pygame_enabled:
            for i in range(self.dust_matrix_width):
                for j in range(self.dust_matrix_height):
                    if self.dust_matrix[i][j] == 1:
                        self.dust_point[i][j] = pygame.draw.circle(self.gameDisplay, self.DUST_DOTS_COLOR,
                                                                   [i * self.dust_dots_intensity,
                                                                    j * self.dust_dots_intensity], self.DUST_DOT_WIDTH)

    def draw_obstacles(self):
        for count, obst in enumerate(self.obstacles_coord):
            pygame.draw.line(self.gameDisplay, self.BLACK,
                             (self.obstacles_coord[count][0], self.obstacles_coord[count][1]),
                             (self.obstacles_coord[count][2], self.obstacles_coord[count][3]), 3)

    def draw_osd(self):
        osd_text_1 = 'Robot Velocity:'
        osd_text_2 = 'Left Wheel:{0}'.format(self.robot.left_wheel_velocity)
        osd_text_3 = 'Right Wheel:{0}'.format(self.robot.right_wheel_velocity)
        osd_text_4 = 'Theta:{0:.2f}'.format(self.robot.theta)
        osd_text_5 = 'Ground Coverage:{0:.2f}'.format(self.ground_coverage)
        osd_1 = self.myfont.render(osd_text_1, False, (0, 0, 0))
        osd_2 = self.myfont.render(osd_text_2, False, (0, 0, 0))
        osd_3 = self.myfont.render(osd_text_3, False, (0, 0, 0))
        osd_4 = self.myfont.render(osd_text_4, False, (0, 0, 0))
        osd_5 = self.myfont.render(osd_text_5, False, (0, 0, 0))
        self.gameDisplay.blit(osd_1, (20, self.height - 120))
        self.gameDisplay.blit(osd_2, (20, self.height - 100))
        self.gameDisplay.blit(osd_3, (20, self.height - 80))
        self.gameDisplay.blit(osd_4, (20, self.height - 60))
        self.gameDisplay.blit(osd_5, (20, self.height - 40))

    def draw_robot(self):
        # Draw the circle of the robot
        self.robot.robot_rect = pygame.draw.circle(self.gameDisplay, self.BLACK,
                                                   [int(self.robot.position[0]), int(self.robot.position[1])],
                                                   self.robot.radius, 3)

        # Draw the small line indicating the direction that the robot is moving
        # End_x and end_y represent where the small line should end, starting from the centre of the circle
        end_x = self.robot.radius * np.cos(2 * np.pi + self.robot.theta)
        end_y = self.robot.radius * np.sin(2 * np.pi + self.robot.theta)

        # Draw the line
        pygame.draw.line(self.gameDisplay, self.BLACK,
                         [int(self.robot.position[0]), int(self.robot.position[1])],
                         [int(self.robot.position[0] + end_x), int(self.robot.position[1] + end_y)],
                         3)

    def draw_sensors(self):
        for sensor in range(len(self.robot.sensors_values)):
            osd_sensor_text = str(round(self.robot.sensors_values[sensor]))
            osd_sensor = self.myfont.render(osd_sensor_text, False, self.BLACK)
            self.gameDisplay.blit(osd_sensor,
                                  (self.robot.sensors_coords[sensor, 2], self.robot.sensors_coords[sensor, 3]))

        # update sensors Rect obj, to update parameters value
        if len(self.robot.sensors_coords) != 0:
            updated_sensors = []
            for sensor in self.robot.sensors_coords:
                updated_sensors.append(pygame.draw.line(self.gameDisplay, self.BLACK,
                                                        [int(sensor[0]), int(sensor[1])],
                                                        [int(sensor[2]), int(sensor[3])],
                                                        3))
            self.robot.sensors_rects = updated_sensors

    def render(self):
        if self.pygame_enabled:
            self.reset_background()

            # Draw components. Ordering of draw matters for the window to look nice
            self.draw_robot()
        self.draw_dust()
        if self.pygame_enabled:
            self.draw_osd()
            self.draw_obstacles()
            self.draw_sensors()

        # Calculate Dust coverage (needed or Evolutionary Algorithm)
        self.calculate_dust_and_ground_coverage()
