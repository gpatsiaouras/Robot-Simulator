import os
import numpy as np
import rooms
import time
from main import Simulator
from ea_plotter import EvolutionaryAlgorithmPlotter

from scipy.spatial import distance

# Fitness Formula Parameters
COLLISION_PENALTY = -0.5
COLLISION_WEIGHT = 0.3
GROUND_MULTIPLIER = 100
GROUND_WEIGHT = 0.7

# Evolutionary Algorithm
NUMBER_OF_PARENTS_MATING = 4

np.set_printoptions(precision=2)


def calculate_distance(list_vectors):
    tot_distance = 0  # just adding all together
    count_i = 0
    for i in list_vectors:
        count_i += 1
        count_j = 0
        for j in list_vectors:
            count_j += 1
            if count_i == count_j:  # sole purpose of this counts is not calculate norms with same vector (probably irrelevant..)
                pass
            else:
                dist1 = distance.euclidean(i, j)  # scipy library
                tot_distance += dist1
    tot_distance = tot_distance / (len(list_vectors) ** 2)
    return tot_distance


def run_chromosome_on_simulator(weights1, weights2, steps=-1):
    # Demonstrate on the simulator
    sim = Simulator(rooms.room_1, max_steps=steps, autonomous=True, pygame_enabled=True)
    sim.network.weights1 = weights1
    sim.network.weights2 = weights2
    sim.run()


class EvolutionaryAlgorithm:
    def __init__(self, number_of_generations, robots_per_generation, exploration_steps, save_each=None):
        # Input Parameters
        self.number_of_generations = number_of_generations
        self.robots_per_generation = robots_per_generation
        self.exploration_steps = exploration_steps
        self.save_each = save_each
        # Fixed Parameters of the ANN
        self.number_of_nodes_input_layer = 17
        self.number_of_nodes_hidden_layer = 5
        self.number_of_nodes_output_layer = 2

        # Statistical data
        self.fitness_average = []
        self.fitness_maximum = []
        self.diversity = []

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
        return weights_combined[0].reshape(self.number_of_nodes_input_layer, self.number_of_nodes_hidden_layer), \
               weights_combined[1].reshape(self.number_of_nodes_hidden_layer, self.number_of_nodes_output_layer)

    def fitness(self, simulator):
        ground_coverage = simulator.env.ground_coverage
        collisions = simulator.robot.collisions

        fitness = (GROUND_WEIGHT * ground_coverage * GROUND_MULTIPLIER
                           + COLLISION_WEIGHT * collisions * COLLISION_PENALTY) / (GROUND_WEIGHT + COLLISION_WEIGHT)

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
            random_value = np.random.uniform(-5.0, 5.0, 1)
            crossover[index, 4] = crossover[index, 4] + random_value

        return crossover

    def evolve(self, start_population=None, start_gen=0):
        if start_population is None:
            population = np.random.uniform(low=-5.0, high=5.0, size=self.population_size)
        else:
            population = start_population

        simulator = Simulator(rooms.room_1, self.exploration_steps, autonomous=True, pygame_enabled=False)
        for generation in range(start_gen, self.number_of_generations):
            start = time.time()
            print("\nGeneration {0}#".format(generation))
            print("Robot running: ", end="", flush=True)
            fitness = []
            for i in range(self.robots_per_generation):
                simulator.reset()
                simulator.network.weights1, simulator.network.weights2 = self.vector_to_weights(population[i])
                print(i, end=" ", flush=True)
                simulator.run()
                fitness.append(self.fitness(simulator))

            self.diversity.append(calculate_distance(population))

            self.fitness_average.append(np.average(fitness))
            self.fitness_maximum.append(np.max(fitness))
            print("\nFitness: " + str(fitness))

            # Select the best parents in the population
            parents = self.select_mating_pool(population, fitness, NUMBER_OF_PARENTS_MATING)

            # Generate the next generation using crossover
            offspring_shape = (self.population_size[0] - parents.shape[0], self.number_of_genes)
            crossover = self.crossover(parents, offspring_shape)

            # Add some variations to the crossover using mutation
            mutation = self.mutation(crossover)

            population[0:parents.shape[0], :] = parents
            population[parents.shape[0]:, :] = mutation

            # Save checkpoint according to frequency requested
            if generation % self.save_each == 0:
                self.save_checkpoint(generation, population)

            print("Time elapsed: {0}".format(time.time() - start))

            # If this is the last generation
            if generation == self.number_of_generations - 1:
                best_chromosome_index = np.where(fitness == np.max(fitness))

                # Retrieve the weights from the chromosome
                weights1, weights2 = self.vector_to_weights(population[best_chromosome_index].T)

                # Print the best weights
                print("\nBest Weights:")
                print(weights1)
                print(weights2)

                return weights1, weights2

    def save_checkpoint(self, generation, population):
        if not os.path.exists(os.path.join("ckpt")):
            os.makedirs("ckpt")
        ckpt = open("ckpt/gen_{}.txt".format(generation), "w+")
        population.tofile(ckpt)

    def evolve_checkpoint(self, ckpt_dir):
        curr_path = os.path.dirname(os.path.abspath(__file__))
        ckpt_dir = curr_path + ckpt_dir
        ckpt = open(ckpt_dir, "r")
        population = np.fromfile(ckpt, dtype=np.float64)
        start_gen = int(ckpt_dir.split("_").pop()[:-4])
        return self.evolve(population.reshape(self.robots_per_generation, self.number_of_genes), start_gen)


if __name__ == '__main__':
    # Initiate the evolutionary algorithm with parameters
    evolutionary_algorithm = EvolutionaryAlgorithm(
        number_of_generations=30,
        robots_per_generation=10,
        exploration_steps=1000,
        save_each=2
    )

    weights1, weights2 = evolutionary_algorithm.evolve()
    # weights1, weights2 = evolutionary_algorithm.evolve_checkpoint("/ckpt/gen_70.txt")

    # Plot Data
    plotter = EvolutionaryAlgorithmPlotter(evolutionary_algorithm)
    plotter.plot()

    # Demonstrate on the simulator by replicating the best individual weights
    run_chromosome_on_simulator(weights1, weights2)
