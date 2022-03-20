from src.models.member import Member
import math

# TODO move to contants.py?
global_minimum = 0.0


def compare_members(member1: Member, member2: Member):
    if math.fabs(member1.fitness_value - global_minimum) > math.fabs(member2.fitness_value - global_minimum):
        return 1
    if math.fabs(member1.fitness_value - global_minimum) == math.fabs(member2.fitness_value - global_minimum):
        return 0
    else:
        return -1
