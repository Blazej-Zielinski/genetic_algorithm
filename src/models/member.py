import numpy as np
import math
from src.models.chromosome import create_chromosome


class Member:
    def __init__(self, interval, precision, chromosome_type):
        self.chromosome_type = chromosome_type
        self.chromosomes = np.array([create_chromosome(chromosome_type, interval, precision) for _ in range(2)])
        self.fitness_value = self.calculate_fitness_fun()

    def calculate_fitness_fun(self):
        x1_val = self.chromosomes[0].calculate_value()
        x2_val = self.chromosomes[1].calculate_value()

        return math.pow(x1_val + 2 * x2_val - 7, 2) + math.pow(2 * x1_val + x2_val - 5, 2)

    def update_fitness_value(self):
        self.fitness_value = self.calculate_fitness_fun()

    def __str__(self):
        return f"[{''.join(str(chromosome.calculate_value()) + ' ; ' for chromosome in self.chromosomes)}{self.fitness_value}]"
