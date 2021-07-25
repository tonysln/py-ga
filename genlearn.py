#!/usr/bin/env python

# genlearn.py
# Basic GA implementation for guessing strings.

# Use pypy3 for vastly better performance!

import random
import math
import string


CHARS = string.ascii_letters + ' ,.?!1234567890';

def pop_fitness(pop, target, power):
    # Return a list of pairs [element, fitness]
    pop_fit = []
    for guess in pop:
        fitness = fitness_strings(guess, target, power)
        pop_fit.append((guess,fitness))
    
    return pop_fit


def fitness_strings(guess, target, power):
    # Percentage of correct chars in correct position
    fitness = sum(u == v for u,v in zip(guess,target)) / len(target)
    return pow(fitness, power)


def fitness_num(guess, target, power):
    try:
        fitness = sum(i==int(c) for i,c in enumerate(guess)) / len(target)
        return pow(fitness, power)
    except:
        return sum(c.isdigit() for c in guess) / len(target) / 10


def populate(size, word_size):
    # Generate random strings of given size & amount
    pop = []
    for i in range(size):
        dna = ''
        for j in range(word_size):
            dna += random.choice(CHARS)
        pop.append(dna)

    return pop


def create_pool(pop_with_fitness):
    # Choose elements for mating pool with a probability
    # proportional to their fitness score.
    pool = []
    max_fitness = 0
    sum_fitness = 0
    best_elem = ''
    
    # Find the best element
    for elem,score in pop_with_fitness:
        if score > max_fitness:
            max_fitness = score
            best_elem = elem
        sum_fitness += score
    
    # Random weighted choice
    for elem,score in pop_with_fitness:
        indx = 0
        r = random.uniform(0, sum_fitness)
        while (r > 0):
            r = r - pop_with_fitness[indx][1] # Score
            indx += 1

        indx -= 1;
        pool.append(pop_with_fitness[indx])

    return (pool, best_elem, max_fitness)


def crossover(parents):
    # Currently only 2 parents supported
    w1 = parents[0]
    w2 = parents[1]
    # Split in half
    pivot = len(w1) // 2
    return w2[:pivot] + w1[pivot:]


def mutate(guess, rate):
    # Introduce a random mutation based on the rate.
    # Decision made for every char
    mutated = guess
    for i in range(len(mutated)):
        if random.random() < rate:
            mutated = mutated[:i] + random.choice(CHARS) + mutated[i+1:]
    
    return mutated


def generate(pool, rate):
    # Choose random parents, apply crossover & mutation
    num_parents = 2
    parents = []
    for i in range(num_parents):
        parents.append(random.choice(pool)[0])

    child = crossover(parents)
    return mutate(child, rate)


def run(target, pop_size, mut_rate, power):
    generations = 0
    found = False
    # Initial population
    population = populate(pop_size, len(target))
   
    while not found:
        generations += 1
        # Calculate fitness of each element
        population = pop_fitness(population, target, power)
        # Create mating pool & get best element
        pool,best_elem,best_fit = create_pool(population)

        output = f'[{generations:05}]  {best_elem}  ({round(best_fit,5):.5f})'
        # Target string found
        if best_elem == target or best_fit == 1.0:
            found = True
            print(f'\n>>> {output} <<<')
        else:
            if generations % 100 == 0:
                print(output)

        # Apply crossover & mutation
        population = [generate(pool, mut_rate) for elem in population] 


if __name__ == '__main__':
    target = 'to be or not to be that is the question'
    pop_size = 400
    mutation_rate = 0.003
    power = 4

    run(target, pop_size, mutation_rate, power)
    print(f'Pop size: {pop_size}')
    print('Done.')   
