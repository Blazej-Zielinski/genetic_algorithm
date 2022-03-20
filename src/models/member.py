from src.models.chromosome import Chromosome
import math


class Member:
    def __init__(self, chromosomes):
        self.x1: Chromosome = chromosomes[0]
        self.x2: Chromosome = chromosomes[1]

    def calculate_fitness_fun(self):
        x1_val = self.x1.calculate_decimal()
        x2_val = self.x2.calculate_decimal()

        return math.pow(x1_val + 2 * x2_val - 7, 2) + math.pow(2 * x1_val + x2_val - 5, 2)