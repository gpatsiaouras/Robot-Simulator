import os
import random

import numpy as np
import rooms
from main import Simulator

# Fitness Formula Parameters
COLLISION_PENALTY = -0.5
COLLISION_WEIGHT = 0.3
GROUND_MULTIPLIER = 100
GROUND_WEIGHT = 0.7

# Evolutionary Algorithm
NUMBER_OF_PARENTS_MATING = 4


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

    def fitness(self, simulators):
        fitness = []
        for simulator in simulators:
            ground_coverage = simulator.env.ground_coverage
            collisions = simulator.robot.collisions

            fitness_formula = (GROUND_WEIGHT * ground_coverage * GROUND_MULTIPLIER
                               + COLLISION_WEIGHT * collisions * COLLISION_PENALTY) / (GROUND_WEIGHT + COLLISION_WEIGHT)
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
            random_value = np.random.uniform(-5.0, 5.0, 1)
            crossover[index, 4] = crossover[index, 4] + random_value

        return crossover

    def evolve(self, start_population=None, start_gen=0):
        if start_population is None:
            population = np.random.uniform(low=-5.0, high=5.0, size=self.population_size)
        else:
            population = start_population

        for generation in range(start_gen, self.number_of_generations):
            print("Generation {0}#".format(generation))

            simulators = []
            for i in range(self.robots_per_generation):
                sim = Simulator(rooms.room_1, self.exploration_steps, autonomous=True)
                sim.network.weights1, sim.network.weights2 = self.vector_to_weights(population[i])

                simulators.append(sim)
                sim.run()

            # Take the fitness of each chromosome in the population
            fitness = self.fitness(simulators)
            print(fitness)
            # Select the best parents in the population
            parents = self.select_mating_pool(population, fitness, NUMBER_OF_PARENTS_MATING)

            # Generate the next generation using crossover
            offspring_shape = (self.population_size[0] - parents.shape[0], self.number_of_genes)
            crossover = self.crossover(parents, offspring_shape)

            # Add some variations to the crossover using mutation
            mutation = self.mutation(crossover)

            population[0:parents.shape[0], :] = parents
            population[parents.shape[0]:, :] = mutation

            if generation % self.save_each == 0:
                self.save_checkpoint(generation, "/src/ckpt/", population)

    def crossover2(self, robots_selected):
        # assuming this list is always even...

        # takes all parents in
        # should return children

        # random numbe between 0 and 1 * len list selected
        # move this into random list... (funtion for randomly sort a list)?
        # remove from that list

        robtos_random = []

        # if length list is not constant, create a new variable with original length list
        for i in range(0, robots_selected):  # does length stay constant, even if loop reducing...
            a = np.random  # rundom number 0 and 1
            index = a * robots_selected.length  # this is NEW length
            robots_random.append(robots_selected[i])  # check..
            del robots_selected[i]  # check #so that this robot is chosen only once

        offspring_list = []

        # now, select in pairs and apply misture
        for i in range(0, robots_random.length / 2):
            k = 2 * i
            offspring = mixture(robots_random(k), robots_random(k + 1))  ##Here is where they mix
            offspring_list.append(offspring)  # check

        return offspring_list

    def mixture2(parent1, parent2):  # way of crossing genes..

        weights_A1 = a.weights1
        weights_B1 = b.weights1

        weights_A2 = a.weights2
        weights_B2 = b.weights2

        weights_C1 = np.zeros  # create new instance robot?
        weights_C2 = np.zeros

        changed_matrix1 = np.zeros
        changed_matrix2 = np.zeros

        # also: choose randomly x spaces --> generate vector random positions
        vectorx1 = [random.randint(1, weights_C1[0].length) for _ in range(number_genes / 2)]  ##assume even?
        vectory1 = [random.randint(1, weights_C1.length) for _ in range(number_genes / 2)]

        vectorx2 = [random.randint(1, weights_C2[0].length) for _ in range(number_genes / 2)]  ##assume even?
        vectory2 = [random.randint(1, weights_C2.length) for _ in range(number_genes / 2)]

        # this might repeat some...

        for i in range(0, number_genes / 2):  # this range needs to corrected I beleive..
            a = vectorx1[i]
            b = vectory1[i]
            weights_C1[a][b] = weights_A1[a][b]
            changed_matrix1[a][b] = 1

        for i in range(0, changed_matrix1.length):
            for j in range(0, changed_matrix1.length):
                if changed_matrix1[i][j] == 0:  # has not been changed, mean this is for the other parent to fill in
                    weights_C1[i][j] = weights_B1[i][j]

        # weights2 ##NEEDS TO BE ADJUSTED
        for i in range(0, number_genes / 2):
            a = vectorx2[i]
            b = vectory2[i]
            weights_C2[a][b] = weights_A2[a][b]
            changed_matrix2[a][b] = 1

        for i in range(0, changed_matrix2.length):
            for j in range(0, changed_matrix2.length):
                if changed_matrix2[i][j] == 0:  # has not been changed, mean this is for the other parent to fill in
                    weights_C2[i][j] = weights_B2[i][j]

        return weight_C1, weights_C2

    def printBestResult(self, fitness, population):
        print(fitness)
        pass

    def save_checkpoint(self, generation, out_dir, population):

        curr_path = os.path.dirname(os.path.abspath(__file__))

        final_dir = curr_path + out_dir + str(generation)
        if not os.path.exists(os.path.join("ckpt")):
            os.makedirs("ckpt")
        # torch.save(state, os.path.join(final_dir, "{}_{}.ckpt".format(learner, episode)))
        ckpt = open("ckpt/gen_{}.txt".format(generation), "w+")
        population.tofile(ckpt)

    def evolve_checkpoint(self, ckpt_dir):
        curr_path = os.path.dirname(os.path.abspath(__file__))
        ckpt_dir = curr_path + ckpt_dir
        ckpt = open(ckpt_dir, "r")
        population = np.fromfile(ckpt)
        start_gen = int(ckpt_dir.split("_").pop()[:-4])
        self.evolve(population, start_gen)


if __name__ == '__main__':
    # Initiate the evolutionary algorithm
    evolutionary_algorithm = EvolutionaryAlgorithm(number_of_generations=15, robots_per_generation=6,
                                                   exploration_steps=20, save_each=2)
    evolutionary_algorithm.evolve()
    # evolutionary_algorithm.evolve_checkpoint("/ckpt/gen_8.txt")
