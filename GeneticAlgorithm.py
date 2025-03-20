import random
import numpy as np
import time

# Parametry
population_size = 10000
chromosome_length = 10
generations = 100
crossover_rate = 0.8
mutation_rate = 0.01


# Funkcja celu

def objective_function(chromosome):
    n = len(chromosome)
    result = 10 * n
    for xi in chromosome:
        result += xi ** 2 - 10 * np.cos(2 * np.pi * xi)
    return result


# Inicjalizacja populacji

def initialize_population():
    population = []
    for _ in range(population_size):
        chromosome = [random.uniform(-5.12, 5.12) for _ in range(chromosome_length)]
        population.append(chromosome)
    return population


# Ewaluacja populacji

def evaluate_population(population):
    fitness_value = []
    for individual in population:
        fitness_value.append(objective_function(individual))
    return fitness_value


# Selekcja turniejowa

def tournament_selection(population, fitness_value):
    tournament_size = 5
    best = None
    best_fitness = float('inf')
    for _ in range(tournament_size):
        index = random.randint(0, len(population) - 1)
        if fitness_value[index] < best_fitness:
            best = population[index]
            best_fitness = fitness_value[index]
    return best


# Krzyżowanie

def crossover(parent1, parent2):
    offspring = []
    for i in range(chromosome_length):
        offspring.append(parent1[i] if random.random() < 0.5 else parent2[i])
    return offspring


# Mutacja

def mutate(chromosome):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] += random.uniform(-1, 1)


def run_genetic_algorithm():
    population = initialize_population()

    for generation in range(generations):
        fitness_values = evaluate_population(population)
        best_index = np.argmin(fitness_values)
        best_fitness = fitness_values[best_index]
        best_chromosome = population[best_index]

        print(f"\nGeneracja {generation}, najlepsza wartość celu: {best_fitness:.4f}")
        print(f"Chromosom najlepszego osobnika: {', '.join([f'{x:.4f}' for x in best_chromosome])}")

        new_population = []
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, fitness_values)
            parent2 = tournament_selection(population, fitness_values)

            if random.random() < crossover_rate:
                offspring = crossover(parent1, parent2)
            else:
                offspring = parent1

            mutate(offspring)
            new_population.append(offspring)

        population = new_population


start_time = time.time()
run_genetic_algorithm()
end_time = time.time()

print(f"\nCzas wykonania: {end_time - start_time:.4f} sekundy")
