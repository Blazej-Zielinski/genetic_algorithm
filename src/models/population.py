import math
import numpy as np
import random
from functools import cmp_to_key
from src.models.member import Member
from src.utils.utils import compare_members
from src.algorithm.conf import OptimizationType


class Population:
    def __init__(self, interval, precision, size, optimization):
        self.size = size
        self.members = [Member(interval, precision) for _ in range(self.size)]
        self.optimization = optimization

        # chromosome config
        self.interval = interval
        self.precision = precision

    def create_child(self):
        return Member(self.interval, self.precision)

    def best_selection(self, percentage: int):
        if not (100 >= percentage >= 0):
            return

        result = sorted(self.members, key=cmp_to_key(compare_members), reverse=OptimizationType.MAXIMIZATION.value == self.optimization)
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
        iterations = math.ceil(self.size / tournament_size)
        tournaments = []
        winners = []
        members_copy = self.members.copy()

        for idx in range(iterations):
            tournaments.append(random.sample(members_copy, tournament_size))
            # remove all elements that occur in one list form another
            members_copy = [member for member in members_copy if member not in tournaments[idx]]

        # getting winners
        for idx in range(len(tournaments)):
            winner = max(tournaments[idx], key=lambda member: member.fitness_value) \
                if OptimizationType.MAXIMIZATION.value == self.optimization \
                else min(tournaments[idx], key=lambda member: member.fitness_value)
            winners.append(winner)

        self.members = winners
        return winners

    def multipoint_crossover(self, parent1: Member, parent2: Member, probability: float, crossover_points_number: int):
        if not (1 >= probability >= 0):
            return
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
        if not (1 >= probability >= 0):
            return

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
        if not (1 >= probability >= 0):
            return

        for i in range(0, member.chromosomes.size):
            which_boundary = random.randint(0, 1)

            if random.random() <= probability:
                if which_boundary:
                    member.chromosomes[i].binary_arr[member.chromosomes[i].binary_arr.size - 1] ^= 1
                else:
                    member.chromosomes[i].binary_arr[0] ^= 1

        member.update_fitness_value()

    def multipoint_mutation(self, member: Member, probability: float, mutation_points_number: int):
        if not (1 >= probability >= 0):
            return

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

    def elite_strategy(self, percentage: int):
        if percentage > 100 or percentage <= 0:
            return []

        # Nr of elite members
        elite_members_nr = math.ceil(self.size * (percentage / 100))
        sorted_members = sorted(self.members, key=cmp_to_key(compare_members), reverse=OptimizationType.MAXIMIZATION.value == self.optimization)

        # Delete elite members from self.members
        self.members = [member for member in self.members if member not in sorted_members[:elite_members_nr]]

        return sorted_members[:elite_members_nr]
