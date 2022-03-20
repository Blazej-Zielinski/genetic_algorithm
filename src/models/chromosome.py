import numpy as np
import math


class Chromosome:
    def __init__(self, interval, precision):
        self.interval = interval
        self.precision = precision
        self.binary_arr = np.random.randint(2, size=(self.__calculate_length(),))

    def __calculate_length(self):
        return math.ceil(math.log2((self.interval[1] - self.interval[0]) * math.pow(10, self.precision)) + math.log2(1))

    def calculate_decimal(self):
        binary_string = ''.join([str(elem) for elem in self.binary_arr])
        return self.interval[0] + int(binary_string, 2) * (self.interval[1] - self.interval[0]) / (
                    math.pow(2, self.binary_arr.size) - 1)
