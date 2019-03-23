import numpy as np
import pygame


class Environment:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BROWN = (222, 184, 135)
    LIGHTYELLOW = (250, 235, 215)
    LIGHTGREEN = (144, 238, 144)
    ROBOT_DIAMETER = 50
    BEACON_DIAMETER = 10
    PADDING = 50

    def __init__(self, width=800, height=800, obstacles=None, beacons=None, robot=None):
        """
        :param width:           Width of window
        :param height:          Height of window
        :param obstacles:       list of lists where each sublist is [x_from, x_to, y_from, y_to]
        :param robot:           Robot Object
        """

        # initialize dimension of the world
        self.width = width
        self.height = height

        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Localization Robot Simulator')
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
            self.obstacles_coord = [
                [0 + self.PADDING, 0 + self.PADDING, self.width - self.PADDING, 0 + self.PADDING],
                [self.width - self.PADDING, 0 + self.PADDING, self.width - self.PADDING, self.height - self.PADDING],
                [self.width - self.PADDING, self.height - self.PADDING, 0 + self.PADDING, self.height - self.PADDING],
                [0 + self.PADDING, self.height - self.PADDING, 0 + self.PADDING, 0 + self.PADDING]
            ]

        # obstacles parameters, handy for sensor values
        self.obstacles_parameters = np.zeros((len(self.obstacles_coord), 2))

        # Add obstacles
        self.add_obstacles()

        # Add beacons
        self.beacons = beacons

    def reset_background(self):
        # Draw everything white
        self.gameDisplay.fill(self.WHITE)

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

            # draw current wall and store Rect object
            curr_wall = pygame.draw.line(self.gameDisplay, self.BLACK,
                                         (self.obstacles_coord[count][0], self.obstacles_coord[count][1]),
                                         (self.obstacles_coord[count][2], self.obstacles_coord[count][3]), 5)
            self.obstacles_rects.append(curr_wall)

    def draw_obstacles(self):
        for count, obst in enumerate(self.obstacles_coord):
            pygame.draw.line(self.gameDisplay, self.BLACK,
                             (self.obstacles_coord[count][0], self.obstacles_coord[count][1]),
                             (self.obstacles_coord[count][2], self.obstacles_coord[count][3]), 3)

    def draw_osd(self):
        osd_text_1 = 'Robot Velocity:'
        osd_text_2 = 'Linear Velocity:{0}'.format(self.robot.linear_velocity)
        osd_text_3 = 'Angular Velocity:{0}'.format(self.robot.angular_velocity)
        osd_text_4 = 'Theta:{0:.2f}'.format(self.robot.theta)
        osd_1 = self.font.render(osd_text_1, False, (0, 0, 0))
        osd_2 = self.font.render(osd_text_2, False, (0, 0, 0))
        osd_3 = self.font.render(osd_text_3, False, (0, 0, 0))
        osd_4 = self.font.render(osd_text_4, False, (0, 0, 0))
        self.gameDisplay.blit(osd_1, (20, self.height - 120))
        self.gameDisplay.blit(osd_2, (20, self.height - 100))
        self.gameDisplay.blit(osd_3, (20, self.height - 80))
        self.gameDisplay.blit(osd_4, (20, self.height - 60))

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

        # Draw robot sensor range
        pygame.draw.circle(self.gameDisplay,
                           self.GREEN if len(self.robot.intercepting_beacons_positions) == 0 else self.RED,
                           [int(self.robot.position[0]), int(self.robot.position[1])],
                           self.robot.sensor_max_radius, 3)

    def draw_beacons(self):
        for beacon in self.beacons:
            pygame.draw.circle(self.gameDisplay, self.RED,
                               [int(beacon[0]), int(beacon[1])], self.BEACON_DIAMETER, 10)

    def draw_path(self):
        for position in self.robot.path:
            pygame.draw.circle(self.gameDisplay, self.BLUE, [int(position[0]), int(position[1])], 1)

    def draw_interceptions(self):
        for intercepting_beacon in self.robot.intercepting_beacons_positions:
            pygame.draw.line(self.gameDisplay, self.RED,
                             [int(self.robot.position[0]), int(self.robot.position[1])],
                             [int(intercepting_beacon[0]), int(intercepting_beacon[1])],
                             3)

    def render(self):
        self.reset_background()
        # Draw components. Ordering of draw matters for the window to look nice
        self.draw_robot()
        self.draw_beacons()
        self.draw_interceptions()
        self.draw_path()
        self.draw_osd()
        self.draw_obstacles()
