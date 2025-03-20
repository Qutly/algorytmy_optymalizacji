import random

MAX_KNAPSACK_WEIGHT = 50
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.01
REPRODUCTION_RATE = 0.15
GENERATIONS = 1000
POPULATION_SIZE = 10
NUM_ITEMS = 15  

class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value
        
    def __str__(self):
        return f"{self.name} (Value: {self.value}, Weight: {self.weight})"
    
class Individual:
    def __init__(self, bits):
        self.bits = bits
    
    def __str__(self):
        return f"Bits: {self.bits}, Fitness: {self.fitness()}"

    def __hash__(self):
        return hash(str(self.bits))
    
    def fitness(self):
        total_value = sum(bit * item.value for item, bit in zip(items, self.bits))
        total_weight = sum(bit * item.weight for item, bit in zip(items, self.bits))

        return total_value if total_weight <= MAX_KNAPSACK_WEIGHT else 0

def generate_items(num):
    item_list = []
    for i in range(num):
        name = f"Item-{i+1}"
        weight = random.randint(1, 15)
        value = random.randint(5, 25)
        item_list.append(Item(name, weight, value))
    return item_list

def init_population(count=POPULATION_SIZE):
    population = set()
    while len(population) < count:
        bits = [random.choice([0, 1]) for _ in items]
        population.add(Individual(bits))
    return list(population)

def selection(population):
    parents = []
    contenders = random.sample(population, 4)
    parents.append(max(contenders[:2], key=lambda i: i.fitness()))
    parents.append(max(contenders[2:], key=lambda i: i.fitness()))
    return parents

def crossover(parents):
    N = len(items)
    cut = random.randint(1, N - 1)
    child1 = parents[0].bits[:cut] + parents[1].bits[cut:]
    child2 = parents[1].bits[:cut] + parents[0].bits[cut:]
    return [Individual(child1), Individual(child2)]

def mutate(individuals):
    for individual in individuals:
        for i in range(len(individual.bits)):
            if random.random() < MUTATION_RATE:
                individual.bits[i] = 1 - individual.bits[i]

def next_generation(population):
    next_gen = []
    while len(next_gen) < len(population):
        parents = selection(population)

        if random.random() < REPRODUCTION_RATE:
            children = parents
        else:
            if random.random() < CROSSOVER_RATE:
                children = crossover(parents)
            else:
                children = parents.copy()

            mutate(children)

        next_gen.extend(children)
    
    return next_gen[:len(population)]

def average_fitness(population):
    return sum(i.fitness() for i in population) / len(population)

def knapsack():
    population = init_population()

    print("Initial Population:")
    for individual in population:
        print(individual)
    print("-" * 40)

    for generation in range(GENERATIONS):
        avg_fit = average_fitness(population)

        if generation % 100 == 0 or generation == GENERATIONS - 1:
            best = max(population, key=lambda i: i.fitness())
            print(f"Generation {generation:4}: Avg Fitness = {avg_fit:.2f}, Best Fitness = {best.fitness()}")

        population = next_generation(population)

    best_solution = max(population, key=lambda i: i.fitness())
    return best_solution

if __name__ == '__main__':
    print(f"Generating {NUM_ITEMS} random items...\n")
    items = generate_items(NUM_ITEMS)

    for item in items:
        print(item)
    print("\n" + "=" * 40 + "\n")

    print(f"Starting Genetic Algorithm (Knapsack Max Weight = {MAX_KNAPSACK_WEIGHT})...\n")
    solution = knapsack()

    print("\nBest solution found:")
    print(solution)
    print("Items included:")
    for bit, item in zip(solution.bits, items):
        if bit:
            print(f"- {item}")
