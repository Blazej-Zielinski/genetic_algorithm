import pprint
import random

from src.algorithm.conf import Config, Crossover, Selection, Mutation
from src.models.population import Population


class Algorithm:

    def __init__(self, config: Config):
        self.config: Config = config

    def start(self):
        # pprint.pprint(vars(self.config))

        population = Population(self.config.interval, self.config.chromosome_precision, self.config.population_size)

        # Loop
        for epoch in range(self.config.epoch_amount):
            # Chosen elite members
            elite_members = population.elite_strategy(self.config.percent_of_elite)
            print(f"Best member: {elite_members[0]}, Epoch: {epoch}")

            # Selection
            {
                Selection.BEST.value: lambda: population.best_selection(self.config.percent_of_selected),
                Selection.TOURNAMENT.value: lambda: population.tournament_selection(self.config.percent_of_selected),
                Selection.ROULETTE_WHEEL.value: lambda: population.roulette_wheel_selection(self.config.percent_of_selected)
            }[self.config.selection]()
            print(f"After Selection: {len(population.members)}")

            # Crossover
            children = []
            while len(population.members) + len(children) + len(elite_members) <= population.size:
                parents = random.sample(population.members, 2)
                children += {
                    Crossover.SINGLE_POINT.value: lambda: population.multipoint_crossover(parents[0], parents[1], 1),
                    Crossover.TWO_POINT.value: lambda: population.multipoint_crossover(parents[0], parents[1], 2),
                    Crossover.THREE_POINT.value: lambda: population.multipoint_crossover(parents[0], parents[1], 3),
                    Crossover.HOMOGENEOUS.value: lambda: population.homogeneous_crossover(parents[0], parents[1], self.config.crossover_probability)
                }[self.config.crossover]()

            # Because we always add two children, sometimes there are too many members
            if len(population.members) + len(children) + len(elite_members) > population.size:
                children.pop()

            population.members += children
            print(f"After Crossover: {len(population.members)}")

            # Mutation
            #todo mutujemy wszystkich ???
            for i in range(len(population.members)):
                {
                    Mutation.SINGLE_POINT.value: lambda: population.multipoint_mutation(population.members[i], self.config.mutation_probability, 1),
                    Mutation.TWO_POINT.value: lambda: population.multipoint_mutation(population.members[i], self.config.mutation_probability, 2),
                    Mutation.BOUNDARY.value: lambda: population.boundary_mutation(population.members[i], self.config.mutation_probability)
                }[self.config.mutation]()
            print(f"After Mutation: {len(population.members)}")

            # Inversion
            for i in range(len(population.members)):
                population.inversion(population.members[i], self.config.inversion_probability)
            print(f"After Inversion: {len(population.members)}")

            # Adding elite member
            population.members += elite_members
            print(f"After adding elite member: {len(population.members)}")
