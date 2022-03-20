from src.models.chromosome import Chromosome
from src.models.member import Member

chr1 = Chromosome([-10, 10], 6)
chr2 = Chromosome([-10, 10], 6)
member = Member([chr1, chr2])

# print(chr1.binary_arr)
# print(chr1.calculate_decimal())

print(chr1.calculate_decimal())
print(chr2.calculate_decimal())
print(member.calculate_fitness_fun())
