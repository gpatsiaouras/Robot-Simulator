import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class EvolutionaryAlgorithmPlotter:
    def __init__(self, evolutionary_algorithm):
        self.data_frame = pd.DataFrame(
            {
                'x': np.arange(0, evolutionary_algorithm.number_of_generations, 1),
                'fitness_avg': evolutionary_algorithm.fitness_average,
                'fitness_max': evolutionary_algorithm.fitness_maximum,
                'diversity': evolutionary_algorithm.diversity,
            }
        )

    def plot(self):
        plt.plot('x', 'fitness_avg', data=self.data_frame, marker='o', color='skyblue', linewidth=2,
                 label="Fitness Average")
        plt.plot('x', 'fitness_max', data=self.data_frame, marker='v', color='olive', linewidth=2,
                 label="Fitness Maximum")
        plt.plot('x', 'diversity', data=self.data_frame, marker='^', color='red', linewidth=2,
                 label="Diversity")
        plt.legend()
        plt.show()
