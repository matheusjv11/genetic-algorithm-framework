import numpy as np
#from Algoritmos import TrangenicGA
#from Algoritmos import Teste

class Benchmark:

    def __init__(self, num_entradas, tam_cada_entrada, lim_min, lim_max, funcao_benchmark):
        self.num = num_entradas
        self.tam = tam_cada_entrada
        self.min = lim_min
        self.max = lim_max
        self.funcao = funcao_benchmark

    def bin_to_entradas(self, individuo):

        escopo = self.max - self.min

        fator = escopo /(2**self.tam - 1)

        entradas = []
        ini = 0
        fim = self.tam
        for i in range(self.num):
            entradas.append(int("".join(str(i) for i in individuo[ini: fim]), 2))
            ini += self.tam
            fim += self.tam

        for i in range(self.num):
            entradas[i] = (entradas[i] * fator) + self.min

        return entradas

    def fitness(self, individuo):
        return self.funcao(self.bin_to_entradas(individuo))

def rastrigin(list_entradas):
    soma = 10 * len(list_entradas)
    for i in range(len(list_entradas)):
        soma += list_entradas[i] ** 2 - (10 * np.cos(2 * np.pi * list_entradas[i]))
    return soma,




def ackley(list_entradas):
    soma1 = 0.0
    soma2 = 0.0
    for x in list_entradas:
        soma1 += x ** 2.0
        soma2 += np.cos(2.0 * np.pi * x)
    n = float(len(list_entradas))
    return -20.0 * np.exp(-0.2 * np.sqrt(soma1 / n)) - np.exp(soma2 / n) + 20 + np.e,


def keane(list_entradas):
    x = list_entradas[0]
    y = list_entradas[1]

    soma1 = ((np.sin(x - y)) ** 2) * ((np.sin(x + y)) ** 2)
    soma2 = np.sqrt((x ** 2) + (y ** 2))
    soma1 = -1.0 * (np.divide(soma1, soma2))

    return soma1,


def shubert(list_entradas):
    produto = 1.0
    for i in list_entradas:
        soma = 0.0
        for j in range(1, 6):
            soma = soma + (j * np.cos(((j + 1) * i) + j))
        produto = produto * soma
    return produto,


def shubert3(list_entradas):
    total = 0.0

    for i in list_entradas:
        soma = 0.0
        for j in range(1, 6):
            soma = soma + (j * np.sin((j + 1) * i + j))
        total = soma + total
    return total,


def schaffer(list_entradas):
    x1 = list_entradas[0]
    x2 = list_entradas[1]

    soma1 = ((np.sin(x1 * x1 - x2 * x2) ** 2) - 0.5)
    soma2 = (1 + 0.001 * (x1 * x1 + x2 * x2)) ** 2

    return 0.5 + (soma1 / soma2),


def info(benchmark):
    if benchmark == rastrigin or benchmark == 0 or benchmark == "Rastrigin":
        return -5.12, 5.12, (-1.0,), (0,), 'Rastrigin'
    if benchmark == ackley or benchmark == 1 or benchmark == "Ackley":
        return -32.0, 32.0, (-1.0,), (0,), 'Ackley'
    if benchmark == keane or benchmark == 2 or benchmark == "Keane":
        return -10.0, 10.0, (-1.0,), (-0.673667521146855,), 'Keane'
    if benchmark == shubert or benchmark == 3 or benchmark == "Shubert":
        return -10.0, 10.0, (-1.0,), (-186.7309,), 'Shubert'
    if benchmark == shubert3 or benchmark == 4 or benchmark == "Shubert3":
        return -10.0, 10.0, (-1.0,), (-29.6733337,), 'Shubert3'
    if benchmark == schaffer or benchmark == 5 or benchmark == "Schaffer":
        return -100, 100, (-1.0,), (0,), 'Schaffer'
    if benchmark == schaffer or benchmark == 5 or benchmark == "Schaffer":
        return -100, 100, (-1.0,), (0,), 'Schaffer'
    return 0, 1, (-1), (0,)
