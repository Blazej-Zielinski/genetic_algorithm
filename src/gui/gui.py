import tkinter as tk
from src.algorithm.conf import RealCrossover, BinaryCrossover, RealMutation, BinaryMutation, \
    Selection, BinaryVariables, RealVariables, Config, GenOperators, binary_default_values, real_default_values, \
    OptimizationType
from src.algorithm.algorithm import RealAlgorithm, BinaryAlgorithm
from src.models.chromosome import ChromosomeType


class GeneticAlgorithmInterface(tk.Frame):
    def __init__(self, main):
        super().__init__(main)
        self.__main_window = main
        self.__main_window.geometry('400x420')
        self.__main_window.resizable(False, False)
        self.__main_window.title("Genetic Algorithm")
        self.start()

    def clear_current_window(self):
        for obj in self.__main_window.winfo_children():
            obj.destroy()

    def start(self):
        self.clear_current_window()
        binary_button = tk.Button(self.__main_window, text="Binary representation",
                                  command=lambda: self.configure_main_window(ChromosomeType.BINARY))
        binary_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        real_button = tk.Button(self.__main_window, text="Real representation",
                                command=lambda: self.configure_main_window(ChromosomeType.REAL))
        real_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    def configure_main_window(self, chromosome_type):
        self.clear_current_window()

        variables = dict()

        # Dropbox inputs
        gen_alg_enum = [e.value for e in GenOperators]
        optimization_enum = [e.value for e in OptimizationType]
        selection_enum = [e.value for e in Selection]
        cross_enum = [e.value for e in (RealCrossover if chromosome_type == ChromosomeType.REAL else BinaryCrossover)]
        mutation_enum = [e.value for e in (RealMutation if chromosome_type == ChromosomeType.REAL else RealMutation)]

        dropdown_variables = [optimization_enum, selection_enum, mutation_enum, cross_enum]

        for idx, enum in enumerate(dropdown_variables):
            frame = tk.Frame(self.__main_window)
            tk.Label(frame, text=gen_alg_enum[idx]).pack(side=tk.LEFT, padx=(10, 0))
            var = tk.StringVar()
            var.set(enum[0])
            dialog = tk.OptionMenu(frame, var, *enum)
            dialog.config(width=15)
            dialog.pack(side=tk.RIGHT, padx=(0, 10))
            frame.pack(fill=tk.X)
            variables[gen_alg_enum[idx]] = var

        # Entry inputs
        variables_labels = [e.value for e in (RealVariables if chromosome_type == ChromosomeType.REAL else BinaryVariables)]
        for idx, label in enumerate(variables_labels):
            fr = tk.Frame(self.__main_window)
            var = tk.StringVar(value=real_default_values[idx] if chromosome_type == ChromosomeType.REAL else binary_default_values[idx])
            tk.Label(fr, text=label).pack(side=tk.LEFT, padx=(10, 0))
            tk.Entry(fr, textvariable=var).pack(side=tk.RIGHT, fill=tk.X, padx=(0, 10))
            fr.pack(fill=tk.X)
            variables[label] = var

        # Button
        button = tk.Button(self.__main_window, command=lambda: configure_and_start_algorithm(variables, chromosome_type), text="Start")
        button.config(width=40)
        button.pack(pady=(10, 0))

        button = tk.Button(self.__main_window, command=self.start, text="Back to menu")
        button.config(width=40)
        button.pack(pady=(10, 0))


def configure_and_start_algorithm(variables, chromosome_type):
    # try:
    config = Config().with_optimization(variables[GenOperators.OPTIMIZATION.value]) \
            .with_epoch_amount(variables[BinaryVariables.EPOCH_AMOUNT.value]) \
            .with_population_size(variables[BinaryVariables.POPULATION_SIZE.value]) \
            .with_elite_strategy(variables[BinaryVariables.PERCENTAGE_ELITE.value]) \
            .with_interval(variables[BinaryVariables.LEFT_INTERVAL_ENDPOINT.value],
                           variables[BinaryVariables.RIGHT_INTERVAL_ENDPOINT.value]) \
            .with_crossover(variables[GenOperators.CROSSOVER.value],
                            variables[BinaryVariables.CROSS_PROBABILITY.value]) \
            .with_mutation(variables[GenOperators.MUTATION.value],
                           variables[BinaryVariables.MUTATION_PROBABILITY.value]) \
            .with_selection(variables[GenOperators.SELECTION.value],
                            variables[BinaryVariables.SELECTION_PERCENTAGE.value]) \
            .with_chromosome_type(chromosome_type)
    if ChromosomeType.BINARY == chromosome_type:
        config.with_inversion(variables[BinaryVariables.INVERSION_PROBABILITY.value]) \
            .with_chromosome_prec(variables[BinaryVariables.CHROMOSOME_PRECISION.value])
    else:
        config.with_alpha(variables[RealVariables.ALPHA.value]) \
            .with_beta(variables[RealVariables.BETA.value])
    # except:
    #     print("Bad config")
    #     return

    RealAlgorithm(config).start() if ChromosomeType.REAL == chromosome_type else BinaryAlgorithm(config).start()
