from Environment import Environment
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
    def __init__(self, room):
        self.robot = Robot(ROBOT_DIAMETER, 0, [100, 100])
        self.env = Environment(SCREEN_WIDTH, SCREEN_HEIGHT, room, self.robot)
        self.robot.setObst(self.env.obstacles_rects, self.env.obstacles_parameters)
        self.game_exit = False
        self.env.render()

    def game_loop(self):
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

            pygame.display.update()
            self.env.clock.tick(25)

    def run(self):
        self.game_loop()
        pygame.quit()
        quit()


if __name__ == '__main__':
    simulator = Simulator(rooms.room_1)
    simulator.run()
