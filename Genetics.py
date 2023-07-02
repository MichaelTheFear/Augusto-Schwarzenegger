import random
import heapq
# Genetic algortihm

# Actions: scout, retreat, attack, return, getGold
# Variables: (6 bits) energy, (10 bits) score , (1 bit) flash, (1 bit) brezeze,
# (1 bit) steps, (4 bit) how_much_explored

# 7 bits (atack_g)
# 10 bits (score_g)
# 7 bits (retreat_g)
# 8 bits (fitness_to_gold_g)
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
    if energy > attack_x:
        attack()
    else:
        retreat()
elif energy < retreat_g:
    retreat()
elif score < score_g:
    if fitness_to_gold < fitness_to_gold_g:
        scout()
    else:
        getGold()
"""
class Genetics:
    population = 10
    # step 1
    # Generate initial population
    def generate_population(self):
        population = []
        for i in range(self.population):
            population.append(random.randint(0, 2**32 - 1))
        return population

    def select_parents(self, population_with_fitness:list[int]):
        return heapq.nlargest(4, range(len(population_with_fitness)), population_with_fitness.__getitem__)

    def crossover(self, population:list[int], parents:list[int]):
        new_population = []
        for i in range(self.population):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            crossover_point = random.randint(0, 31)
            new_population.append((population[parent1] & (2**crossover_point - 1)) + (population[parent2] & (2**(32 - crossover_point) - 1)))
        return new_population
    
    def mutation(self, population:list[int]):
        for i in range(self.population):
            if random.randint(0, 100) < 5:
                population[i] = population[i] ^ (1 << random.randint(0, 31))
        return population

    def digivolve(self,bots:list[tuple[int, int]]):
        population_with_fitness = []
        for bot in bots:
            population_with_fitness.append(bot[1])
        parents = self.select_parents(population_with_fitness)
        population = self.crossover(population_with_fitness, parents)
        population = self.mutation(population)
        return population
    
    def parse_to_dict(self,genome:int) -> dict[str, int]:
        max_energy = 100
        max_score = 90_000
        max_retreat = 100
        max_fitness_to_gold = 100

        attack_g = (genome & 0b11111110000000000000000000000000) >> 25
        score_g = (genome & 0b00000001111111111111100000000000) >> 15
        retreat_g = (genome & 0b00000000000000000000011111100000) >> 10
        fitness_to_gold_g = (genome & 0b00000000000000000000000000011111)

        # convert to range proper range
        attack_g = int(attack_g / 2**7 * max_energy)
        score_g = int(score_g / 2**10 * max_score)
        retreat_g = int(retreat_g / 2**7 * max_retreat)
        fitness_to_gold_g = int(fitness_to_gold_g / 2**8 * max_fitness_to_gold)


        return {
            "attack": attack_g,
            "score": score_g,
            "retreat": retreat_g,
            "fitness_to_gold": fitness_to_gold_g,
            "genome": genome
        }
