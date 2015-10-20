#!/usr/bin/env python
"""
"We'd like exactly $15.05 worth of appetisers, please..."

QUESTION: can you find both optimal solutions (there are two)?
QUESTION: what happens when you initialise with large number of items?

"""
import random

from copy import deepcopy
from operator import attrgetter
from collections import namedtuple

ITEMS = [
	"Mixed Fruit", "French Fries", "Side Salad",
	"Hot Wings", "Mozzarella Sticks", "Sampler Plate"
]
PRICES = [2.15, 2.75, 3.35, 3.55, 4.2, 5.8]
TARGET = 15.05

GENERATIONS = 50
POPULATION_SIZE = 100
TOURNAMENT_SIZE = 5
CROSSOVER_PROBABILITY = 0.5
MUTATION_PROBABILITY = 0.5
MUTATION_CHANCE = 0.4

Individual = namedtuple("Individual", "solution fitness")


def evaluate(solution):
	price = sum(s * p for s,p in zip(solution, PRICES))
	return abs(TARGET - price)


def init():
	solution = [0] * len(ITEMS)
	items = (int(random.random() * len(ITEMS)) for i in range(3))
	for i in items:
		solution[i] += 1
	return Individual(solution, evaluate(solution))


def mutate(solution):
	for i in range(len(solution)):
		if random.random() < MUTATION_CHANCE:
			solution[i] += random.choice([-1, 1])
			solution[i] = max(0, solution[i])


def crossover_uniform(a, b, probability=0.25):
	"""
	Uniform crossover: AAABBABBABB, BBBAABAABAA (in place).

	"""
	size = min(len(a), len(b))
	for i in range(size):
		if random.random() < probability:
			a[i], b[i] = b[i], a[i]


def select(population, k, tournament_size):
	chosen = []
	for i in range(k):
		candidates = random.sample(population, tournament_size)
		winner = min(candidates, key=attrgetter("fitness"))
		chosen.append(deepcopy(winner))
	return chosen


def variate(population):
	for i in range(1, len(population), 2):
		if random.random() < CROSSOVER_PROBABILITY:
			crossover_uniform(population[i-1].solution, population[i].solution)

	for i in range(len(population)):
		if random.random() < MUTATION_PROBABILITY:
			mutate(population[i].solution)
	return population


population = [init() for i in range(POPULATION_SIZE)]

for i in range(GENERATIONS):
	chosen = select(population, len(population), TOURNAMENT_SIZE)
	population = variate(chosen)

	for i in range(len(population)):
		new_fitness = evaluate(population[i].solution)
		population[i] = population[i]._replace(fitness=new_fitness)

population.sort(key=attrgetter("fitness"))
params = population[0].fitness, population[-1].fitness, population[POPULATION_SIZE / 2].fitness
print("best={0}, worst={1}, median={2}".format(*params))

for params in zip(population[0].solution, ITEMS):
	print("{0} x {1}".format(*params))
