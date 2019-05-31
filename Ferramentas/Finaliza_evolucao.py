import numpy as np

finaliza_por_maximo_geracoes = 0
finaliza_por_maximo_repeticoes = 1
finaliza_por_qualquer_motivo = 2

class repet:
    def __init__(self, max_repet):
        self.num_repet = 0
        self.ultimo_result = 0
        self.max_repet = max_repet

    def finaliza_repet(self, pesos, pop, solucao):
        novo_result = abs(max([sum(np.multiply(x.fitness.values, pesos)) for x in pop]) - solucao)
        if novo_result >= self.ultimo_result:
            self.num_repet += 1
            if self.num_repet >= self.max_repet:
                print('Finalizado por repetições')
                return True
            else:
                self.ultimo_result = novo_result
                return False
        else:
            self.num_repet = 0
            return False




def finaliza_evolucao(tipo, max_generation, cont_repet, pesos, pop, solucao, g):
    if tipo == 0:
        return finaliza_max_geracoes(pesos, pop, solucao, g, max_generation)
    elif tipo == 1:
        return finaliza_max_repet(pesos, pop, solucao, cont_repet)
    else:
        pass

def finaliza_max_geracoes(pesos, pop, solucao, g, max_ger):
    if achou_solucao(pesos, pop, solucao) or g >= max_ger:
        return True
    else:
        return False

def finaliza_max_repet(pesos, pop, solucao, cont_repet):
    if achou_solucao(pesos, pop, solucao) or cont_repet.finaliza_repet(pesos, pop, solucao):
        return True
    else:
        return False

def achou_solucao(pesos, pop, solucao):
    if abs(max([sum(np.multiply(x.fitness.values, pesos)) for x in pop]) - solucao) < 0.001:
        return True
    else:
        return False