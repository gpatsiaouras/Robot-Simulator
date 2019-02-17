from Environment import Environment
from robot import Robot
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# environment without obstacles
# env = Environment()
# environment with obstacles
env = Environment(100, 80, [[0, 60, 20, 23],
                            [80, 83, 0, 43],
                            [20, 83, 43, 46]])

pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Differential Robot Simulator')
clock = pygame.time.Clock()

obstacles = [[0, 60, 20, 23],
             [80, 83, 0, 43],
             [20, 83, 43, 46]]

obs_surfaces = []

walls = []

wall1 = pygame.Surface([60, 3])
wall1.fill(BLACK)
walls.append(wall1)

wall2 = pygame.Surface([3, 40])
wall2.fill(BLACK)
walls.append(wall2)

wall3 = pygame.Surface([63, 3])
wall3.fill(BLACK)
walls.append(wall3)


robot = Robot(10, 0, [100, 100])

robotImage = pygame.image.load('../assets/robot.png')
robotImage = pygame.transform.scale(robotImage, (50, 50))

gameDisplay.blit(wall1, (0, 20))
gameDisplay.blit(wall2, (80, 0))
gameDisplay.blit(wall3, (20, 43))

gameDisplay.blit(robotImage, (100, 100))
gameDisplay.fill(WHITE)
gameExit = False


def game_loop():
    global robotImage
    while not gameExit:
        robot.move()

        # Draw everything white
        gameDisplay.fill(WHITE)
        robotImage = pygame.transform.rotate(robotImage, robot.rotation)
        # Redraw with the new position
        gameDisplay.blit(wall1, (0, 20))
        gameDisplay.blit(wall2, (80, 0))
        gameDisplay.blit(wall3, (20, 43))

        gameDisplay.blit(robotImage, (robot.position[0], robot.position[1]))
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

            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #         robot. = 0

        pygame.display.update()
        clock.tick(30)


game_loop()
pygame.quit()
quit()
