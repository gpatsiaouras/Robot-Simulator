from Environment import Environment
import keyboard
import sys, tty, termios


def get_character():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# environment without obstacles
# env = Environment()
# environment with obstacles
env = Environment(100, 80, [[0, 60, 20, 23],
                            [80, 83, 0, 43],
                            [20, 83, 43, 46]])

while True:  # making a loop
    env.render()

    char = get_character()

    if char == "q":  # if key 'q' is pressed
        print('Closing environment')
        break  # finishing the loop

