# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 21:27:22 2022

@author: Efrain
"""
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

rutas = [[0,7,9,8,20],
         [7,0,10,4,11],
         [9,10,0,15,5],
         [8,4,15,0,17],
         [20,11,5,17,0]]

#Problem parameter
NB_QUEENS = 5

def evalroutes(individual):
    size = len(individual)
    sum_=0
    for i in range(size-1):
      sum_=sum_+rutas[individual[i]][individual[i+1]]
    sum_=sum_+rutas[individual[size-1]][individual[0]]
    return sum_,


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

#Since there is only one queen per line, 
#individual are represented by a permutation
toolbox = base.Toolbox()
toolbox.register("permutation", random.sample, range(NB_QUEENS), NB_QUEENS)

#Structure initializers
#An individual is a list that represents the position of each queen.
#Only the line is stored, the column is the index of the number in the list.
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.permutation)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evalroutes)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=2.0/NB_QUEENS)
toolbox.register("select", tools.selTournament, tournsize=3)

def main(seed=0):
    random.seed(seed)

    pop = toolbox.population(n=10)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Avg", numpy.mean)
    stats.register("Std", numpy.std)
    stats.register("Min", numpy.min)
    stats.register("Max", numpy.max)

    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=100, stats=stats,
                        halloffame=hof, verbose=False)

    return pop, stats, hof

if __name__ == "__main__":
    pop, stats, hof = main()
    print(hof)


# A=0
# B=1
# C=2
# D=3
# E=4

# E-B-D-A-C

# 11+4+8+9=32

# +5= 37