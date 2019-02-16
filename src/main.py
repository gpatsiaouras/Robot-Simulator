from Environment import Environment
import keyboard

# environment without obstacles
# env = Environment()
# environment with obstacles
env = Environment(100, 80, [[0, 60, 20, 23],
                            [80, 83, 0, 43],
                            [20, 83, 43, 46]])

while True:  # making a loop
    env.render()
    if keyboard.is_pressed('q'):  # if key 'q' is pressed
        print('Closing environment')
        break  # finishing the loop

