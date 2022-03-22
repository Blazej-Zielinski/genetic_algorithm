from src.models.chromosome import Chromosome
import math


class Member:
    def __init__(self, interval, precision):
        # Todo array of chromosomes to avoid code duplication
        self.x1: Chromosome = Chromosome(interval, precision)
        self.x2: Chromosome = Chromosome(interval, precision)
        self.fitness_value = self.calculate_fitness_fun()

    def calculate_fitness_fun(self):
        x1_val = self.x1.calculate_decimal()
        x2_val = self.x2.calculate_decimal()

        return math.pow(x1_val + 2 * x2_val - 7, 2) + math.pow(2 * x1_val + x2_val - 5, 2)

    def update_fitness_value(self):
        self.fitness_value = self.calculate_fitness_fun()

    def __str__(self):
        return f"[{self.x1.calculate_decimal()} ; {self.x2.calculate_decimal()} ; {self.fitness_value}]"
