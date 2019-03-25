from localization.environment import Environment
from localization.robot import Robot
import pygame
import rooms

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
ROBOT_DIAMETER = 50
PADDING = 10
CENTER_W = SCREEN_WIDTH / 2
CENTER_H = SCREEN_HEIGHT / 2


class Simulator:
    def __init__(self, room, beacons):
        self.robot = Robot(ROBOT_DIAMETER, 0, [60, 60], beacons)
        self.env = Environment(SCREEN_WIDTH, SCREEN_HEIGHT, room, beacons, self.robot)
        self.game_exit = False

        self.current_step = 0
        self.env.render()

    def reset(self):
        self.game_exit = False
        self.current_step = 0
        self.robot.reset(theta=0, position=[60, 60])
        self.env.render()

    def run(self):
        while not self.game_exit:
            self.robot.move()
            self.env.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.robot.increment_linear_velocity()
                    if event.key == pygame.K_s:
                        self.robot.decrement_linear_velocity()
                    if event.key == pygame.K_a:
                        self.robot.decrement_angular_velocity()
                    if event.key == pygame.K_d:
                        self.robot.increment_angular_velocity()
                    if event.key == pygame.K_p:
                        self.robot.increase_noise_factor()
                    if event.key == pygame.K_l:
                        self.robot.decrease_noise_factor()
                    if event.key == pygame.K_x:
                        self.robot.stop_motors()
                    if event.key == pygame.K_z:
                        self.reset()

            pygame.display.update()
            self.env.clock.tick(25)

            self.current_step += 1


if __name__ == '__main__':
    simulator = Simulator(rooms.empty_room, rooms.beacons_empty)
    simulator.run()
