import pprint
import tkinter as tk
from src.algorithm.conf import Crossover, Mutation, Selection, Variables, Config, GenAlgorithms, default_values
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

        # Dropbox
        selection_enum = [e.value for e in Selection]
        cross_enum = [e.value for e in Crossover]
        mutation_enum = [e.value for e in Mutation]

        selection_frame = tk.Frame(self.__main_window)
        tk.Label(selection_frame, text=GenAlgorithms.SELECTION.value).grid(row=0, column=0)
        selection_var = tk.StringVar()
        selection_var.set(selection_enum[0])
        selection_dialog = tk.OptionMenu(selection_frame, selection_var, *selection_enum)
        selection_dialog.grid(row=0, column=1)
        selection_frame.pack()
        variables[GenAlgorithms.SELECTION.value] = selection_var

        cross_frame = tk.Frame(self.__main_window)
        tk.Label(cross_frame, text=GenAlgorithms.CROSSOVER.value).grid(row=0, column=0)
        cross_var = tk.StringVar()
        cross_var.set(cross_enum[0])
        cross_dialog = tk.OptionMenu(cross_frame, cross_var, *cross_enum)
        cross_dialog.grid(row=0, column=1)
        cross_frame.pack()
        variables[GenAlgorithms.CROSSOVER.value] = cross_var

        mutation_frame = tk.Frame(self.__main_window)
        tk.Label(mutation_frame, text=GenAlgorithms.MUTATION.value).grid(row=0, column=0)
        mutation_var = tk.StringVar()
        mutation_var.set(mutation_enum[0])
        mutation_dialog = tk.OptionMenu(mutation_frame, mutation_var, *mutation_enum)
        mutation_dialog.grid(row=0, column=1)
        mutation_frame.pack()
        variables[GenAlgorithms.MUTATION.value] = mutation_var

        # Inputs
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
        config = Config().with_epoch_amount(variables[Variables.EPOCH_AMOUNT.value])\
            .with_population_size(variables[Variables.POPULATION_SIZE.value])\
            .with_inversion(variables[Variables.INVERSION_PROBABILITY.value])\
            .with_elite_strategy(variables[Variables.PERCENTAGE_ELITE.value])\
            .with_interval(variables[Variables.LEFT_INTERVAL_ENDPOINT.value], variables[Variables.RIGHT_INTERVAL_ENDPOINT.value]) \
            .with_crossover(variables[GenAlgorithms.CROSSOVER.value], variables[Variables.CROSS_PROBABILITY.value])\
            .with_mutation(variables[GenAlgorithms.MUTATION.value], variables[Variables.MUTATION_PROBABILITY.value])\
            .with_selection(variables[GenAlgorithms.SELECTION.value], variables[Variables.SELECTION_PROBABILITY.value])\
            .with_chromosome_prec(variables[Variables.CHROMOSOME_PRECISION.value])
    except:
        print("Bad config")
        return

    Algorithm(config).start()
