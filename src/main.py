from Environment import Environment
from robot import Robot
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
ROBOT_DIAMETER = 50
PADDING = 10
CENTER_W = SCREEN_WIDTH / 2
CENTER_H = SCREEN_HEIGHT / 2

empty_room = [[0 + PADDING, 0 + PADDING, SCREEN_WIDTH - PADDING, 0 + PADDING],
                                    [SCREEN_WIDTH - PADDING, 0 + PADDING, SCREEN_WIDTH - PADDING,
                                     SCREEN_HEIGHT - PADDING],
                                    [SCREEN_WIDTH - PADDING, SCREEN_HEIGHT - PADDING, 0 + PADDING,
                                     SCREEN_HEIGHT - PADDING],
                                    [0 + PADDING, SCREEN_HEIGHT - PADDING, 0 + PADDING, 0 + PADDING]
                                    ]

room_1 = [[0 + PADDING, 0 + PADDING, SCREEN_WIDTH - PADDING, 0 + PADDING],
                                    [SCREEN_WIDTH - PADDING, 0 + PADDING, SCREEN_WIDTH - PADDING,
                                     SCREEN_HEIGHT - PADDING],
                                    [SCREEN_WIDTH - PADDING, SCREEN_HEIGHT - PADDING, 0 + PADDING,
                                     SCREEN_HEIGHT - PADDING],
                                    [0 + PADDING, SCREEN_HEIGHT - PADDING, 0 + PADDING, 0 + PADDING],
                                    [CENTER_W - 100, CENTER_H - 100, CENTER_W + 100, CENTER_H - 100],
                                    [CENTER_W + 100, CENTER_H - 100, CENTER_W + 100, CENTER_H + 100],
                                    [CENTER_W + 100, CENTER_H + 100, CENTER_W - 100, CENTER_H + 100],
                                    [CENTER_W - 100, CENTER_H + 100, CENTER_W - 100, CENTER_H - 100]]

robot = Robot(ROBOT_DIAMETER, 0, [100, 100])
# env = Environment(SCREEN_WIDTH, SCREEN_HEIGHT, None, robot)
env = Environment(SCREEN_WIDTH, SCREEN_HEIGHT, room_1, robot)
robot.setObst(env.obstacles_rects, env.obstacles_parameters)

gameExit = False
env.render()


def game_loop():
    while not gameExit:
        robot.move()
        robot.check_sensors()
        env.render()

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

        pygame.display.update()
        env.clock.tick(25)


game_loop()
pygame.quit()
quit()
