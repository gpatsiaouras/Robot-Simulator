import numpy as np
import pygame


class Environment:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
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
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Differential Robot Simulator')
        self.clock = pygame.time.Clock()

        self.add_obstacles()

    def add_obstacles(self):
        self.wall_lenght = (self.height / 4) * 3 if self.height < self.width else (self.width / 4) * 3
        self.wall_thickness = 3

        self.walls = []

        self.wall1 = pygame.draw.line(self.gameDisplay, self.BLACK, (0, self.height / 3),
                                      (self.wall_lenght, self.height / 3), 3)
        # self.wall1 = pygame.Surface([self.wall_lenght, self.wall_thickness])
        # self.wall1.fill(self.BLACK)
        self.walls.append(self.wall1)

        self.wall2 = pygame.draw.line(self.gameDisplay, self.BLACK, (self.width / 4 * 3, 0),
                                      (self.width / 4 * 3, self.wall_lenght), 3)
        # self.wall2 = pygame.Surface([self.wall_thickness, self.wall_lenght])
        # self.wall2.fill(self.BLACK)
        self.walls.append(self.wall2)

        self.wall3 = pygame.draw.line(self.gameDisplay, self.BLACK, (self.width / 4, (self.height / 6) * 5),
                                      ((self.width / 4) + self.wall_lenght, (self.height / 6) * 5), 3)
        # self.wall3 = pygame.Surface([self.wall_lenght, self.wall_thickness])
        # self.wall3.fill(self.BLACK)
        self.walls.append(self.wall3)

    def render(self):

        # Draw everything white
        self.gameDisplay.fill(self.WHITE)
        # Redraw with the new position
        self.gameDisplay.blit(self.wall1, (0, self.height / 3))
        self.gameDisplay.blit(self.wall2, (self.width / 4 * 3, 0))
        self.gameDisplay.blit(self.wall3, (self.width / 4, (self.height / 4) * 3))

        if self.robot is not None:
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

            pygame.draw.circle(self.gameDisplay, self.BLACK, [int(self.robot.position[0]), int(self.robot.position[1])],
                               50, 3)
            end_x = self.robot.diameter * np.cos(2 * np.pi + self.robot.theta)
            end_y = self.robot.diameter * np.sin(2 * np.pi + self.robot.theta)
            pygame.draw.line(self.gameDisplay, self.BLACK,
                             [int(self.robot.position[0]), int(self.robot.position[1])],
                             [int(self.robot.position[0] + end_x), int(self.robot.position[1] + end_y)],
                             3)

            # check if sensor list is not empty
            if len(self.robot.sensors_coords) != 0:
                updated_sensors = []
                for sensor in self.robot.sensors_coords:
                    updated_sensors.append(pygame.draw.line(self.gameDisplay, self.GREEN,
                                                            [int(sensor[0]), int(sensor[1])],
                                                            [int(sensor[2]), int(sensor[3])],
                                                            3))
                self.robot.sensors_rects = updated_sensors
