import numpy as np
import random
from copy import deepcopy

class Gene:
    def __init__(self):
        self.gene = 0
        self.qty = 0

    def get_gene(self):
        return self.gene


    def set_gene(self, i):
        self.gene = i

    def add(self):
        self.qty += 1

    def update(self, g):
        if g == self.gene:
            self.qty += 1
        else:
            self.reset(g)

    def reset(self, g):
        self.gene = g
        self.qty = 0

class Historico:

    def __init__(self, tam, pesos, fator_aprox = 0.1):
        self.tam = tam
        self.pesos = pesos
        self.fator = fator_aprox
        self.fit = None
        self.table = [Gene() for i in range(self.tam)]

    def __getitem__(self, item):
        if item == self.tam:
            return self.fit
        return self.table[item]

    def __setitem__(self, key, value):
        if key == self.tam:
            self.fit = value
        gene = self.table[key]
        gene.reset(value)

    def fitness(self):
        return self.fit

    def update(self, pop):
        maior_fit = sum(np.multiply(pop[0].fitness.values, self.pesos))
        maior = pop[0]

        #pega individuo como maior fitness
        for i in range(1, len(pop)):
            fit_temp = sum(np.multiply(pop[i].fitness.values, self.pesos))
            if fit_temp > maior_fit:
                maior = pop[i]
                maior_fit = fit_temp

        if self.fit is None or maior_fit > self.fit:
            self.reset(maior_fit, maior)
        for i in pop:
            if sum(np.multiply(i.fitness.values, self.pesos)) > self.fit - self.fator:
                self.add_to_his(i)


    def reset(self, fit, ind):
        self.fit = fit
        for i in range(len(ind)):
            if ind[i] != self.table[i].get_gene():
                self.table[i].reset(ind[i])

    def add_to_his(self, ind):
        for i in range(len(ind)):
            if ind[i] == self.table[i].get_gene():
                self.table[i].add()

    def get_ocorrencias(self):
        ocorrencias = []
        for i in self.table:
            ocorrencias.append(i.qty)
        return ocorrencias

def trangenic(pop, historico, funcao_aval, clone):
        historico.update(pop)
        m1 = clone(pop)
        m2 = clone(pop)
        m3 = clone(pop)
        m4 = clone(pop)
        #print([i.qty for i in historico.table])


        ocorrencias = historico.get_ocorrencias()
        inserir_genes(m1, selecionar(1, ocorrencias), historico)
        inserir_genes(m2, selecionar(2, ocorrencias), historico)
        inserir_genes(m3, selecionar(3, ocorrencias), historico)
        inserir_genes(m4, selecionar(4, ocorrencias), historico)

        trang_pop = []
        trang_pop += m1
        trang_pop += m2
        trang_pop += m3
        trang_pop += m4


        for i in range(len(trang_pop)):
            trang_pop[i].fitness.values = funcao_aval(trang_pop[i])

        """
        pesos = pop[0].fitness.weights
        aval = [abs(sum(np.multiply(ind.fitness.values, pesos))) for ind in trang_pop]
        selecionados = selecionar(len(pop), aval)

        nova_pop = []
        for i in selecionados:
            nova_pop.append(trang_pop[i])

        return nova_pop
        """
        return trang_pop


def inserir_genes(pop, genes, historico):
    for ind in pop:
        for i in genes:
            ind[i] = historico.table[i].get_gene()


def selecionar(num, ocorrencias):
    selecionados = []
    for i in range(num):
        selecionados.append(roleta_proporcional(ocorrencias))
    return selecionados


def roleta_proporcional(ocorrencias):
    max = sum(ocorrencias)
    escolha = random.uniform(0, max)
    atual = 0
    for i in range(len(ocorrencias)):
            atual += ocorrencias[i]
            if atual >= escolha:
                return i