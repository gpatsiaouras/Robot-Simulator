from src.Environment import Environment

# environment without obstacles
# env = Environment()
# environment with obstacles
env = Environment(100, 80, [[0, 40, 18, 21],
                            [55, 58, 0, 50]])

while KeyboardInterrupt:
    env.render()
env.render()
