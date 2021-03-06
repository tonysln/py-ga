#!/usr/bin/env python

# genpixel.py
# Basic GA implementation for guessing pixel values (chars) for an image.
# Each image is represented as an array of ASCII characters.

# Using pypy3 is a must due to atrocious performance at the moment.
# Recommended image side length: [4,12].

import random
import math
import os
from PIL import Image


PIXEL_CHARS = '@#O%+=|i-:. '[::-1]

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def pop_fitness(pop, target_repr, power):
    # Return a list of pairs [element, fitness]
    pop_fit = []
    for guess_repr in pop:
        fitness = img_fitness(guess_repr, target_repr, power)
        pop_fit.append((guess_repr,fitness))
    
    return pop_fit
    

def img_fitness(guess_repr, target_repr, power):
    fitness = sum(u == v for u,v in zip(guess_repr,target_repr)) / len(target_repr)
    return pow(fitness, power)
    

def populate(size, img_size):
    # Generate random images
    pop = []
    for i in range(size):
        dna = repr(random_img(img_size))
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
    

def mutate(item, rate):
    # Introduce a random mutation based on the rate.
    # Decision made for every char
    mutated = item
    for i in range(len(mutated)):
        if random.random() < rate:
            mutated = mutated[:i] + random.choice(PIXEL_CHARS) + mutated[i+1:]
    
    return mutated
    

def generate(pool, rate):
    # Choose random parents, apply crossover & mutation
    num_parents = 2
    parents = []
    for i in range(num_parents):
        parents.append(random.choice(pool)[0])

    child = crossover(parents)
    return mutate(child, rate)
    

def run(target_img, img_size, pop_size, mut_rate, power, print_img=True):
    generations = 0
    found = False
    # Initial population
    population = populate(pop_size, img_size)

    while not found:
        generations += 1
        # Calculate fitness of each element
        population = pop_fitness(population, target_img, power)
        # Create mating pool & get best element
        pool,best_elem,best_fit = create_pool(population)

        output = f'[{generations:05}] {round(best_fit,5):.5f}'
        if generations % 100 == 0:
            if print_img:
                cls()
                draw_img(repr_to_arr(best_elem, img_size))
            print(output)

        # Target string found
        if best_elem == target_img or best_fit == 1.0:
            found = True
            cls()
            draw_img(repr_to_arr(best_elem, img_size))
            print(output)
            print('='*((img_size*2)+3))

        # Apply crossover & mutation
        population = [generate(pool, mut_rate) for elem in population] 


def repr(img_array):
    repr = ''
    for line in img_array:
        repr += ''.join(line)

    return repr


def draw_img(img_array):
    size = len(img_array)
    
    print(f'???{"???"*(size*2+1)}???')
    for line in img_array:
       print(f'??? {" ".join(line)} ???')

    print(f'???{"???"*(size*2+1)}???')


def repr_to_arr(img_repr, size):
    img = []
    for i in range(0, len(img_repr), size):
        img.append(img_repr[i:i+size])
    return img


def random_img(size):
    img = []
    for y in range(size):
        img.append([random.choice(PIXEL_CHARS) for x in range(size)])
    return img


def convert_img(path, size):
    img = Image.open(path).convert('L')
    img = img.resize((size, size))

    img_pixels = list(img.getdata())
    img_array = []
    for i in range(0, len(img_pixels), size):
        line = img_pixels[i:i+size]
        img_array.append([PIXEL_CHARS[pixel//25] for pixel in line])

    return img_array


if __name__ == '__main__':
    side_len = 12

    # target = random_img(side_len)
    target = convert_img('tux.png', side_len)

    pop_size = 1000
    mut_rate = 0.0008
    power = 5
    print_img = False
    run(repr(target), side_len, pop_size, mut_rate, power, print_img)

    draw_img(target)
    print('Done.')
    