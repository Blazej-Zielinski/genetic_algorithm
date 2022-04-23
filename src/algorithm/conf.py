from enum import Enum

binary_default_values = [60, 0.5, 0.02, 0, 10, -10, 10, 6, 100, 1000]
real_default_values = [60, 0.5, 0.02, 10, 0, 0, -10, 10, 100, 1000]


class OptimizationType(Enum):
    MAXIMIZATION = 'maximization'
    MINIMIZATION = 'minimization'


class BinaryCrossover(Enum):
    SINGLE_POINT = 'single-point'
    TWO_POINT = 'two-point'
    THREE_POINT = 'three-point'
    HOMOGENEOUS = 'homogeneous'


class RealCrossover(Enum):
    ARITHMETIC = 'arithmetic'
    BLEND_ALPHA = 'blend-alpha'
    BLEND_ALPHA_BETA = 'blend-alpha-beta'
    AVERAGE = 'average'
    LINEAR = 'linear'


class Selection(Enum):
    BEST = 'best'
    ROULETTE_WHEEL = 'roulette-wheel'
    TOURNAMENT = 'tournament'


class BinaryMutation(Enum):
    BOUNDARY = 'boundary'
    SINGLE_POINT = 'single-point'
    TWO_POINT = 'two-point'


class RealMutation(Enum):
    UNIFORM = 'uniform'
    GAUSS = 'Gauss'


class BinaryVariables(Enum):
    SELECTION_PERCENTAGE = 'selection percentage / tournament size:'
    CROSS_PROBABILITY = 'cross prob:'
    MUTATION_PROBABILITY = 'mutation prob:'
    INVERSION_PROBABILITY = 'inversion prob:'
    PERCENTAGE_ELITE = 'percentage elite:'

    LEFT_INTERVAL_ENDPOINT = 'left interval endpoint:'
    RIGHT_INTERVAL_ENDPOINT = 'right interval endpoint:'
    CHROMOSOME_PRECISION = 'chromosome precision:'
    POPULATION_SIZE = 'population size:'
    EPOCH_AMOUNT = 'epoch amount:'


class RealVariables(Enum):
    SELECTION_PERCENTAGE = 'selection percentage / tournament size:'
    CROSS_PROBABILITY = 'cross prob:'
    MUTATION_PROBABILITY = 'mutation prob:'
    PERCENTAGE_ELITE = 'percentage elite:'
    ALPHA = 'alpha:'
    BETA = 'beta:'

    LEFT_INTERVAL_ENDPOINT = 'left interval endpoint:'
    RIGHT_INTERVAL_ENDPOINT = 'right interval endpoint:'
    POPULATION_SIZE = 'population size:'
    EPOCH_AMOUNT = 'epoch amount:'


class GenOperators(Enum):
    OPTIMIZATION = 'optimization'
    SELECTION = 'selection'
    MUTATION = 'mutation'
    CROSSOVER = 'crossover'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):
    def __init__(self):
        # optimization
        self.optimization = None
        # chromosome config
        self.interval = None
        self.chromosome_type = None
        # population config
        self.population_size = None
        # algorithm config
        self.epoch_amount = None
        self.crossover = None
        self.crossover_probability = None
        self.selection = None
        self.percent_of_selected = None
        self.mutation = None
        self.mutation_probability = None
        self.percent_of_elite = None
        # real representation
        self.alpha = None
        self.beta = None
        # binary representation
        self.chromosome_precision = None
        self.inversion_probability = None

    def with_optimization(self, optimization):
        self.optimization = optimization.get()
        return self

    def with_crossover(self, crossover, probability):
        self.crossover = crossover.get()
        self.crossover_probability = float(probability.get())
        return self

    def with_selection(self, selection, percent):
        self.selection = selection.get()
        self.percent_of_selected = int(percent.get())
        return self

    def with_mutation(self, mutation, probability):
        self.mutation = mutation.get()
        self.mutation_probability = float(probability.get())
        return self

    def with_inversion(self, probability):
        self.inversion_probability = float(probability.get())
        return self

    def with_elite_strategy(self, percent):
        self.percent_of_elite = int(percent.get())
        return self

    def with_interval(self, left_interval_endpoint, right_interval_endpoint):
        self.interval = [float(left_interval_endpoint.get()), float(right_interval_endpoint.get())]
        return self

    def with_chromosome_prec(self, chromosome_prec):
        self.chromosome_precision = int(chromosome_prec.get())
        return self

    def with_chromosome_type(self, chromosome_type):
        self.chromosome_type = chromosome_type
        return self

    def with_population_size(self, population_size):
        self.population_size = int(population_size.get())
        return self

    def with_epoch_amount(self, epoch_amount):
        self.epoch_amount = int(epoch_amount.get())
        return self

    def with_alpha(self, alpha):
        self.alpha = float(alpha.get())
        return self

    def with_beta(self, beta):
        self.beta = float(beta.get())
        return self

