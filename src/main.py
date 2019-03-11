import numpy as np
from Environment import Environment
from ann import ANN
from robot import Robot
import pygame
import rooms

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
ROBOT_DIAMETER = 50
PADDING = 10
CENTER_W = SCREEN_WIDTH / 2
CENTER_H = SCREEN_HEIGHT / 2


class Simulator:
    def __init__(self, room, max_steps=-1, autonomous=False):
        self.autonomous = autonomous
        self.robot = Robot(ROBOT_DIAMETER, 0, [100, 100])
        self.env = Environment(SCREEN_WIDTH, SCREEN_HEIGHT, room, self.robot)
        self.robot.setObst(self.env.obstacles_rects, self.env.obstacles_parameters)
        self.game_exit = False

        self.network = ANN()

        self.current_step = 0
        self.max_steps = max_steps
        self.env.render()

    def run(self):
        while not self.game_exit:
            self.robot.move()
            self.robot.check_sensors()
            self.env.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.robot.increment_left_wheel()
                    if event.key == pygame.K_s:
                        self.robot.decrement_left_wheel()
                    if event.key == pygame.K_o:
                        self.robot.increment_right_wheel()
                    if event.key == pygame.K_l:
                        self.robot.decrement_right_wheel()
                    if event.key == pygame.K_t:
                        self.robot.increment_both_wheels()
                    if event.key == pygame.K_g:
                        self.robot.decrement_both_wheels()
                    if event.key == pygame.K_x:
                        self.robot.stop_motors()

            if self.autonomous:
                # Change the sensor values from a list to numpy array so that the ann can read it
                # and make it uniform
                sensors_as_vector = np.asarray(self.robot.sensors_values) * 0.01
                motor_values = self.network.feed_forward(sensors_as_vector)
                self.robot.left_wheel_velocity = motor_values[0] * 5
                self.robot.right_wheel_velocity = motor_values[1] * 5

            pygame.display.update()
            self.env.clock.tick(25)

            # Increment step and check if the simulator should exit. Only when steps are defined
            self.current_step += 1
            if self.max_steps != -1 and self.current_step >= self.max_steps:
                self.game_exit = True


if __name__ == '__main__':
    simulator = Simulator(rooms.room_1, autonomous=True)
    simulator.network.weights1 = np.random.rand(17, 5)
    simulator.network.weights2 = np.random.rand(5, 2)
    simulator.run()
