import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pygame


class Environment:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    ROBOT_DIAMETER = 50

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
        self.map = pygame.Surface([self.height, self.width])
        self.map.fill((255, 255, 255))
        self.rect = self.map.get_rect()
        # initialize robot/s
        self.robot = robot

        self.obstacles = []

        # obstacle coordinates, handy for wall collision
        self.obstacles_coord = []

        pygame.init()
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)

        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Differential Robot Simulator')
        self.clock = pygame.time.Clock()

        self.add_obstacles()

        osd_text_1 = 'Robot Velocity:'
        osd_text_2 = 'Left Wheel:{0}'.format(robot.left_wheel_velocity)
        osd_text_3 = 'Right Wheel:{0}'.format(robot.right_wheel_velocity)
        osd_text_4 = 'Theta:{0}'.format(robot.theta)

        self.osd_1 = myfont.render(osd_text_1, False, (0, 0, 0))
        self.osd_2 = myfont.render(osd_text_2, False, (0, 0, 0))
        self.osd_3 = myfont.render(osd_text_3, False, (0, 0, 0))
        self.osd_4 = myfont.render(osd_text_4, False, (0, 0, 0))

        if self.robot is not None:
            self.robotImage = pygame.image.load('../assets/robot.png')
            self.robotImage = pygame.transform.scale(self.robotImage, (self.ROBOT_DIAMETER, self.ROBOT_DIAMETER))

    def add_obstacles(self):
        self.wall_lenght = (self.height / 4) * 3 if self.height < self.width else (self.width / 4) * 3
        self.wall_thickness = 3

        self.walls = []

        self.wall1 = pygame.Surface([self.wall_lenght, self.wall_thickness])
        self.wall1.fill(self.BLACK)
        self.walls.append(self.wall1)

        self.wall2 = pygame.Surface([self.wall_thickness, self.wall_lenght])
        self.wall2.fill(self.BLACK)
        self.walls.append(self.wall2)

        self.wall3 = pygame.Surface([self.wall_lenght, self.wall_thickness])
        self.wall3.fill(self.BLACK)
        self.walls.append(self.wall3)

    def render(self):

        # Draw everything white
        self.gameDisplay.fill(self.WHITE)
        # Redraw with the new position
        self.gameDisplay.blit(self.wall1, (0, self.height/ 3))
        self.gameDisplay.blit(self.wall2, (self.width / 4 * 3, 0))
        self.gameDisplay.blit(self.wall3, (self.width / 4, (self.height / 4) * 3))
        self.gameDisplay.blit(self.osd_1, (0, self.height - 80))
        self.gameDisplay.blit(self.osd_2, (0, self.height - 60))
        self.gameDisplay.blit(self.osd_3, (0, self.height - 40))
        self.gameDisplay.blit(self.osd_4, (0, self.height - 20))

        if self.robot is not None:
            self.gameDisplay.blit(self.robotImage, (self.robot.position[0], self.robot.position[1]))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
