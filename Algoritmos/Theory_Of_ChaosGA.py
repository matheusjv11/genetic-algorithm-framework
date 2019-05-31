import random
import numpy as np
from deap import base
from deap import creator
from deap import tools
from Benchmark import Benchmark
from Operadores import Theory_Of_Chaos
from Ferramentas.Finaliza_evolucao import finaliza_evolucao


def chaosGA( benchmark = Benchmark.rastrigin, tam_entradas = 32, num_entradas=2, max_geracoes=100, populacao_inicial=100, prob_mut=0.2, prob_p_flip_bit=0.05, tam_torneio=3):


    lim_min, lim_max, pesos, solucoes, str_benchmark = Benchmark.info(benchmark)

    creator.create("avaliacao", base.Fitness, weights=pesos)  ##setando objetivo das avaliacoes

    creator.create("Individuo", list, fitness=creator.avaliacao)  ##Criando tipo de Individuos

    toolbox = base.Toolbox()  ## Instanciando objeto Toolbox

    toolbox.register("ini_gene", random.randint, 0, 1)  ## registrando ferramenta para pegar bit ramdomico (0 ou 1)

    tam = tam_entradas*num_entradas*2+6

    toolbox.register("individuo", tools.initRepeat, creator.Individuo, toolbox.ini_gene, tam)  ## registrando ferramenta para criar individuo com 48 bits apartir da ferramenta "ini_gene"

    toolbox.register("populacao", tools.initRepeat, list,toolbox.individuo)  ##registrando ferramenta para criar populacao com base na ferramenta "individuo"

    indiv = Benchmark.Benchmark(num_entradas, tam_entradas, lim_min, lim_max, benchmark)  ##Instanciando Objeto para Benchmark

    toolbox.register("avaliacao",indiv.fitness)  ##registrando ferramenta para avaliar com base na nossa função fitness do Objeto Benchmark

    toolbox.register("crusar", tools.cxTwoPoint)  ##registrando ferramenta para crusar dois individuos

    toolbox.register("mutar", tools.mutFlipBit,indpb=prob_p_flip_bit)  ##registrando ferramenta para mutar individuos com chance de mutação de 5%

    toolbox.register("selecionar", tools.selTournament,tournsize=tam_torneio)  ##registrando ferramenta para selecionar pais em um torneio.



   # toolbox.register("mutar", tools.mutFlipBit, prob_p_flip_bit)

   # toolbox.register("selecionar", tools.selTournament, tam_torneio)

    toolbox.register("selecao_elitista",tools.selBest)  ##registrando ferramenta para selecionar pais de forma totalmente elitista.

    if sum(solucoes) > 0 and sum(pesos) < 0 or sum(solucoes) < 0 and sum(pesos) > 0:
       solucoes = np.multiply(solucoes, -1)

    return run_chaos(toolbox,prob_mut, populacao_inicial, max_geracoes,num_entradas, pesos, sum(np.multiply(solucoes, pesos)))

def run_chaos(toolbox,prob_mut, populacao_inicial, max_geracoes, num_entradas, pesos, solucao):

    MaxList = []
    AvgList = []
    MinList = []

    Melhor_da_geracao = None
    repeticao = 0
    pop = toolbox.populacao(populacao_inicial)

    cont_repet = None  # Ferramentas.repet(5)

    tamanho_mutacao = int(((len(pop[0]) - 6) / 2) + 6)

    Avaliacoes = list(map(toolbox.avaliacao, pop))

    for x, y in zip(pop, Avaliacoes):
        x.fitness.values = y

    lamba = [1,1,0,1,0,0]

    Aval = [x.fitness.values[0] for x in pop]

    #Aqui é feita a aplicação do mesmo lambda em toda a população

    for x in range (0,len(pop)):
      posicao = tamanho_mutacao-6
      for y in range (0,len(lamba)):
           pop[x][posicao]= lamba[y]
           posicao+=1

    g = 0
    while not finaliza_evolucao(0, max_geracoes, cont_repet, pesos, pop, solucao, g):

        g = g + 1


        #print("-- Geração %i --" % g)

        #Aqui separa a populacao em elitista para passar para a nova geracao e os selecionados pelo round para procriar
        paisCROSSOVER = toolbox.selecionar(pop, int(len(pop)/2))
        #paisCROSSOVER = pop[:49]
        pais = toolbox.selecao_elitista(pop, int(len(pop)/2))




        #Aqui passa os pais para o crossover com a teoria do caos

        pais += Theory_Of_Chaos.crossover(paisCROSSOVER,num_entradas)



        #pai mutante recebe so o DNA que deve sofrer mutação, ou seja, nao contem a mascara e nem o lambda

        paisMUTANTES = []

        for x in range(0,len(pais)):

            paisMUTANTES.append(pais[x][:tamanho_mutacao-6])

        #Aqui ocorre o processo de mutacao

        for m in range(0,len(paisMUTANTES)):

            if random.random() < 0.2:
                toolbox.mutar(paisMUTANTES[m])
                del pais[m].fitness.values

        #Aqueles pais que foram mutados, voltam para 'pais' com seu novo DNA

        for x in range(0,len(pais)):

            if not pais[x].fitness.valid:

                for y in range(0,tamanho_mutacao-6):
                    pais[x][y] = paisMUTANTES[x][y]

        Avaliacoes = map(toolbox.avaliacao, pais)

        for ind, aval in zip(pais, Avaliacoes):
            ind.fitness.values = aval


        pop[:] = pais

        Aval = [ind.fitness.values[0] for ind in pop]

        tam = len(pop)
        media = sum(Aval) / tam
        sum2 = sum(x * x for x in Aval)
        std = abs(sum2 / tam - media ** 2) ** 0.5



        MaxList.append(max(Aval))
        AvgList.append(media)
        MinList.append(min(Aval))

        # Criterio de parada por repeticao de melhor individuo
        if Melhor_da_geracao == min(Aval):
            repeticao+=1
        else:
             repeticao=0

        #print("  menor %s" % min(Aval))

        Melhor_da_geracao=min(Aval)
        #print("  maior %s" % max(Aval))
        #print("  media %s" % media)
        #print("  Std %s" % std)
        melhor = tools.selBest(pop, 1)[0]
        lambdaBIN = melhor[tamanho_mutacao-6:tamanho_mutacao]
        lambdaINTERVALO = (4/((2**6)-1))*int("".join(str(i) for i in lambdaBIN), 2)
        #print("  Lambda do melhor : %s" % lambdaINTERVALO)
        #if repeticao == 10 :
            #print("Nao chegou na soulucao")
            #break

    #print("-- final da evolução --")

    melhor = tools.selBest(pop, 1)[0]
    #print("Melhor individuo é %s; \nAvaliação: %s;" % (melhor, melhor.fitness.values))

    return sum(melhor.fitness.values), g, MaxList, AvgList, MinList

