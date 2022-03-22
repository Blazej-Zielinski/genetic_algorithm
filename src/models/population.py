import math

import numpy as np

from src.models.member import Member
import random
from functools import cmp_to_key
from src.utils.utils import compare_members


class Population:
    def __init__(self):
        self.size = 100
        # self.members = np.empty(self.size, dtype=Member)
        self.members = [Member([-10, 10], 6) for _ in range(self.size)]

    def create_child(self):
        return Member([-10, 10], 6)

    # selection
    def best_selection(self, percentage: int):
        if 0 > percentage or percentage > 100:
            print('Illegal percentage value')
            # TODO raise(sth);
            return

        result = sorted(self.members, key=cmp_to_key(compare_members))
        number_of_selected_members = math.ceil(self.size * percentage / 100)

        return result[:number_of_selected_members]

    def roulette_wheel_selection(self, percentage: int):
        fitness_sum = sum(1 / member.fitness_value for member in self.members)
        selection_probability = list(map(lambda member: (1 / member.fitness_value) / fitness_sum, self.members))
        number_of_selected_members = math.ceil(self.size * percentage / 100)

        # todo czy z powtórzeniami czy bez
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
            winner = min(tournaments[idx], key=lambda member: member.fitness_value)
            winners.append(winner)

        # todo self.members = winners ( czy wyrzuca sie tych co nie zostali wybrani)
        return winners

    # crossover
    def multipoint_crossover(self, parent1: Member, parent2: Member, crossover_points_number: int):
        x1_crossover_points = sorted(np.random.choice(
            np.arange(0, parent1.x1.binary_arr.size - 1),
            replace=False,
            size=crossover_points_number))
        x2_crossover_points = sorted(np.random.choice(
            np.arange(0, parent1.x2.binary_arr.size - 1),
            replace=False,
            size=crossover_points_number))

        child1, child2 = self.create_child(), self.create_child()

        child1.x1.binary_arr = parent1.x1.binary_arr.copy()
        child1.x2.binary_arr = parent1.x2.binary_arr.copy()

        child2.x1.binary_arr = parent2.x1.binary_arr.copy()
        child2.x2.binary_arr = parent2.x2.binary_arr.copy()

        for x1_crossover_point in x1_crossover_points:
            child1.x1.binary_arr = np.concatenate((
                child1.x1.binary_arr[:x1_crossover_point],
                parent2.x1.binary_arr[x1_crossover_point:]),
                axis=None)
            child2.x1.binary_arr = np.concatenate((
                child2.x1.binary_arr[:x1_crossover_point],
                parent1.x1.binary_arr[x1_crossover_point:]),
                axis=None)

        for x2_crossover_point in x2_crossover_points:
            child1.x2.binary_arr = np.concatenate((
                child1.x2.binary_arr[:x2_crossover_point],
                parent2.x2.binary_arr[x2_crossover_point:]),
                axis=None)
            child2.x2.binary_arr = np.concatenate((
                child2.x2.binary_arr[:x2_crossover_point],
                parent1.x2.binary_arr[x2_crossover_point:]),
                axis=None)

        child1.update_fitness_value()
        child2.update_fitness_value()

        return child1, child2

    def homogeneous_crossover(self, probability: float):
        if not (1 >= probability >= 0):
            return

        parent1, parent2 = random.sample(self.members, k=2)
        p1_chromosome_x1, p1_chromosome_x2 = parent1.x1, parent1.x2
        p2_chromosome_x1, p2_chromosome_x2 = parent2.x1, parent2.x2
        nr_of_bits = len(p1_chromosome_x1.binary_arr)

        ch1_chromosome_x1_bin_arr, ch1_chromosome_x2_bin_arr = p1_chromosome_x1.binary_arr.copy(), p1_chromosome_x2.binary_arr.copy()
        ch2_chromosome_x1_bin_arr, ch2_chromosome_x2_bin_arr = p2_chromosome_x1.binary_arr.copy(), p2_chromosome_x2.binary_arr.copy()

        for idx in range(nr_of_bits):
            random_value_for_x1 = random.random()
            random_value_for_x2 = random.random()

            # success mutation
            if random_value_for_x1 <= probability:
                temp = ch1_chromosome_x1_bin_arr[idx]
                ch1_chromosome_x1_bin_arr[idx] = ch2_chromosome_x1_bin_arr[idx]
                ch2_chromosome_x1_bin_arr[idx] = temp

            # success mutation
            if random_value_for_x2 <= probability:
                temp = ch1_chromosome_x2_bin_arr[idx]
                ch1_chromosome_x2_bin_arr[idx] = ch2_chromosome_x2_bin_arr[idx]
                ch2_chromosome_x2_bin_arr[idx] = temp

        child1, child2 = self.create_child(), self.create_child()

        child1.x1.binary_arr = ch1_chromosome_x1_bin_arr
        child1.x2.binary_arr = ch1_chromosome_x2_bin_arr
        child1.update_fitness_value()

        child2.x1.binary_arr = ch2_chromosome_x1_bin_arr
        child2.x2.binary_arr = ch2_chromosome_x2_bin_arr
        child2.update_fitness_value()

        return child1, child2

    def boundary_mutation(self, member: Member, probability: float):
        if not (1 >= probability >= 0):
            return

        which_boundary = random.randint(0, 1)

        generated_probability = random.random()
        if generated_probability <= probability:
            if which_boundary:
                member.x1.binary_arr[member.x1.binary_arr.size - 1] ^= 1
            else:
                member.x1.binary_arr[0] ^= 1

        generated_probability = random.random()
        if generated_probability <= probability:
            if which_boundary:
                member.x2.binary_arr[member.x1.binary_arr.size - 1] ^= 1
            else:
                member.x2.binary_arr[0] ^= 1

        member.update_fitness_value()

    def multipoint_mutation(self, member: Member, probability: float, mutation_points_number: int):
        if not (1 >= probability >= 0):
            return

        x1_mutation_points = sorted(np.random.choice(
            np.arange(0, member.x1.binary_arr.size - 1),
            replace=False,
            size=mutation_points_number))

        x2_mutation_points = sorted(np.random.choice(
            np.arange(0, member.x2.binary_arr.size - 1),
            replace=False,
            size=mutation_points_number))

        generated_probability = random.random()
        if generated_probability <= probability:
            for mutation_point in x1_mutation_points:
                member.x1.binary_arr[mutation_point] ^= 1

        generated_probability = random.random()
        if generated_probability <= probability:
            for mutation_point in x2_mutation_points:
                member.x2.binary_arr[mutation_point] ^= 1

    def inversion(self, member: Member):
        x1_crossover_points = sorted(np.random.choice(
            np.arange(0, member.x1.binary_arr.size - 1),
            replace=False,
            size=2))

        x2_crossover_points = sorted(np.random.choice(
            np.arange(0, member.x1.binary_arr.size - 1),
            replace=False,
            size=2))

        # Inversion for x1
        for x1_crossover_point in range(x1_crossover_points[0], x1_crossover_points[1]):
            member.x1.binary_arr[x1_crossover_point] = 1 - member.x1.binary_arr[x1_crossover_point]

        # Inversion for x2
        for x2_crossover_point in range(x2_crossover_points[0], x2_crossover_points[1]):
            member.x2.binary_arr[x2_crossover_point] = 1 - member.x2.binary_arr[x2_crossover_point]

    def elite_strategy(self, percentage: int):
        if not (100 >= percentage >= 0):
            return

        # Nr of elite members
        elite_members_nr = math.ceil(self.size * (percentage / 100))
        sorted_members = sorted(self.members, key=cmp_to_key(compare_members))

        return sorted_members[:elite_members_nr]
