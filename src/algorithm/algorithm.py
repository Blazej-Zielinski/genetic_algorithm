from src.algorithm.conf import Config
from src.models.population import Population


class Algorithm:

    def __init__(self, config: Config):
        self.config: Config = config

    def start(self):
        population = Population(self.config.interval, self.config.chromosome_precision, self.config.population_size)

        # Pętla
            # Wybór elity

            # Selekcja

            # Crossover

            # Mutacja

            # Inversja

        pass
