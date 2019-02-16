import numpy as np
import matplotlib
import matplotlib.pyplot as plt


class Environment:

    def __init__(self, width=100, height=100, obstacles=None, robot=None):
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

        # initialize robot/s
        self.robot = robot

        self.obstacles = []

        # obstacle coordinates, handy for wall collision
        self.obstacles_coord = []

        if obstacles is not None:
            self.add_obstacles(obstacles)

    def add_obstacles(self, obstacles):
        self.obstacles.extend(obstacles)
        for obst in obstacles:
            for y in range(obst[2], obst[3]):
                for x in range(obst[0], obst[1]):
                    self.grid[y][x] = 1
                    self.obstacles_coord.append([x, y])

    def render(self):
        img = self.grid
        plt.clf()
        plt.imshow(img, cmap="binary", origin="upper")
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.draw()
        plt.pause(0.001)
