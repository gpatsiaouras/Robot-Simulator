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

# pygame.init()
# pygame.font.init()
# myfont = pygame.font.SysFont('Comic Sans MS', 30)
#
# gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption('Differential Robot Simulator')
# clock = pygame.time.Clock()

# wall_lenght = (SCREEN_HEIGHT / 4) * 3 if SCREEN_HEIGHT < SCREEN_WIDTH else (SCREEN_WIDTH / 4) * 3
# wall_thickness = 3
#
# walls = []
#
# wall1 = pygame.Surface([wall_lenght, wall_thickness])
# wall1.fill(BLACK)
# walls.append(wall1)
#
# wall2 = pygame.Surface([wall_thickness, wall_lenght])
# wall2.fill(BLACK)
# walls.append(wall2)
#
# wall3 = pygame.Surface([wall_lenght, wall_thickness])
# wall3.fill(BLACK)
# walls.append(wall3)

robot = Robot(ROBOT_DIAMETER, 0, [100, 100])
env = Environment(robot=robot)

# robotImage = pygame.image.load('../assets/robot.png')
# robotImage = pygame.transform.scale(robotImage, (ROBOT_DIAMETER, ROBOT_DIAMETER))


# gameDisplay.blit(wall1, (0, SCREEN_HEIGHT/3))
# gameDisplay.blit(wall2, (SCREEN_WIDTH/4*3, 0))
# gameDisplay.blit(wall3, (SCREEN_WIDTH/4, (SCREEN_HEIGHT / 4) * 3))
#
#
# gameDisplay.blit(robotImage, (100, 100))
# gameDisplay.fill(WHITE)
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
