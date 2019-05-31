import matplotlib.pyplot as plt
from Benchmark import Benchmark
import numpy as np
import math
import os

def plot(matriz, legends, benchmark = None ,titulo = '', titulo_x = '', titulo_y = '', salvar = False, limites = (0, 0), dir = ''):
    x = [i for i in range(1, len(matriz[0])+1)]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, matriz[0], '-.o', label=legends[0])
    plt.plot(x, matriz[1], ':x', label=legends[1])
    plt.plot(x, matriz[2], '--', label=legends[2])

    lgd = plt.legend(loc=2, borderaxespad=0., bbox_to_anchor=(1.05, 1))
    plt.title(titulo)
    plt.xlabel(titulo_x)
    plt.ylabel(titulo_y)

    ax.set_ylim(Benchmark.info(benchmark)[3][0]+limites[0], Benchmark.info(benchmark)[3][0]+limites[1])
    if salvar:
        plt.savefig(dir + titulo + '.pdf')
        plt.savefig(dir + titulo + '.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.show()

def salvar_resultados(titulo, entrada, GAs ,benchmark, dir = ''):
    dir = criar_dir(dir + 'Test - ' + titulo)
    file = open(dir + '/' + titulo + '_info' + '.csv', 'w')
    file.write('Resultados do Teste:, ' + titulo + '\n')

    file.write('\nAtributos do Teste: \n')
    file.write('Benchmark ,' + Benchmark.info(benchmark)[4] + '\n')
    file.write('Número de Testes ,' + str(len(entrada[0])) + '\n')

    file.write('\n\nAlgoritimo, Média, Desvio Padrão, Variância\n')
    for i in range(len(entrada)):
        med, desv, var = media(entrada[i])
        file.write(str(GAs[i]) + ',' + str(med) + ',' + str(desv) + ',' + str(var) + '\n')

    file.close()

    print('Arquivo Salvo em: ' + dir + '/' + titulo + '_info' + '.csv')

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


def media(list):
    media = np.sum(list)/float(len(list))
    desv = 0
    for i in range(len(list)):
        desv = desv + ((list[i] - media)*(list[i] - media))
    var = desv/float(len(list))
    desv = math.sqrt(var)
    return media, desv, var
