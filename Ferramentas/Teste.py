from Benchmark import Benchmark
from Algoritmos import TrangenicGA
from Algoritmos import Theory_Of_ChaosGA
from Algoritmos import GABasico
from Algoritmos import HomogeneousGA
from Algoritmos import FluidGA
import math
import numpy as np
import os
import matplotlib.pyplot as plt


class Teste:
    def __init__(self, num_testes, algoritmoGA, salvar):
        self.num = num_testes
        self.algoritmo = algoritmoGA
        self.salvar = salvar


    def config_basico(self, benchmark=Benchmark.rastrigin, tam_entradas=24, num_entradas=2, max_geracoes=100, populacao_inicial=100, prob_mut=0.2, prob_p_flip_bit=0.05, prob_p_cruz=0.5, tam_torneio=3):
        self.benchmark = benchmark
        self.tam_entradas = tam_entradas
        self.num_entradas = num_entradas
        self.max_geracoes = max_geracoes
        self.populacao_inicial = populacao_inicial
        self.prob_mut = prob_mut
        self.prob_p_flip_bit = prob_p_flip_bit
        self.prob_p_cruz = prob_p_cruz
        self.tam_torneio = tam_torneio

    def config_trans(self, benchmark=Benchmark.rastrigin, tam_entradas=24, num_entradas=2, max_geracoes=100, populacao_inicial=100, prob_mut=0.2, prob_p_flip_bit=0.05, prob_p_cruz=0.5, tam_torneio=3, fator_aprox_histo=0.0001):
        self.benchmark = benchmark
        self.tam_entradas = tam_entradas
        self.num_entradas = num_entradas
        self.max_geracoes = max_geracoes
        self.populacao_inicial = populacao_inicial
        self.prob_mut = prob_mut
        self.prob_p_flip_bit = prob_p_flip_bit
        self.prob_p_cruz = prob_p_cruz
        self.tam_torneio = tam_torneio
        self.fator_aprox_histo = fator_aprox_histo

    def config_chaos(self, benchmark=Benchmark.rastrigin, tam_entradas=32, num_entradas=2, max_geracoes=100, populacao_inicial=100, prob_mut=0.2, prob_p_flip_bit=0.05, tam_torneio=3):
        self.benchmark = benchmark
        self.tam_entradas = tam_entradas
        self.num_entradas = num_entradas
        self.max_geracoes = max_geracoes
        self.populacao_inicial = populacao_inicial
        self.prob_mut = prob_mut
        self.prob_p_flip_bit = prob_p_flip_bit
        self.tam_torneio = tam_torneio

    def run(self):
        if self.algoritmo == TrangenicGA.trangenicGA:
            melhor, geracao_f, Max, Avg, Min = self.algoritmo(self.benchmark, self.tam_entradas,
                                                              self.num_entradas, self.max_geracoes,
                                                              self.populacao_inicial, self.prob_mut,
                                                              self.prob_p_flip_bit, self.prob_p_cruz, self.tam_torneio,
                                                              self.fator_aprox_histo)
            print("melhor Individuo: " + str(melhor))
            print("Geração Final: " + str(geracao_f))
            self.plot(Max, "Fitness maximo", 'Gerações', 'Fitness')
            self.plot(Avg, "Média do Fitness", 'Gerações', 'Fitness')
            self.plot(Min, "Fitness mínimo", 'Gerações', 'Fitness')
        elif self.algoritmo == Theory_Of_ChaosGA.chaosGA:
            melhor, geracao_f, Max, Avg, Min = self.algoritmo(self.benchmark, self.tam_entradas, self.num_entradas,
                                                              self.max_geracoes, self.populacao_inicial, self.prob_mut,
                                                              self.prob_p_flip_bit, self.tam_torneio)
            print("melhor Individuo: " + str(melhor))
            print("Geração Final: " + str(geracao_f))
            self.plot(Max, "Fitness maximo", 'Gerações', 'Fitness')
            self.plot(Avg, "Média do Fitness", 'Gerações', 'Fitness')
            self.plot(Min, "Fitness mínimo", 'Gerações', 'Fitness')
        elif self.algoritmo == GABasico.GAbasico:
            melhor, geracao_f, Max, Avg, Min = self.algoritmo(self.benchmark, self.tam_entradas, self.num_entradas,
                                                              self.max_geracoes, self.populacao_inicial, self.prob_mut,
                                                              self.prob_p_flip_bit, self.prob_p_cruz, self.tam_torneio)
            print("melhor Individuo: " + str(melhor))
            print("Geração Final: " + str(geracao_f))
            self.plot(Max, "Fitness maximo", 'Gerações', 'Fitness')
            self.plot(Avg, "Média do Fitness", 'Gerações', 'Fitness')
            self.plot(Min, "Fitness mínimo", 'Gerações', 'Fitness')
        elif self.algoritmo == HomogeneousGA.homogeneousGA:
            melhor, geracao_f, Max, Avg, Min = self.algoritmo(self.benchmark, self.tam_entradas,
                                                              self.num_entradas, self.max_geracoes,
                                                              self.populacao_inicial, self.prob_mut,
                                                              self.prob_p_flip_bit, self.prob_p_cruz, self.tam_torneio,
                                                              self.fator_aprox_histo)
            print("melhor Individuo: " + str(melhor))
            print("Geração Final: " + str(geracao_f))
            self.plot(Max, "Fitness maximo", 'Gerações', 'Fitness')
            self.plot(Avg, "Média do Fitness", 'Gerações', 'Fitness')
            self.plot(Min, "Fitness mínimo", 'Gerações', 'Fitness')
        elif self.algoritmo == FluidGA.FluidGA:
            melhor, geracao_f, Max, Avg, Min = self.algoritmo(self.tam_entradas, self.num_entradas,
                                                              self.max_geracoes, self.populacao_inicial, self.prob_mut,
                                                              self.prob_p_flip_bit, self.prob_p_cruz, self.tam_torneio)
            print("melhor Individuo: " + str(melhor))
            print("Geração Final: " + str(geracao_f))
            self.plot(Max, "Fitness maximo", 'Gerações', 'Fitness')
            self.plot(Avg, "Média do Fitness", 'Gerações', 'Fitness')
            self.plot(Min, "Fitness mínimo", 'Gerações', 'Fitness')
        return melhor, geracao_f, Max, Avg, Min

    def teste(self):
        melhores = []
        geracoes_finais = []
        nao_convergidos = 0
        for i in range(self.num):
            print('Fazendo Teste Número ({})'.format(i))
            if(self.algoritmo == TrangenicGA.trangenicGA):
                melhor, geracao_f, Max, Avg, Min = self.algoritmo(self.benchmark, self.tam_entradas,
                                                                  self.num_entradas, self.max_geracoes,
                                                                  self.populacao_inicial, self.prob_mut,
                                                                  self.prob_p_flip_bit, self.prob_p_cruz,
                                                                  self.tam_torneio, self.fator_aprox_histo)
                melhores.append(melhor)
                geracoes_finais.append(geracao_f)
                if geracao_f == self.max_geracoes:
                    nao_convergidos = nao_convergidos + 1
                titulo, eixo_x_M, eixo_y_M , eixo_x_G, eixo_y_G= 'Transgenic GA with ' + Benchmark.info(self.benchmark)[4], 'Number of the Test', 'Evaluation of the Best Individual', 'Number of the Test', 'Final Generation'
            elif self.algoritmo == Theory_Of_ChaosGA.chaosGA:
                melhor, geracao_f, Max, Avg, Min = self.algoritmo(self.benchmark, self.tam_entradas, self.num_entradas,
                                                                  self.max_geracoes, self.populacao_inicial,
                                                                  self.prob_mut, self.prob_p_flip_bit, self.tam_torneio)
                melhores.append(melhor)
                geracoes_finais.append(geracao_f)
                if geracao_f == self.max_geracoes:
                    nao_convergidos = nao_convergidos + 1
                titulo, eixo_x_M, eixo_y_M, eixo_x_G, eixo_y_G = 'Theory of Chaos GA with ' + Benchmark.info(self.benchmark)[4], 'Number of the Test', 'Evaluation of the Best Individual', 'Number of the Test', 'Final Generation'
            elif self.algoritmo == GABasico.GAbasico:

                melhor, geracao_f, Max, Avg, Min = self.algoritmo(self.benchmark, self.tam_entradas, self.num_entradas,
                                                              self.max_geracoes, self.populacao_inicial, self.prob_mut,
                                                              self.prob_p_flip_bit, self.prob_p_cruz, self.tam_torneio)
                melhores.append(melhor)
                geracoes_finais.append(geracao_f)
                if geracao_f == self.max_geracoes:
                    nao_convergidos = nao_convergidos + 1
                titulo, eixo_x_M, eixo_y_M, eixo_x_G, eixo_y_G = 'Basic GA with ' + Benchmark.info(self.benchmark)[4], 'Number of the Test', 'Evaluation of the Best Individual', 'Number of the Test', 'Final Generation'
            elif self.algoritmo == HomogeneousGA.homogeneousGA:
                melhor, geracao_f, Max, Avg, Min = self.algoritmo(self.benchmark, self.tam_entradas,
                                                                  self.num_entradas, self.max_geracoes,
                                                                  self.populacao_inicial, self.prob_mut,
                                                                  self.prob_p_flip_bit, self.prob_p_cruz,
                                                                  self.tam_torneio, self.fator_aprox_histo)
                melhores.append(melhor)
                geracoes_finais.append(geracao_f)
                if geracao_f == self.max_geracoes:
                    nao_convergidos = nao_convergidos + 1
                titulo, eixo_x_M, eixo_y_M , eixo_x_G, eixo_y_G= 'Transgenic GA with ' + Benchmark.info(self.benchmark)[4], 'Number of the Test', 'Evaluation of the Best Individual', 'Number of the Test', 'Final Generation'
            elif self.algoritmo == FluidGA.FluidGA:
                melhor, geracao_f, Max, Avg, Min = self.algoritmo(self.benchmark, self.tam_entradas, self.num_entradas,
                                                                  self.max_geracoes, self.populacao_inicial, self.prob_mut,
                                                                  self.prob_p_flip_bit, self.prob_p_cruz, self.tam_torneio)
                melhores.append(melhor)
                geracoes_finais.append(geracao_f)
                if geracao_f == self.max_geracoes:
                    nao_convergidos = nao_convergidos + 1
                titulo, eixo_x_M, eixo_y_M, eixo_x_G, eixo_y_G = 'Basic GA with ' + Benchmark.info(self.benchmark)[4], 'Number of the Test', 'Evaluation of the Best Individual', 'Number of the Test', 'Final Generation'
        dir = 'Test - ' + titulo
        if self.salvar:
            dir = criar_dir(dir)
            self.salvar_resultados_teste(dir, titulo, melhores, geracoes_finais, Max, Avg, Min,nao_convergidos)
        self.plot(melhores, "Best Individuals - " + titulo, eixo_x_M, eixo_y_M, self.salvar, dir)
        self.plot(geracoes_finais, "Final Generations - " + titulo, eixo_x_G, eixo_y_G, self.salvar, dir)
        return melhores, geracoes_finais, nao_convergidos


    def plot(self, list, titulo, titulo_x, titulo_y, salvar = False, dir = ''):
        x = [i for i in range(1, len(list)+1)]
        plt.plot(x, list)
        plt.title(titulo)
        plt.xlabel(titulo_x)
        plt.ylabel(titulo_y)
        if salvar:
            print('Imagem Salva em: ' + dir + '/' + titulo + '.pdf')
            plt.savefig(dir + '/' + titulo + '.pdf')
        plt.show()

    def salvar_resultados_teste(self, dir, titulo, melhores, geracoes_finais, Max, Avg, Min, nao_convergidos):
        file = open(dir + '/' + titulo + '.txt', 'w')
        file.write('Resultados do Teste: ' + titulo + '\n')

        file.write('\nAtributos do Teste: \n')
        file.write('    Benchmark = ' + Benchmark.info(self.benchmark)[4] + '\n')
        file.write('    Número de Testes = ' + str(self.num) + '\n')
        file.write('    Número de Testes não convergidos= ' + str(nao_convergidos) + '\n')

        Media, dp, va = media(melhores)
        file.write('\nMelhores Individuos: \n')
        file.write('    ' + str(melhores) + '\n')
        file.write('    Media = ' + str(Media) + '\n')
        file.write('    Desvio Padrão = ' + str(dp) + '\n')
        file.write('    Variância = ' + str(va) + '\n')
        Media, dp, va = media(geracoes_finais)
        file.write('\nGerações Finais: \n')
        file.write('    ' + str(geracoes_finais) + '\n')
        file.write('    Media = ' + str(Media) + '\n')
        file.write('    Desvio Padrão = ' + str(dp) + '\n')
        file.write('    Variância = ' + str(va) + '\n')
        file.close()


        print('Arquivo Salvo em: ' + dir + '/' + titulo + '.txt')

def media(list):
    media = np.sum(list)/float(len(list))
    desv = 0
    for i in range(len(list)):
        desv = desv + ((list[i] - media)*(list[i] - media))
    var = desv/float(len(list))
    desv = math.sqrt(var)
    return media, desv, var

def criar_dir(dir):
    repetir = True
    add = ''
    i = 1
    while repetir:
        repetir = False
        try:
            os.mkdir(dir+add)
        except Exception:
            add = ' - ' + str(i)
            i += 1
            repetir = True
    return dir+add

def func_testTrans(list_entradas):
    list_entradas[0] = 5 * list_entradas[0]
    list_entradas[4] = 50 * list_entradas[4]
    list_entradas[5] = 5 * list_entradas[5]
    a = Teste.Teste(10, TrangenicGA.trangenicGA)
    a.config_trans(config=int(list_entradas[0]), benchmark=Benchmark.rastrigin, tam_entradas=24, num_entradas=2,
                    max_geracoes=250, populacao_inicial=100, prob_mut=list_entradas[1],
                    prob_p_flip_bit=list_entradas[2], prob_p_cruz=list_entradas[3],
                    tam_torneio=int(list_entradas[4]), fator_aprox_histo=list_entradas[5])
    return sum(a.teste())