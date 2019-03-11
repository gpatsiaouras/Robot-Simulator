import numpy as np
import rooms
from main import Simulator


class EvolutionaryAlgorithm:
    def __init__(self, number_of_generations, robots_per_generation, exploration_steps):
        # Input Parameters
        self.number_of_generations = number_of_generations
        self.robots_per_generation = robots_per_generation

        # Fixed Parameters
        self.number_of_parents_mating = 4
        self.number_of_weights = 12

        # Specify population
        self.population_size = (self.robots_per_generation, self.number_of_weights)

        # Initialize simulators
        self.simulators_list = []
        for i in range(self.robots_per_generation):
            sim = Simulator(rooms.room_1, exploration_steps)
            self.simulators_list.append(sim)

    def fitness(self):
        pass

    def select_mating_pool(self):
        pass

    def crossover(self):
        pass

    def mutation(self):
        pass

    def evolve(self):
        # new_population = np.random.uniform(low=0.0, high=1.0, size=self.population_size)

        for generation in range(self.number_of_generations):
            # For each chromesome (robot in a different environment) run the simulation
            for sim_num in range(self.robots_per_generation):
                self.simulators_list[sim_num].run()

            # Take the fitness of each chromosome in the population
            # fitness = fitness(self.simulators_list[sim_num])
            # Select the best parents in the population
            # parents = self.select_mating_pool(new_population, fitness, number_of_parents_mating)


if __name__ == '__main__':
    # Initiate the evolutionary algorithm
    evolutionary_algorithm = EvolutionaryAlgorithm(number_of_generations=10, robots_per_generation=2, exploration_steps=10)
    evolutionary_algorithm.evolve()
