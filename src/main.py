from Environment import Environment
from robot import Robot
import pygame

pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Differential Robot Simulator')
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# environment without obstacles
# env = Environment()
# environment with obstacles
env = Environment(100, 80, [[0, 60, 20, 23],
                            [80, 83, 0, 43],
                            [20, 83, 43, 46]])

robot = Robot(10, 2, [100,100])

# robotImage = pygame.image.load('../assets/robot.gif')
# gameDisplay.blit(robotImage, (100, 100))
gameDisplay.fill(WHITE)
pygame.draw.circle(gameDisplay, BLACK, [80, 80], 80, 5)
gameExit = False


def game_loop():
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    robot.move(0, 10)
                if event.key == pygame.K_s:
                    robot.move(0, -10)
                if event.key == pygame.K_o:
                    robot.move(10, 0)
                if event.key == pygame.K_l:
                    robot.move(-10, 0)

            gameDisplay.fill(WHITE)
            pygame.draw.circle(gameDisplay, BLACK, [robot.position[0], robot.position[1]], 40, 1)

            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #         robot. = 0

        pygame.display.update()
        clock.tick(60)


game_loop()
pygame.quit()
quit()
