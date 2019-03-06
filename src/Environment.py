import numpy as np
import pygame


class Environment:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    ROBOT_DIAMETER = 50
    PADDING = 50

    def __init__(self, width=800, height=800, obstacles=None, robot=None):
        """
        :param width:
        :param height:
        :param obstacles:       list of lists where each sublist is [x_from, x_to, y_from, y_to]
        :param robot:           list of robots object in the environment
        """

        # initialize dimension of the world
        self.width = width
        self.height = height

        # initialize matrix with zeros representing the map
        self.grid = np.zeros((self.height, self.width))
        # self.map = pygame.Surface([self.height + self.PADDING, self.width + self.PADDING])
        self.map = pygame.Surface([self.height, self.width])
        self.map.fill((255, 255, 255))
        self.rect = self.map.get_rect()

        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Differential Robot Simulator')
        self.clock = pygame.time.Clock()

        # initialize robot
        self.robot = robot

        # OBSTACLES

        # initialize walls object (rects)
        self.obstacles_rects = []

        # obstacle coordinates, handy for wall collision
        self.obstacles_coord = obstacles

        # If no coordinates are passed, initialize empty room (with border walls)
        if self.obstacles_coord is None:
            self.obstacles_coord = [[0 + self.PADDING, 0 + self.PADDING, self.width - self.PADDING, 0 + self.PADDING],
                                    [self.width - self.PADDING, 0 + self.PADDING, self.width - self.PADDING, self.height - self.PADDING],
                                    [self.width - self.PADDING, self.height - self.PADDING, 0 + self.PADDING, self.height - self.PADDING],
                                    [0 + self.PADDING, self.height - self.PADDING, 0 + self.PADDING, 0 + self.PADDING]
                                    ]

        # obstacles parameters, handy for sensor values
        self.obstacles_parameters = np.zeros((len(self.obstacles_coord), 2))

        # Add obstacles
        self.add_obstacles()

    def add_obstacles(self):

        # for counter, obst in enumerate(self.obstacles_rects):

        # obstacles parameters
        for count, obst in enumerate(self.obstacles_coord):
            # sensors functions parameters

            # slope m
            try:
                self.obstacles_parameters[count][0] = (self.obstacles_coord[count][3] - self.obstacles_coord[count][1]) / (
                        (self.obstacles_coord[count][2] - self.obstacles_coord[count][0]))
                # intercept q
                self.obstacles_parameters[count][1] = self.obstacles_coord[count][1] - (
                        self.obstacles_parameters[count][0] * self.obstacles_coord[count][0])
            except ZeroDivisionError:
                pass

            # draw current wall and store Rect object
            curr_wall = pygame.draw.line(self.gameDisplay, self.BLACK,
                                         (self.obstacles_coord[count][0], self.obstacles_coord[count][1]),
                                         (self.obstacles_coord[count][2], self.obstacles_coord[count][3]), 5)
            self.obstacles_rects.append(curr_wall)

        # wall1 = pygame.draw.line(self.gameDisplay, self.BLACK, (self.obstacles_coord[0, 0], self.obstacles_coord[0, 1]),
        #                          (self.obstacles_coord[0, 2], self.obstacles_coord[0, 3]), 3)
        # self.obstacles_rects.append(wall1)
        #
        # wall2 = pygame.draw.line(self.gameDisplay, self.BLACK, (self.obstacles_coord[1, 0], self.obstacles_coord[1, 1]),
        #                          (self.obstacles_coord[1, 2], self.obstacles_coord[1, 3]), 3)
        # self.obstacles_rects.append(wall2)
        #
        # wall3 = pygame.draw.line(self.gameDisplay, self.BLACK, (self.obstacles_coord[2, 0], self.obstacles_coord[2, 1]),
        #                          (self.obstacles_coord[2, 2], self.obstacles_coord[2, 3]), 3)
        # self.obstacles_rects.append(wall3)

    def redraw_obstacles(self):
        for count, obst in enumerate(self.obstacles_coord):
            pygame.draw.line(self.gameDisplay, self.BLACK,
                             (self.obstacles_coord[count][0], self.obstacles_coord[count][1]),
                             (self.obstacles_coord[count][2], self.obstacles_coord[count][3]), 3)

        # pygame.draw.line(self.gameDisplay, self.BLACK, (self.obstacles_coord[0, 0], self.obstacles_coord[0, 1]),
        #                  (self.obstacles_coord[0, 2], self.obstacles_coord[0, 3]), 3)
        # pygame.draw.line(self.gameDisplay, self.BLACK, (self.obstacles_coord[1, 0], self.obstacles_coord[1, 1]),
        #                  (self.obstacles_coord[1, 2], self.obstacles_coord[1, 3]), 3)
        # pygame.draw.line(self.gameDisplay, self.BLACK, (self.obstacles_coord[2, 0], self.obstacles_coord[2, 1]),
        #                  (self.obstacles_coord[2, 2], self.obstacles_coord[2, 3]), 3)

    def render(self):

        # Draw everything white
        self.gameDisplay.fill(self.WHITE)
        # Redraw with the new position
        self.redraw_obstacles()

        # Check validity of rendering
        if self.robot is None:
            return

        osd_text_1 = 'Robot Velocity:'
        osd_text_2 = 'Left Wheel:{0}'.format(self.robot.left_wheel_velocity)
        osd_text_3 = 'Right Wheel:{0}'.format(self.robot.right_wheel_velocity)
        osd_text_4 = 'Theta:{0}'.format(self.robot.theta)
        osd_1 = self.myfont.render(osd_text_1, False, (0, 0, 0))
        osd_2 = self.myfont.render(osd_text_2, False, (0, 0, 0))
        osd_3 = self.myfont.render(osd_text_3, False, (0, 0, 0))
        osd_4 = self.myfont.render(osd_text_4, False, (0, 0, 0))
        self.gameDisplay.blit(osd_1, (0, self.height - 80))
        self.gameDisplay.blit(osd_2, (0, self.height - 60))
        self.gameDisplay.blit(osd_3, (0, self.height - 40))
        self.gameDisplay.blit(osd_4, (0, self.height - 20))

        self.robot.robot_rect = pygame.draw.circle(self.gameDisplay, self.BLACK,
                                                   [int(self.robot.position[0]), int(self.robot.position[1])],
                                                   self.robot.radius, 3)
        end_x = self.robot.radius * np.cos(2 * np.pi + self.robot.theta)
        end_y = self.robot.radius * np.sin(2 * np.pi + self.robot.theta)
        pygame.draw.line(self.gameDisplay, self.BLACK,
                         [int(self.robot.position[0]), int(self.robot.position[1])],
                         [int(self.robot.position[0] + end_x), int(self.robot.position[1] + end_y)],
                         3)

        for sensor in range(len(self.robot.sensors_values)):
            osd_sensor_text = str(round(self.robot.sensors_values[sensor]))
            osd_sensor = self.myfont.render(osd_sensor_text, False, (0, 255, 0))
            self.gameDisplay.blit(osd_sensor,
                                  (self.robot.sensors_coords[sensor, 2], self.robot.sensors_coords[sensor, 3]))

        # update sensors Rect obj, to update parameters value
        if len(self.robot.sensors_coords) != 0:
            updated_sensors = []
            for sensor in self.robot.sensors_coords:
                updated_sensors.append(pygame.draw.line(self.gameDisplay, self.GREEN,
                                                        [int(sensor[0]), int(sensor[1])],
                                                        [int(sensor[2]), int(sensor[3])],
                                                        3))
            self.robot.sensors_rects = updated_sensors
