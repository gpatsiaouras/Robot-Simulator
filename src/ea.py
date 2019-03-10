import numpy as np


class EvolutionaryAlgorithm:
    def __init__(self, number_of_generations, robots_per_generation):
        # Input Parameters
        self.number_of_generations = number_of_generations
        self.robots_per_generation = robots_per_generation

        # Fixed Parameters
        self.number_of_parents_mating = 4
        self.number_of_weights = 12

        # Specify population
        self.population_size = (self.robots_per_generation, self.number_of_weights)

        # Initiate environments and robots
        # TODO Initiate the lists to use below
        for i in range(self.robots_per_generation):
            # TODO create a new environment and robot for the generations and put the objects in a list
            pass

    def fitness(self):
        # TODO Fill in this method
        return 0

    def select_mating_pool(self):
        return 0

    def crossover(self):
        pass

    def mutation(self):
        pass

    def evolve(self):
        new_population = np.random.uniform(low=0.0, high=1.0, size=self.population_size)

        for generation in range(self.number_of_generations):
            for i in range(self.robots_per_generation):
                # TODO Fixed steps of movement for each robot
                # Take the fitness of each chromesome in the population
                fitness = fitness()
                # Select the best parents in the population
                parents = self.select_mating_pool(new_population, fitness, number_of_parents_mating)


if __name__ == '__main__':
    # Initiate the evolutionary algorithm
    evolutionary_algorithm = EvolutionaryAlgorithm(number_of_generations=10, robots_per_generation=10)
