import numpy as np
import matplotlib
import matplotlib.pyplot as plt


class Environment:

    def __init__(self, width=100, height=100, robot=None):
        # initialize dimension of the world
        self.width = width
        self.height = height

        self.grid = np.zeros((self.height, self.width))

        self.obstacles = []

        self.robot = robot

    def render(self, mode='human', close=False):
        img = self.grid
        plt.clf()
        plt.imshow(img, cmap="binary", origin="upper")
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.draw()
        plt.pause(0.001)

