import math
import numpy as np
import random
from abc import ABC
from functools import cmp_to_key
from src.models.member import Member
from src.utils.utils import compare_members
from src.algorithm.conf import OptimizationType


class Population(ABC):
    def __init__(self, interval, precision, chromosome_type, size, optimization):
        self.size = size
        self.members = [Member(interval, precision, chromosome_type) for _ in range(self.size)]
        self.optimization = optimization

        # chromosome config
        self.interval = interval
        self.precision = precision
        self.chromosome_type = chromosome_type

    def create_child(self):
        return Member(self.interval, self.precision, self.chromosome_type)

    def best_selection(self, percentage: int):
        result = sorted(self.members, key=cmp_to_key(compare_members),
                        reverse=OptimizationType.MAXIMIZATION.value == self.optimization)
        number_of_selected_members = math.ceil(self.size * percentage / 100)

        self.members = result[:number_of_selected_members]
        return result[:number_of_selected_members]

    def roulette_wheel_selection(self, percentage: int):
        fitness_sum = sum(1 / member.fitness_value for member in self.members)
        selection_prob_fun = (lambda member: member.fitness_value / fitness_sum) \
            if OptimizationType.MAXIMIZATION.value == self.optimization \
            else (lambda member: (1 / member.fitness_value) / fitness_sum)

        selection_probability = list(map(selection_prob_fun, self.members))
        number_of_selected_members = math.ceil(self.size * percentage / 100)

        selected_members = random.choices(self.members, weights=selection_probability, k=number_of_selected_members)

        return selected_members

    def tournament_selection(self, tournament_size: int):
        iterations = math.floor(len(self.members) / tournament_size)
        tournaments = []
        winners = []
        members_copy = self.members.copy()

        for idx in range(iterations):
            tournaments.append(random.sample(members_copy, tournament_size))
            # remove all elements that occur in one list form another
            members_copy = [member for member in members_copy if member not in tournaments[idx]]

        if len(members_copy) > 0:
            tournaments.append(random.sample(members_copy, len(members_copy)))

        # getting winners
        for idx in range(len(tournaments)):
            winner = max(tournaments[idx], key=lambda member: member.fitness_value) \
                if OptimizationType.MAXIMIZATION.value == self.optimization \
                else min(tournaments[idx], key=lambda member: member.fitness_value)
            winners.append(winner)

        self.members = winners
        return winners

    def elite_strategy(self, percentage: int):
        # Nr of elite members
        elite_members_nr = math.ceil(self.size * (percentage / 100))
        sorted_members = sorted(self.members, key=cmp_to_key(compare_members),
                                reverse=OptimizationType.MAXIMIZATION.value == self.optimization)

        # Delete elite members from self.members
        self.members = [member for member in self.members if member not in sorted_members[:elite_members_nr]]

        return sorted_members[:elite_members_nr]


class PopulationReal(Population):
    def __init__(self, interval, precision, chromosome_type, size, optimization):
        super().__init__(interval, precision, chromosome_type, size, optimization)

    def arithmetic_crossover(self, parent1: Member, parent2: Member, probability: float):
        if random.random() >= probability:
            return []

        child1 = self.create_child()
        child1.chromosomes[0].value = probability * parent1.chromosomes[0].value + (1 - probability) * \
                                      parent2.chromosomes[0].value
        child1.chromosomes[1].value = probability * parent1.chromosomes[1].value + (1 - probability) * \
                                      parent2.chromosomes[1].value

        child2 = self.create_child()
        child2.chromosomes[0].value = (1 - probability) * parent1.chromosomes[0].value + probability * \
                                      parent2.chromosomes[0].value
        child2.chromosomes[1].value = (1 - probability) * parent1.chromosomes[1].value + probability * \
                                      parent2.chromosomes[1].value

        child1.update_fitness_value()
        child2.update_fitness_value()

        return child1, child2

    def blend_crossover(self, parent1: Member, parent2: Member, probability: float, alpha: float, beta: float = None):
        if random.random() >= probability:
            return []

        children = [self.create_child() for _ in range(2)]
        beta = beta if beta is not None else alpha

        for child in children:
            dx = abs(parent1.chromosomes[0].value - parent2.chromosomes[0].value)
            dy = abs(parent1.chromosomes[1].value - parent2.chromosomes[1].value)

            while True:
                child.chromosomes[0].value = random.uniform(
                    min(parent1.chromosomes[0].value, parent2.chromosomes[0].value) - alpha * dx,
                    max(parent1.chromosomes[0].value, parent2.chromosomes[0].value) + beta * dx)

                child.chromosomes[1].value = random.uniform(
                    min(parent1.chromosomes[1].value, parent2.chromosomes[1].value) - alpha * dy,
                    max(parent1.chromosomes[1].value, parent2.chromosomes[1].value) + beta * dy)

                child.update_fitness_value()
                if child.chromosomes[0].is_value_in_interval() and child.chromosomes[1].is_value_in_interval():
                    break

        return children

    def average_crossover(self, parent1: Member, parent2: Member, probability: float):
        if not random.random() <= probability:
            return []

        child = self.create_child()
        for idx, chromosome in enumerate(child.chromosomes):
            chromosome.value = (parent1.chromosomes[idx].value + parent2.chromosomes[idx].value) / 2

        child.update_fitness_value()
        return [child]

    def linear_crossover(self, parent1: Member, parent2: Member, probability: float):
        if not random.random() <= probability:
            return []

        children = [self.create_child() for _ in range(3)]
        factors = [
            [[0.5, 0.5], [0.5, 0.5]],
            [[1.5, -0.5], [1.5, -0.5]],
            [[-0.5, 1.5], [-0.5, 1.5]]
        ]

        for i, child in enumerate(children):
            for j, chromosome in enumerate(child.chromosomes):
                chromosome.value = factors[i][j][0] * parent1.chromosomes[j].value + factors[i][j][1] * \
                                   parent2.chromosomes[j].value
            child.update_fitness_value()

        filtered_children = list(
            filter(lambda r: r.chromosomes[0].is_value_in_interval() and r.chromosomes[1].is_value_in_interval(),
                   children))
        if len(filtered_children) < 2:
            return []

        result = sorted(filtered_children, key=cmp_to_key(compare_members),
                        reverse=OptimizationType.MAXIMIZATION.value == self.optimization)[:2]

        return result[:2]

    def uniform_mutation(self, member: Member, probability: float):
        if not random.random() <= probability:
            return

        index_to_update = random.randint(0, 1)
        member.chromosomes[index_to_update].value = random.uniform(self.interval[0], self.interval[1])
        member.update_fitness_value()

    def gauss_mutation(self, member: Member, probability: float):
        if not random.random() <= probability:
            return

        n_distribution = np.random.normal()
        if (self.interval[0] <= member.chromosomes[0].value + n_distribution <= self.interval[1]) and (
                self.interval[0] <= member.chromosomes[1].value + n_distribution <= self.interval[1]):
            for chromosome in member.chromosomes:
                chromosome.value += n_distribution
            member.update_fitness_value()


