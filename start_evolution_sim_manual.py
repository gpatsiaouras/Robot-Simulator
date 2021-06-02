from evolution import Simulator
import rooms
import numpy as np

if __name__ == '__main__':
    simulator = Simulator(rooms.room_1, autonomous=False, pygame_enabled=True)
    simulator.network.weights1 = np.random.rand(17, 5)
    simulator.network.weights2 = np.random.rand(5, 2)
    simulator.run()
