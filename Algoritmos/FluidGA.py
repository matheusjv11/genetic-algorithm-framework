from Benchmark import Benchmark
import random
from Operadores import Fluid
from deap import base
from deap import creator
from deap import tools
from copy import deepcopy

def FluidGA(benchmark = Benchmark.rastrigin, tam_entradas=24, num_entradas=2, max_geracoes=250, populacao_inicial=100, prob_mut=0.2, prob_p_flip_bit=0.05, prob_p_cruz=0.5, tam_torneio=3):

    lim_min, lim_max, pesos, solucoes, str_benchmark = Benchmark.info(benchmark)

    creator.create("avaliacao", base.Fitness, weights=pesos)  ##setando objetivo das avaliacoes ###

    creator.create("Individuo", list, fitness=creator.avaliacao)  ##Criando tipo de Individuos
#
    toolbox = base.Toolbox()  ## Instanciando objeto Toolbox

    toolbox.register("ini_gene", random.randint, 0,1)  ## registrando ferramenta para pegar bit ramdomico (0 ou 1)

    tam = tam_entradas*num_entradas

    toolbox.register("individuo", tools.initRepeat, creator.Individuo, toolbox.ini_gene, tam)  ## registrando ferramenta para criar individuo com 48 bits apartir da ferramenta "ini_gene"

    toolbox.register("populacao", tools.initRepeat, list, toolbox.individuo)  ##registrando ferramenta para criar populacao com base na ferramenta "individuo"

    indiv = Benchmark.Benchmark(num_entradas, tam_entradas, lim_min, lim_max, benchmark)  ##Instanciando Objeto para Benchmark

    toolbox.register("avaliacao", indiv.fitness)  ##registrando ferramenta para avaliar com base na nossa função fitness do Objeto Benchmark

    #toolbox.register("crusar", tools.cxTwoPoint)  ##registrando ferramenta para crusar dois individuos

    #toolbox.register("mutar", tools.mutFlipBit, indpb=prob_p_flip_bit)  ##registrando ferramenta para mutar individuos com chance de mutação de 5%

    toolbox.register("selecionar", tools.selTournament, tournsize=tam_torneio)  ##registrando ferramenta para selecionar pais em um torneio.

    toolbox.register("selecao_elitista", tools.selBest)  ##registrando ferramenta para selecionar pais de forma totalmente elitista.

    return run_Fluid(toolbox, populacao_inicial, max_geracoes, pesos, solucoes, tam)

def run_Fluid(toolbox, populacao_inicial, max_ger, pesos, solucao,tam):

    MaxList = []
    AvgList = []
    MinList = []



    pop = toolbox.populacao(n=populacao_inicial)


    # Setando as probabilidades aleatorias para a primeira geração
    for x in range(0, len(pop)):
        for y in range(0,len(pop[0])):
            #pop[x][y] = round(random.randint(0, 100)/100,2)
            pop[x][y] = 0.5

    # Seta a primeira geração do blueprint, que terá todas as celulas com 50% de probabilidade
    blueprint = deepcopy(pop[0])

    for x in range (0,tam):
        blueprint[x]= 0.5


    #Chamando a função para gerar os individuos de primeira geração a partir da probabilidade
    pop = Fluid.BornAnIndividual(pop, tam)
    #Essa função serve para organizar o individuo, trazendo resposta de benchmark para os primeiros indices
    pop = Fluid.ChangePlace(pop)


    for x in pop:
        x.fitness.values = toolbox.avaliacao(x)

    g = 0

    while min([x.fitness.values[0] for x in pop]) > 0.001 and g < max_ger:

        g = g + 1

        #print("-- Geração %i --" % g)

        # Aqui ira selecionar os pais pelo round
        paisCROSSOVER = toolbox.selecionar(pop, int(len(pop) / 1.25))

        # A proxima geração, contara com os melhores individuos da antiga geração
        pais = toolbox.selecao_elitista(pop, int(len(pop) / 5))


        # Aqui passa os pais para o crossover usando o metodo fluid
        pais += Fluid.Crossover(paisCROSSOVER,tam,blueprint)

        blueprint = Fluid.NewBlueprint(blueprint,pais,tam)




        ##Aval = [ind.fitness.values[0] for ind in pop]
        #for x in pop:
       #     x.fitness.values = toolbox.avaliacao(x)

        Avaliacoes = map(toolbox.avaliacao, pais)

        for ind, aval in zip(pais, Avaliacoes):
            ind.fitness.values = aval

        pop[:] = pais

        Aval = [ind.fitness.values[0] for ind in pop]

        tamanho = len(pop)
        media = sum(Aval) / tamanho
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

    print("-- final da evolução --")
    print("-- Geração final : %i --" % g)
    melhor = tools.selBest(pop, 1)[0]

    print("Melhor individuo é %s; \n Avaliação: %s;" % (melhor, melhor.fitness.values[0]))

    #return sum(np.multiply(melhor.fitness.values, pesos)), g, MaxList, AvgList, MinList

if __name__ == '__main__':
    FluidGA()