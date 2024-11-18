import pandas as pd
import math
import random
import numpy as np

# Reading and parsing the TSP file
def read_parser(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        city_data_start = False
        city_info = []
        for line in lines:
            if "NODE_COORD_SECTION" in line:
                city_data_start = True
                continue
            if "EOF" in line:
                break
            if city_data_start:
                parts = line.strip().split()
                city_info.append((int(parts[0]), float(parts[1]), float(parts[2])))

    df = pd.DataFrame(city_info, columns=["ID", "X", "Y"])
    return df

# Distance function
def cities_distance(city1, city2):
    x1, y1 = city1["X"], city1["Y"]
    x2, y2 = city2["X"], city2["Y"]
    return round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

# Fitness function
def fitness(solution):
    total_distance = 0
    for i in range(len(solution)):
        city1_idx = solution[i] - 1
        city2_idx = solution[(i + 1) % len(solution)] - 1
        city1 = rp_df.iloc[city1_idx]
        city2 = rp_df.iloc[city2_idx]
        total_distance += cities_distance(city1, city2)
    return total_distance

# Population initialization
def create_initial_population(pop_size, include_greedy=False):
    population = []
    num_cities = rp_df.shape[0]

    # Greedy solutions
    if include_greedy:
        for starting_city in range(min(pop_size, num_cities)):
            _, greedy_solution = greedy_algorithm(starting_city)
            population.append(greedy_solution)

    # Random solutions
    while len(population) < pop_size:
        solution = list(range(1, num_cities + 1))
        random.shuffle(solution)
        population.append(solution)

    return population

# Greedy algorithm
def greedy_algorithm(starting_city):
    num_cities = rp_df.shape[0]
    visited = []
    current_city = starting_city
    tour = [current_city + 1]
    total_distance = 0

    while len(tour) < num_cities:
        min_dist = float("inf")
        nearest_city = None
        for idx, city in rp_df.iterrows():
            if idx not in visited:
                distance = cities_distance(rp_df.iloc[current_city], city)
                if distance < min_dist:
                    min_dist = distance
                    nearest_city = idx

        tour.append(nearest_city + 1)
        visited.append(current_city)
        current_city = nearest_city
        total_distance += min_dist

    total_distance += cities_distance(rp_df.iloc[current_city], rp_df.iloc[starting_city])
    return total_distance, tour

# Selection: Tournament selection
def tournament_selection(population):
    tournament_size = 3
    selected = random.sample(population, tournament_size)
    selected.sort(key=lambda x: x[1])  # Sort by fitness
    return selected[0][0]  # Return the individual (not the score)

# Crossover: Ordered crossover (OC)
def ordered_crossover(parent1, parent2):
    size = len(parent1)
    child = [-1] * size
    start, end = sorted(random.sample(range(size), 2))

    # Copy the segment from parent1 to child
    child[start:end] = parent1[start:end]

    # Fill the remaining cities from parent2
    pointer = end
    for city in parent2:
        if city not in child:
            while child[pointer] != -1:
                pointer = (pointer + 1) % size
            child[pointer] = city

    return child

# Mutation: Swap mutation
def mutation(individual, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

# Population evaluation
def evaluate_population(population):
    return [(indiv, fitness(indiv)) for indiv in population]

# Population statistics
def print_population_info(population):
    fitness_values = [fit for _, fit in population]
    print(f"Population size: {len(population)}")
    print(f"Best score: {min(fitness_values)}")
    print(f"Median score: {np.median(fitness_values)}")
    print(f"Worst score: {max(fitness_values)}")

# Genetic algorithm
def genetic_algorithm(pop_size, epochs, Px, Pm, stop_condition=None):
    # Initialize population
    population = create_initial_population(pop_size, include_greedy=True)
    evaluated_population = evaluate_population(population)
    best_solution = None
    best_score = float("inf")

    for t in range(epochs):
        new_population = []

        # Generate next generation
        while len(new_population) < pop_size:
            parent1 = tournament_selection(evaluated_population)
            parent2 = tournament_selection(evaluated_population)

            if random.random() < Px:
                child = ordered_crossover(parent1, parent2)
            else:
                child = parent1

            child = mutation(child, Pm)
            child_fitness = fitness(child)
            new_population.append((child, child_fitness))

            if child_fitness < best_score:
                best_score = child_fitness
                best_solution = child

        evaluated_population = new_population
        print(f"Epoch {t + 1}, Best Score: {best_score}")
        if stop_condition and stop_condition(best_score, t):
            break

    return best_solution, best_score

# Main execution
file_path = "berlin11_modified.tsp"
rp_df = read_parser(file_path)

# Parameters
pop_size = 10
epochs = 100
Px = 0.8  # Crossover probability
Pm = 0.2  # Mutation probability

best_solution, best_score = genetic_algorithm(pop_size, epochs, Px, Pm)
print("Best solution found:", best_solution)
print("Best score:", best_score)
