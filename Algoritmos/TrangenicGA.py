from Benchmark import Benchmark
import random
from deap import base
from deap import creator
from deap import tools
from Operadores import Trangenic
import numpy as np
from Ferramentas.Finaliza_evolucao import finaliza_evolucao

def trangenicGA(benchmark = Benchmark.rastrigin, tam_entradas=24, num_entradas=2, max_geracoes=250, populacao_inicial=100, prob_mut=0.2, prob_p_flip_bit=0.05, prob_p_cruz=0.5, tam_torneio=3, fator_aprox_histo=0.0001):

    lim_min, lim_max, pesos, solucoes, str_benchmark= Benchmark.info(benchmark)

    creator.create("avaliacao", base.Fitness, weights=pesos)  ##setando objetivo das avaliacoes

    creator.create("Individuo", list, fitness=creator.avaliacao)  ##Criando tipo de Individuos

    toolbox = base.Toolbox()  ## Instanciando objeto Toolbox

    toolbox.register("ini_gene", random.randint, 0, 1)  ## registrando ferramenta para pegar bit ramdomico (0 ou 1)

    tam = tam_entradas*num_entradas

    toolbox.register("individuo", tools.initRepeat, creator.Individuo, toolbox.ini_gene, tam)  ## registrando ferramenta para criar individuo com 48 bits apartir da ferramenta "ini_gene"

    toolbox.register("populacao", tools.initRepeat, list,toolbox.individuo)  ##registrando ferramenta para criar populacao com base na ferramenta "individuo"

    indiv = Benchmark.Benchmark(num_entradas, tam_entradas, lim_min, lim_max, benchmark)  ##Instanciando Objeto para Benchmark

    toolbox.register("avaliacao",indiv.fitness)  ##registrando ferramenta para avaliar com base na nossa função fitness do Objeto Benchmark

    toolbox.register("crusar", tools.cxTwoPoint)  ##registrando ferramenta para crusar dois individuos

    toolbox.register("mutar", tools.mutFlipBit,indpb=prob_p_flip_bit)  ##registrando ferramenta para mutar individuos com chance de mutação de 5%

    toolbox.register("selecionar", tools.selTournament,tournsize=tam_torneio)  ##registrando ferramenta para selecionar pais em um torneio.

    toolbox.register("selecao_elitista", tools.selBest) ##registrando ferramenta para selecionar pais de forma totalmente elitista.

    historico = Trangenic.Historico(tam, pesos, fator_aprox_histo)

    if sum(solucoes) > 0 and sum(pesos) < 0 or sum(solucoes) < 0 and sum(pesos) > 0:
       solucoes = np.multiply(solucoes, -1)

    return run_trangenicGA(toolbox, prob_mut, prob_p_cruz, populacao_inicial, historico, max_geracoes, pesos, sum(np.multiply(solucoes, pesos)))

def run_trangenicGA(toolbox, prob_mut, prob_p_cruz, populacao_inicial, historico, max_ger, pesos, solucao):
    MaxList = []
    AvgList = []
    MinList = []

    pop = toolbox.populacao(n=populacao_inicial)

    cont_repet = None#Ferramentas.repet(5)

    for x in pop:
        x.fitness.values = toolbox.avaliacao(x)

    g = 0

    while not finaliza_evolucao(0, max_ger, cont_repet, pesos, pop, solucao, g):
        g = g + 1

        #print("-- Geração %i --" % g)


        pais = Trangenic.trangenic(pop, historico, toolbox.avaliacao, toolbox.clone)

        pais = toolbox.selecionar(pais, int(len(pop)/2))

        pais = list(map(toolbox.clone, pais))

        for filho1, filho2 in zip(pais[::2], pais[1::2]):

            if random.random() < prob_p_cruz:
                toolbox.crusar(filho1, filho2)

                del filho1.fitness.values
                del filho2.fitness.values

        pais += toolbox.selecao_elitista(pop, int(len(pop)/2))

        for mutante in pais:

            if random.random() < prob_mut:
                toolbox.mutar(mutante)
                del mutante.fitness.values


        for ind in pais:
                ind.fitness.values = toolbox.avaliacao(ind)


        pop[:] = pais

        Aval = [ind.fitness.values[0] for ind in pop]

        tam = len(pop)
        media = sum(Aval) / tam
        sum2 = sum(x * x for x in Aval)
        std = abs(sum2 / tam - media ** 2) ** 0.5

        maxAval = max(Aval)
        MaxList.append(maxAval)
        AvgList.append(media)
        MinList.append(min(Aval))
        #print("  menor %s" % min(Aval))
        #print("  maior %s" % maxAval)
        #print("  media %s" % media)
        #print("  Std %s" % std)

    #print("-- final da evolução --")

    melhor = tools.selBest(pop, 1)[0]

    #print("Melhor individuo é %s; \n Avaliação: %s;" % (melhor, melhor.fitness.values[0]))

    return sum(melhor.fitness.values), g, MaxList, AvgList, MinList
