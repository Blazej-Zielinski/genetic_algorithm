import os
import random
import time
import tkinter as tk
import tkinter.messagebox
import csv
import sys
import copy
import matplotlib.pyplot as plt
from functools import cmp_to_key
from statistics import mean, stdev
from abc import ABC, abstractmethod
from src.algorithm.conf import Config, BinaryCrossover, RealCrossover, Selection, BinaryMutation, RealMutation, OptimizationType
from src.models.population import PopulationBinary, PopulationReal
from src.utils.utils import compare_members


class Algorithm:

    def __init__(self, config: Config):
        self.config: Config = config
        self.epoch_best_members = []  # Best member in each epoch
        self.epoch_average = []  # Best member in each epoch
        self.epoch_standard_deviation = []  # Best member in each epoch

        # Output path
        folder = sys.argv[0][:-7] + f'output/{config.optimization}_S={config.selection}_C={config.crossover}_M={config.mutation}/'
        if not os.path.isdir(folder):
            os.mkdir(folder)

        self.output_file_path = folder + 'output.csv'
        self.plot_path_fv = folder + 'fitness_value.png'
        self.plot_path_avg = folder + 'average.png'
        self.plot_path_stdev = folder + 'standard_deviation.png'

    def start(self):
        pass

    def write_to_file(self):
        header = ['Epoch', 'X1', 'X2', 'Fitness_value', 'Average', 'Standard_deviation']

        with open(self.output_file_path, 'w', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write the data
            for epoch in range(len(self.epoch_best_members)):
                writer.writerow([
                    epoch + 1,
                    self.epoch_best_members[epoch].chromosomes[0].calculate_value(),
                    self.epoch_best_members[epoch].chromosomes[1].calculate_value(),
                    self.epoch_best_members[epoch].fitness_value,
                    self.epoch_average[epoch],
                    self.epoch_standard_deviation[epoch]
                ])

    def create_plots(self):
        x = range(1, self.config.epoch_amount + 2)

        plt.xlabel('Epoch')
        plt.ylabel('Fitness value')
        plt.title("Chart of fitness value by epoch")

        plt.plot(x, [best_member.fitness_value for best_member in self.epoch_best_members])
        plt.savefig(self.plot_path_fv)
        plt.cla()

        plt.xlabel('Epoch')
        plt.ylabel('Average')
        plt.title("Chart of average by epoch")

        plt.plot(x, [avg for avg in self.epoch_average])
        plt.savefig(self.plot_path_avg)
        plt.cla()

        plt.xlabel('Epoch')
        plt.ylabel('Standard deviation')
        plt.title("Chart of standard deviation by epoch")

        plt.plot(x, [s_dev for s_dev in self.epoch_standard_deviation])
        plt.savefig(self.plot_path_stdev)
        plt.cla()
