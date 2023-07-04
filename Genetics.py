import random
import heapq
from Bot import Bot
# Genetic algortihm

# Actions: scout, retreat, attack, return, getGold
# Variables: (6 bits) energy, (10 bits) score , (1 bit) flash, (1 bit) brezeze,
# (1 bit) steps, (4 bit) how_much_explored

# 6 bits (atack_g) = 64
# 7 bits (score_g) = 128
# 6 bits (retreat_g) = 64
# 6 bits (fitness_to_gold_g) = 64
# 7 bits (a_estrela) = 128

# 32 bits (total)
# Genome: 32 bits (int)

# aaaaaaassssssssssrrrrrrrffffffff

# 1. Generate initial population
# 2. Evaluate fitness
# 3. Select parents
# 4. Crossover
# 5. Mutation
# 6. Repeat

"""
if breeze:
    retreat()
elif flash or steps:
    if energy > attack_g:
        attack()
    else:
        retreat() # fugir
elif energy < retreat_g:
    retreat() # pegar mais energia
elif score < score_g:
    if fitness_to_gold < fitness_to_gold_g:
        explorar()
    else:
        getGold()
"""
class Genetics:
    n_pop = 10
    # step 1
    # Generate initial population
    def __init__(self,n_pop = 10):
        self.n_pop = n_pop

    def generate_population(self):
        population = []
        for i in range(self.n_pop):
            population.append(random.randint(0, 2**32 - 1))
        return population

    def select_parents(self, population_with_fitness:list[int]):
        return heapq.nlargest(4, range(len(population_with_fitness)), population_with_fitness.__getitem__)

    def crossover(self, population:list[int], parents:list[int]):
        new_population = []
        for i in range(self.n_pop):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            crossover_point = random.randint(0, 31)
            new_population.append((population[parent1] & (2**crossover_point - 1)) + (population[parent2] & (2**(32 - crossover_point) - 1)))
        return new_population
    
    def mutation(self, population:list[int]):
        for i in range(self.n_pop):
            if random.randint(0, 100) < 5:
                population[i] = population[i] ^ (1 << random.randint(0, 31))
        return population

    def _digivolve(self,bots:list[tuple[int, int]]):
        population_with_fitness = []
        for bot in bots:
            population_with_fitness.append(bot[1])
        parents = self.select_parents(population_with_fitness)
        p = [bots[i][0] for i in parents]
        population = self.crossover(population_with_fitness, p)
        population = self.mutation(population)
        return population
    
    def parse_to_dict(self,genome:int) -> dict[str, int]:
        max_energy = 100
        max_score = 90_000
        max_retreat = 100
        max_fitness_to_gold = 100
        max_a_estrela = 100

        attack_g = genome & 0b111111
        score_g = (genome >> 6) & 0b1111111
        retreat_g = (genome >> 13) & 0b111111
        fitness_to_gold_g = (genome >> 19) & 0b111111
        a_estrela = (genome >> 25) & 0b1111111

        attack_g = int(attack_g / 63 * max_energy)
        score_g = int(score_g / 127 * max_score)
        retreat_g = int(retreat_g / 63 * max_retreat)
        fitness_to_gold_g = int(fitness_to_gold_g / 63 * max_fitness_to_gold)
        a_estrela = int(a_estrela / 127 * max_a_estrela)


        return {
            "attack": attack_g,
            "score": score_g,
            "retreat": retreat_g,
            "fitness_to_gold": fitness_to_gold_g,
            "a_estrela": a_estrela,
            "genome": genome
        }
    
    def digivolve(self,bots:list[tuple[int, int]]) -> list[dict[str, int]]:
        population = self._digivolve(bots)
        g_dict = []
        for genome in population:
            g_dict.append(self.parse_to_dict(genome))

        return g_dict
            
