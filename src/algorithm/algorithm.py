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

from src.algorithm.conf import Config, Crossover, Selection, Mutation, OptimizationType
from src.models.population import Population
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
        # Start time execution
        start_time = time.time()

        population = Population(
            self.config.interval,
            self.config.chromosome_precision,
            self.config.population_size,
            self.config.optimization
        )

        # Loop
        for _ in range(self.config.epoch_amount):
            fitness_values = [member.fitness_value for member in population.members]

            self.epoch_best_members.append(copy.deepcopy(sorted(population.members, key=cmp_to_key(compare_members), reverse=OptimizationType.MAXIMIZATION.value == population.optimization)[0]))
            self.epoch_average.append(mean(fitness_values))
            self.epoch_standard_deviation.append(stdev(fitness_values))

            # Chosen elite members
            elite_members = population.elite_strategy(self.config.percent_of_elite)

            # Selection
            {
                Selection.BEST.value: lambda: population.best_selection(self.config.percent_of_selected),
                Selection.TOURNAMENT.value: lambda: population.tournament_selection(self.config.percent_of_selected),
                Selection.ROULETTE_WHEEL.value: lambda: population.roulette_wheel_selection(self.config.percent_of_selected)
            }[self.config.selection]()

            # Crossover
            children = []
            while len(population.members) + len(children) + len(elite_members) < population.size:
                parents = random.sample(population.members + elite_members, 2)
                children += {
                    Crossover.SINGLE_POINT.value: lambda: population.multipoint_crossover(parents[0], parents[1], self.config.crossover_probability, 1),
                    Crossover.TWO_POINT.value: lambda: population.multipoint_crossover(parents[0], parents[1], self.config.crossover_probability, 2),
                    Crossover.THREE_POINT.value: lambda: population.multipoint_crossover(parents[0], parents[1], self.config.crossover_probability, 3),
                    Crossover.HOMOGENEOUS.value: lambda: population.homogeneous_crossover(parents[0], parents[1], self.config.crossover_probability)
                }[self.config.crossover]()

            # Because we always add two children, sometimes there are too many members
            if len(population.members) + len(children) + len(elite_members) > population.size:
                children.pop()

            population.members += children

            # Mutation
            for i in range(len(population.members)):
                {
                    Mutation.SINGLE_POINT.value: lambda: population.multipoint_mutation(population.members[i], self.config.mutation_probability, 1),
                    Mutation.TWO_POINT.value: lambda: population.multipoint_mutation(population.members[i], self.config.mutation_probability, 2),
                    Mutation.BOUNDARY.value: lambda: population.boundary_mutation(population.members[i], self.config.mutation_probability)
                }[self.config.mutation]()

            # Inversion
            for i in range(len(population.members)):
                population.inversion(population.members[i], self.config.inversion_probability)

            # Adding elite member
            population.members += elite_members

        fitness_values = [member.fitness_value for member in population.members]

        self.epoch_best_members.append(copy.deepcopy(sorted(population.members, key=cmp_to_key(compare_members), reverse=OptimizationType.MAXIMIZATION.value == population.optimization)[0]))
        self.epoch_average.append(mean(fitness_values))
        self.epoch_standard_deviation.append(stdev(fitness_values))

        # Calculating execution time
        execution_time = round(time.time() - start_time, 2)

        # Writing program solution tu file
        self.write_to_file()

        # Creating plots
        self.create_plots()

        solution = self.epoch_best_members[-1]
        tk.messagebox.showinfo("Solution found",
                               f"Solution found in {execution_time} seconds.\n"
                               f"f({round(solution.chromosomes[0].calculate_decimal(), 10)}, "
                               f"{round(solution.chromosomes[1].calculate_decimal(), 10)}) = "
                               f"{round(solution.fitness_value, 10)}")

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
                    self.epoch_best_members[epoch].chromosomes[0].calculate_decimal(),
                    self.epoch_best_members[epoch].chromosomes[1].calculate_decimal(),
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
