
from src.models.population import Population


population = Population()
population.best_selection(32)
population.tournament_selection(20)

population.homogeneous_crossover(0.25)

child = population.multipoint_crossover(population.members[1], population.members[5], 2)