class PopulationBinary(Population):
    def __init__(self, interval, precision, chromosome_type, size, optimization):
        super().__init__(interval, precision, chromosome_type, size, optimization)

    def multipoint_crossover(self, parent1: Member, parent2: Member, probability: float, crossover_points_number: int):
        if random.random() >= probability:
            return []

        child1, child2 = self.create_child(), self.create_child()

        for i in range(parent1.chromosomes.size):
            crossover_points = sorted(np.random.choice(
                np.arange(0, parent1.chromosomes[i].binary_arr.size - 1),
                replace=False,
                size=crossover_points_number))

            child1.chromosomes[i].binary_arr = parent1.chromosomes[i].binary_arr.copy()
            child2.chromosomes[i].binary_arr = parent2.chromosomes[i].binary_arr.copy()

            for crossover_point in crossover_points:
                child1.chromosomes[i].binary_arr = np.concatenate((
                    child1.chromosomes[i].binary_arr[:crossover_point],
                    parent2.chromosomes[i].binary_arr[crossover_point:]),
                    axis=None)
                child2.chromosomes[i].binary_arr = np.concatenate((
                    child2.chromosomes[i].binary_arr[:crossover_point],
                    parent1.chromosomes[i].binary_arr[crossover_point:]),
                    axis=None)

        child1.update_fitness_value()
        child2.update_fitness_value()

        return child1, child2

    def homogeneous_crossover(self, parent1: Member, parent2: Member, probability: float):
        child1, child2 = self.create_child(), self.create_child()

        for i in range(parent1.chromosomes.size):
            child1.chromosomes[i].binary_arr = parent1.chromosomes[i].binary_arr.copy()
            child2.chromosomes[i].binary_arr = parent2.chromosomes[i].binary_arr.copy()
            nr_of_bits = parent1.chromosomes[i].binary_arr.size

            for idx in range(nr_of_bits):

                # success mutation
                if random.random() <= probability:
                    temp = child1.chromosomes[i].binary_arr[idx]
                    child1.chromosomes[i].binary_arr[idx] = child2.chromosomes[i].binary_arr[idx]
                    child2.chromosomes[i].binary_arr[idx] = temp

        child1.update_fitness_value()
        child2.update_fitness_value()

        return child1, child2

    def boundary_mutation(self, member: Member, probability: float):
        for i in range(0, member.chromosomes.size):
            which_boundary = random.randint(0, 1)

            if random.random() <= probability:
                if which_boundary:
                    member.chromosomes[i].binary_arr[member.chromosomes[i].binary_arr.size - 1] ^= 1
                else:
                    member.chromosomes[i].binary_arr[0] ^= 1

        member.update_fitness_value()

    def multipoint_mutation(self, member: Member, probability: float, mutation_points_number: int):
        for i in range(0, member.chromosomes.size):
            mutation_points = sorted(np.random.choice(
                np.arange(0, member.chromosomes[i].binary_arr.size - 1),
                replace=False,
                size=mutation_points_number))

            if random.random() <= probability:
                for mutation_point in mutation_points:
                    member.chromosomes[i].binary_arr[mutation_point] ^= 1

        member.update_fitness_value()

    def inversion(self, member: Member, probability: float):
        if not random.random() <= probability:
            return

        for i in range(0, member.chromosomes.size):
            inversion_points = sorted(np.random.choice(
                np.arange(0, member.chromosomes[i].binary_arr.size - 1),
                replace=False,
                size=2))

            for inversion_point in range(inversion_points[0], inversion_points[1]):
                member.chromosomes[i].binary_arr[inversion_point] ^= 1

        member.update_fitness_value()
