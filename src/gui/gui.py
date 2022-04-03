import pprint
import tkinter as tk
from src.algorithm.conf import Crossover, Mutation, Selection, Variables, Config, GenAlgorithms, default_values, OptimizationType
from src.algorithm.algorithm import Algorithm


class GeneticAlgorithmInterface(tk.Frame):
    def __init__(self, main):
        super().__init__(main)
        self.__main_window = main
        self.configure_main_window()

    def configure_main_window(self):
        self.__main_window.geometry('600x400')
        self.__main_window.resizable(False, False)
        self.__main_window.title("Genetic Algorithm")

        variables = dict()

        # Dropbox inputs
        gen_alg_enum = [e.value for e in GenAlgorithms]
        optimization_enum = [e.value for e in OptimizationType]
        selection_enum = [e.value for e in Selection]
        cross_enum = [e.value for e in Crossover]
        mutation_enum = [e.value for e in Mutation]

        dropdown_variables = [optimization_enum, selection_enum, mutation_enum, cross_enum]

        for idx, enum in enumerate(dropdown_variables):
            frame = tk.Frame(self.__main_window)
            tk.Label(frame, text=gen_alg_enum[idx]).grid(row=0, column=0)
            var = tk.StringVar()
            var.set(enum[0])
            dialog = tk.OptionMenu(frame, var, *enum)
            dialog.grid(row=0, column=1)
            frame.pack()
            variables[gen_alg_enum[idx]] = var

        # Entry inputs
        variables_labels = [e.value for e in Variables]
        for idx, label in enumerate(variables_labels):
            fr = tk.Frame(self.__main_window)
            var = tk.StringVar(value=default_values[idx])
            tk.Label(fr, text=label).grid(row=idx, column=0)
            tk.Entry(fr, textvariable=var).grid(row=idx, column=1)
            fr.pack()
            variables[label] = var

        # Button
        tk.Button(self.__main_window, command=lambda: configure_and_start_algorithm(variables), text="Start").pack()


def configure_and_start_algorithm(variables):
    try:
        config = Config().with_optimization(variables[GenAlgorithms.OPTIMIZATION.value])\
            .with_epoch_amount(variables[Variables.EPOCH_AMOUNT.value])\
            .with_population_size(variables[Variables.POPULATION_SIZE.value])\
            .with_inversion(variables[Variables.INVERSION_PROBABILITY.value])\
            .with_elite_strategy(variables[Variables.PERCENTAGE_ELITE.value])\
            .with_interval(variables[Variables.LEFT_INTERVAL_ENDPOINT.value], variables[Variables.RIGHT_INTERVAL_ENDPOINT.value]) \
            .with_crossover(variables[GenAlgorithms.CROSSOVER.value], variables[Variables.CROSS_PROBABILITY.value])\
            .with_mutation(variables[GenAlgorithms.MUTATION.value], variables[Variables.MUTATION_PROBABILITY.value])\
            .with_selection(variables[GenAlgorithms.SELECTION.value], variables[Variables.SELECTION_PERCENTAGE.value])\
            .with_chromosome_prec(variables[Variables.CHROMOSOME_PRECISION.value])
    except:
        print("Bad config")
        return

    Algorithm(config).start()
