from enum import Enum


class Crossover(Enum):
    SINGLE_POINT = 'single point'
    TWO_POINT = 'two point'
    THREE_POINT = 'three point'
    HOMOGENEOUS = 'homogeneous'


class Selection(Enum):
    BEST = 'best'
    ROULETTE_WHEEL = 'roulette wheel'
    TOURNAMENT = 'tournament'


class Mutation(Enum):
    BOUNDARY = 'boundary'
    SINGLE_POINT = 'single point'
    TWO_POINT = 'two point'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):
    def __init__(self):
        # chromosome config
        self.left_interval_endpoint = None
        self.right_interval_endpoint = None
        self.chromosome_precision = None
        # population config
        self.population_size = None
        # algorithm config
        self.epoch_number = None
        self.crossover = None
        self.crossover_probability = None
        self.selection = None
        self.percent_of_selected = None
        self.mutation = None
        self.mutation_probability = None
        self.with_inversion = None
        self.inversion_probability = None
        self.with_elite_strategy = None
        self.percent_of_elite = None

    def with_crossover(self, crossover: Crossover, probability: float):
        self.crossover = crossover
        self.crossover_probability = probability
        return self

    def with_selection(self, selection: Selection, percent: int):
        self.selection = selection
        self.percent_of_selected = percent
        return self

    def with_mutation(self, mutation: Mutation, probability: float):
        self.mutation = mutation
        self.mutation_probability = probability
        return self

    def with_inversion(self, with_inversion: bool, probability: float):
        self.with_inversion = with_inversion
        self.inversion_probability = probability
        return self

    def with_elite_strategy(self, with_elite_strategy: bool, percent: int):
        self.with_elite_strategy = with_elite_strategy
        self.percent_of_elite = percent
        return self
