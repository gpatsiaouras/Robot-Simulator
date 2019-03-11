import numpy as np
import rooms
from main import Simulator

# Fitness Formula Parameters
COLLISION_PENALTY = -0.5
COLLISION_WEIGHT = 0.7
DUST_MULTIPLIER = 100
DUST_WEIGHT = 0.3

# Evolutionary Algorithm
NUMBER_OF_PARENTS_MATING = 2


class EvolutionaryAlgorithm:
    def __init__(self, number_of_generations, robots_per_generation, exploration_steps):
        # Input Parameters
        self.number_of_generations = number_of_generations
        self.robots_per_generation = robots_per_generation
        self.exploration_steps = exploration_steps

        # Fixed Parameters of the ANN
        self.number_of_nodes_input_layer = 12
        self.number_of_nodes_hidden_layer = 5
        self.number_of_nodes_output_layer = 2

        # Calculating the number of genes based on the layers of the RNN used to calculate the motion
        self.number_of_genes = self.number_of_nodes_input_layer * self.number_of_nodes_hidden_layer \
                               + self.number_of_nodes_hidden_layer * self.number_of_nodes_output_layer

        # Specify population size
        self.population_size = (self.robots_per_generation, self.number_of_genes)

    def weights_to_vector(self, weights1, weights2):
        return np.append(weights1.flatten(), weights2.flatten())

    def vector_to_weights(self, vector):
        weights_combined = np.split(vector, [
            self.number_of_genes - self.number_of_nodes_hidden_layer * self.number_of_nodes_output_layer,
            self.number_of_genes])
        return weights_combined[0], weights_combined[1]

    def fitness(self, simulators):
        fitness = []
        for simulator in simulators:
            dust_coverage = simulator.env.dust_coverage
            collisions = simulator.robot.collisions

            fitness_formula = (DUST_WEIGHT * dust_coverage * DUST_MULTIPLIER
                               + COLLISION_WEIGHT * collisions * COLLISION_PENALTY) / (DUST_WEIGHT + COLLISION_WEIGHT)
            fitness.append(fitness_formula)

        return fitness

    def select_mating_pool(self, population, fitness, number_of_parents_mating):
        parents = np.empty((number_of_parents_mating, population.shape[1]))

        for parent_number in range(number_of_parents_mating):
            index_of_max_fitness = np.where(fitness == np.max(fitness))
            index_of_max_fitness = index_of_max_fitness[0][0]
            parents[parent_number, :] = population[index_of_max_fitness, :]
            fitness[index_of_max_fitness] = -99999999999

        return parents

    def crossover(self, parents, offspring_shape):
        offspring = np.empty(offspring_shape)
        # We specify the crossover point to be at the center
        crossover_point = np.uint8(offspring_shape[1] / 2)

        for i in range(offspring_shape[0]):
            # Index of the first parent
            parent1_index = i % parents.shape[0]
            # Index of the second parent
            parent2_index = (i + 1) % parents.shape[0]
            # First half from parent 1
            offspring[i, 0:crossover_point] = parents[parent1_index, 0:crossover_point]
            # Second half from parent 2
            offspring[i, crossover_point:] = parents[parent2_index, crossover_point:]

        return offspring

    def mutation(self, crossover):
        # Mutation changes a single gene in each offspring randomly.
        for index in range(crossover.shape[0]):
            # Generate a random value to add to the gene
            random_value = np.random.uniform(0.0, 1.0, 1)
            crossover[index, 4] = crossover[index, 4] + random_value

        return crossover

    def evolve(self):
        population = np.random.uniform(low=0.0, high=5.0, size=self.population_size)

        for generation in range(self.number_of_generations):
            print("Generation {0}#".format(generation))

            simulators = []
            for i in range(self.robots_per_generation):
                sim = Simulator(rooms.room_1, self.exploration_steps)
                simulators.append(sim)
                # TODO Instruct the simulator to run in "Headless" mode by
                # giving him the weights for the ann in order to move the robot
                # for the time of the simulation
                sim.run()

            # Take the fitness of each chromosome in the population
            fitness = self.fitness(simulators)

            # Select the best parents in the population
            parents = self.select_mating_pool(population, fitness, NUMBER_OF_PARENTS_MATING)

            # Generate the next generation using crossover
            offspring_shape = (self.population_size[0] - parents.shape[0], self.number_of_genes)
            crossover = self.crossover(parents, offspring_shape)

            # Add some variations to the crossover using mutation
            mutation = self.mutation(crossover)

            population[0:parents.shape[0], :] = parents
            population[parents.shape[0]:, :] = mutation

        self.printBestResult(fitness, population)

    def printBestResult(self, fitness, population):
        # TODO Implement for clarity
        pass


if __name__ == '__main__':
    # Initiate the evolutionary algorithm
    evolutionary_algorithm = EvolutionaryAlgorithm(number_of_generations=1, robots_per_generation=4,
                                                   exploration_steps=100)
    evolutionary_algorithm.evolve()
