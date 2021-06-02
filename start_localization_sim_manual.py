from localization import Simulator
import rooms

if __name__ == '__main__':
    simulator = Simulator(rooms.empty_room, rooms.beacons_empty)
    simulator.run()
