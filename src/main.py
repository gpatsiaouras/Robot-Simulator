from Environment import Environment
from robot import Robot
import pygame
import numpy as np

# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 800
ROBOT_DIAMETER = 50
# environment


robot = Robot(ROBOT_DIAMETER, 0, [100, 100])
env = Environment(robot=robot)

gameExit = False


def game_loop():
    global robotImage
    while not gameExit:

        robot.move()
        # RENDER

        env.render()

        # TODO It doesn't work for now
        # robotImage = pygame.transform.rotate(robotImage, robot.theta * 180 / np.pi)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    robot.increment_left_wheel()
                if event.key == pygame.K_s:
                    robot.decrement_left_wheel()
                if event.key == pygame.K_o:
                    robot.increment_right_wheel()
                if event.key == pygame.K_l:
                    robot.decrement_right_wheel()
                if event.key == pygame.K_t:
                    robot.increment_both_wheels()
                if event.key == pygame.K_g:
                    robot.decrement_both_wheels()
                if event.key == pygame.K_x:
                    robot.stop_motors()

            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #         robot. = 0

        pygame.display.update()
        env.clock.tick(25)


game_loop()
pygame.quit()
quit()
