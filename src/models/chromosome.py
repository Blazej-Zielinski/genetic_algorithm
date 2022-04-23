import numpy as np
import random
import math
from abc import ABC, abstractmethod
from enum import Enum


class ChromosomeType(Enum):
    BINARY = 'binary chromosome'
    REAL = 'real chromosome'


class Chromosome(ABC):

    @abstractmethod
    def calculate_value(self):
        pass


class BinaryChromosome(Chromosome):
    def __init__(self, interval, precision):
        self.interval = interval
        self.precision = precision
        self.binary_arr = np.random.randint(2, size=(self.__calculate_length(),))

    def __calculate_length(self):
        return math.ceil(math.log2((self.interval[1] - self.interval[0]) * math.pow(10, self.precision)) + math.log2(1))

    def calculate_value(self):
        binary_string = ''.join([str(elem) for elem in self.binary_arr])
        return self.interval[0] + int(binary_string, 2) * (self.interval[1] - self.interval[0]) / (
                    math.pow(2, self.binary_arr.size) - 1)


class RealChromosome(Chromosome):
    def __init__(self, interval):
        self.interval = interval
        self.value = random.uniform(self.interval[0], self.interval[1])

    def calculate_value(self):
        return self.value

    def is_value_in_interval(self):
        return self.interval[0] <= self.value <= self.interval[1]


def create_chromosome(chromosome_type: ChromosomeType, interval, precision=6):
    if ChromosomeType.BINARY == chromosome_type:
        return BinaryChromosome(interval, precision)
    elif ChromosomeType.REAL == chromosome_type:
        return RealChromosome(interval)
