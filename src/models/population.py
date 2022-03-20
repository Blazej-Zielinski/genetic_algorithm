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
            np.arange(0, parent1.x1.binary_arr.size),
            replace=False,
            size=crossover_points_number))
        x2_crossover_points = sorted(np.random.choice(
            np.arange(0, parent1.x2.binary_arr.size),
            replace=False,
            size=crossover_points_number))

        child = self.create_child()
        child.x1.binary_arr = parent1.x1.binary_arr.copy()
        child.x2.binary_arr = parent1.x2.binary_arr.copy()

        for x1_crossover_point in x1_crossover_points:
            child.x1.binary_arr = np.concatenate((
                child.x1.binary_arr[:x1_crossover_point],
                parent2.x1.binary_arr[x1_crossover_point:]),
                axis=None)

        for x2_crossover_point in x2_crossover_points:
            child.x2.binary_arr = np.concatenate((
                child.x2.binary_arr[:x2_crossover_point],
                parent2.x2.binary_arr[x2_crossover_point:]),
                axis=None)

        child.update_fitness_value()

        return child

    def homogeneous_crossover(self, probability: float):
        if not (1 >= probability >= 0):
            return

        parent1, parent2 = random.sample(self.members, k=2)
        p1_chromosome_x1, p1_chromosome_x2 = parent1.x1, parent1.x2
        p2_chromosome_x1, p2_chromosome_x2 = parent2.x1, parent2.x2
        nr_of_bits = len(p1_chromosome_x1.binary_arr)

        ch_chromosome_x1_bin_arr, ch_chromosome_x2_bin_arr = p1_chromosome_x1.binary_arr.copy(), p1_chromosome_x2.binary_arr.copy()

        for idx in range(nr_of_bits):
            random_value_for_x1 = random.random()
            random_value_for_x2 = random.random()

            # success mutation
            if random_value_for_x1 <= probability:
                ch_chromosome_x1_bin_arr[idx] = p2_chromosome_x1.binary_arr[idx]

            if random_value_for_x2 <= probability:
                ch_chromosome_x2_bin_arr[idx] = p2_chromosome_x2.binary_arr[idx]

        child = self.create_child()
        child.x1.binary_arr = ch_chromosome_x1_bin_arr
        child.x2.binary_arr = ch_chromosome_x2_bin_arr
        child.update_fitness_value()

        # print(f"parent1: {parent1} : {parent1.x1.binary_arr} {parent1.x2.binary_arr}")
        # print(f"parent2: {parent2} : {parent2.x1.binary_arr} {parent1.x2.binary_arr}")
        # print(f"child: {child} : {child.x1.binary_arr} {child.x2.binary_arr}")

        return child
