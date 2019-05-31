from random import shuffle, randint, choice, sample, random
from deap import tools
import copy
from numpy import average

def to_homogeneous(individuo, criador_individuo): #transforma o individuo binário em homogenio
    homogeneous_ind = criador_individuo()
    for i in range(len(individuo)):
        if individuo[i] == 1:
            homogeneous_ind.append(i)
    homogeneous_ind.fitness = copy.copy(individuo.fitness)
    return homogeneous_ind


def to_homogeneous_pop(pop, criador_individuo):
    for i in range(len(pop)):
        pop.append(to_homogeneous(pop.pop(0), criador_individuo))
    return pop


def to_binary(individuo, criador_individuo, tam_ind):
    binary_ind = criador_individuo()
    for i in range(tam_ind):
        binary_ind.append(0)

    for i in range(len(individuo)):
        binary_ind[individuo[i]] = 1

    binary_ind.fitness = copy.copy(individuo.fitness)
    return binary_ind


def to_binary_pop(pop, criador_individuo, tam_ind):
    for i in range(len(pop)):
        pop.append(to_binary(pop.pop(0), criador_individuo, tam_ind))
    return pop


def scaled_roulette_wheel():
    # Ordenar individuos em um Ranking e fazer a seleção por roleta bazeado nesse rank
    pass


def fitness_adjustmen(pop_fitness, umin):
    umin = umin*-1+1
    for i in range(len(pop_fitness)):
        pop_fitness[i] = pop_fitness[i]+umin
    return pop_fitness


def fitness_linear_scaling(pop):
    C = 2
    pop_fitness = [a.fitness.wvalues[0] for a in pop]

    umin = min(pop_fitness)

    #if umin < 0:
    #    fitness_adjustmen(pop_fitness, umin)

    # Calculando Coeficientes ------------- #calculo tirado do livro do Goldberg - página 79

    uavg = average(pop_fitness)
    umin = min(pop_fitness)
    umax = max(pop_fitness)

    if umin > ((C*uavg-umax)/(C-1)):
        delta = umax - uavg
        a = (C - 1) * uavg / delta
        b = uavg * (umax - C*uavg) / delta
    else:
        delta = uavg - umin
        a = uavg / delta
        b = -umin * uavg / delta
    # -------------------------------------

    for i in range(len(pop)):
        pop[i].fitness.wvalues = individual_fitness_scaling(pop_fitness[i], a, b),

    return pop


def individual_fitness_scaling(fitness, a, b):
    return a*fitness + b

def random_mixing_crossover(pais, criador_individuo):
    shuffle(pais)
    centro = int(len(pais)/2)
    filhos = []
    for i in range(centro):
        filho1, filho2 = crossover(pais[i], pais[centro+i], criador_individuo)
        filhos.append(filho1)
        filhos.append(filho2)

    return filhos


def crossover(pai1, pai2, criador_individuo):
    menor_maximo = min(max(pai1), max(pai2))

    Int = []

    for i in range(menor_maximo):
        if pai1.__contains__(i) and pai2.__contains__(i):
            Int.append(i)

    if len(pai1) == len(Int) or len(pai2) == len(Int):
        filho1 = copia_ind(pai1, criador_individuo)
        filho2 = copia_ind(pai2, criador_individuo)
    else:
        menor_tam = min(len(pai1), len(pai2))-len(Int)
        j = randint(1, menor_tam)
        genes1 = get_subconjunto(pai1, Int, j)
        genes2 = get_subconjunto(pai2, Int, j)

        filho1 = criador_individuo()
        genes_copiados = 0
        for i in pai1:
            if genes1.__contains__(i):
               filho1.append(genes2[genes_copiados])
               genes_copiados += 1
            else:
                filho1.append(i)

        filho2 = criador_individuo()
        genes_copiados = 0
        for i in pai2:
            if genes2.__contains__(i):
                filho2.append(genes1[genes_copiados])
                genes_copiados += 1
            else:
                filho2.append(i)

    return filho1, filho2


def get_subconjunto(Individuo, Int, n): # pega n elementos de Individuo que não estejam em Int
    subconj = sample(Individuo, n)
    for i in range(len(subconj)):
        if Int.__contains__(subconj[i]):
            a = subconj[i]
            while(Int.__contains__(a) or subconj.__contains__(a)):
                a = choice(Individuo)
            subconj[i] = a
    return subconj


def random_pool_mutation(pop, p, tam_ind):
    for i in pop:
        if random() < p:
            mutation(i, tam_ind)
    return pop


def mutation(individuo, tam_ind):
    j = randint(1, min(len(individuo), tam_ind-len(individuo)))
    A = [i for i in range(0, tam_ind) if not individuo.__contains__(i)]
    individuo_indexes = sample(range(0, len(individuo)), j)
    A_indexes = sample(range(0, len(A)), j)
    for i in range(j):
        individuo[individuo_indexes[i]] = A[A_indexes[i]]
    return individuo


def copia_ind(individuo, criador_individuo, copy_f=False):
    novo = criador_individuo()

    for i in individuo:
        novo.append(i)

    if copy_f:
        novo.fitness = copy.deepcopy(individuo.fitness)

    return novo


def copia_pop(pop, criador_individuo, copy_f=False):
    nova_pop = []
    for i in pop:
        nova_pop.append(copia_ind(i, criador_individuo, copy_f))
    return nova_pop
