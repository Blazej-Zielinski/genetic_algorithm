import tkinter as tk
from src.gui.gui import GeneticAlgorithmInterface


# population = Population([-10, 10], 6, 100)
# population.best_selection(32)
# population.tournament_selection(20)
#
# population.homogeneous_crossover(population.members[1], population.members[5], 0.25)
#
# child = population.multipoint_crossover(population.members[1], population.members[5], 2)
#
# population.elite_strategy(1)
#
# population.boundary_mutation(population.members[0], 0.7)

if __name__ == "__main__":

    root = tk.Tk()
    GeneticAlgorithmInterface(root)
    root.mainloop()