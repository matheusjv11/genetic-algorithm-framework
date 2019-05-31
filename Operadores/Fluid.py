import random
from copy import deepcopy

def BornAnIndividual(cromossomos,tam):

    # Aqui ira gerar os individuos apartir das probabilidades
    # Ele sera inserido na mesma tupla das probabilidades
    # O que ira separar sera o tamanho do individuo original, ate o determinado tamanho, sera probabilidade, apartir disso, sera individuo

    tamanhoSOLUTION = tam

    for x in range(0, len(cromossomos)):

        # O tamanho dos individuos tem que ser setado nesse for
        for y in range(0,tam):

            porcentagem = int(cromossomos[x][y]*100)

            # Randomização apartir da porcentagem
            if random.randint(0, 100)< porcentagem:
                cromossomos[x].append(1)
            else:
                cromossomos[x].append(0)



    return cromossomos

def BornAChild(cromossomos,tam, blueprint):
    # Essa função irá gerar os pais das proximas gerações

    for x in range(0, len(cromossomos)):

        tamanho = tam

        for y in range(0,tam):

            EPVi = 100*Equation(cromossomos[x][tamanho],blueprint[y])
            tamanho+=1

            if random.randint(0, 100) < EPVi:
                cromossomos[x][y] = 1
            else:
                cromossomos[x][y] = 0
            if tamanho == len(cromossomos[0]):
                break

    return cromossomos

def Equation (probabilidade, probabilidadeblueprint):
    #Essa é a função que gera a probabilidade para a obetenção de um novo resultado

    #As duas variaveis seguintes são setadas manualmente para a melhoria da convergência
    ng = 0.1

    ndr = 0.05

    EPVi = (ng*probabilidadeblueprint) + ((1-ng)*probabilidade)

    if EPVi < ndr :
        EPVi = ndr
    if EPVi > 1-ndr:
        EPVi = 1-ndr

    return round(EPVi,2)

def NewBlueprint(blueprint, pais, tam):
    # Essa função irá gerar a blueprint para ser usada na proxima geração
    posição = 0

    for i in range(tam,int(tam*2)):
        auxiliar = 0.0
        for y in range(0,len(pais)):
            auxiliar += pais[y][i]
        blueprint[posição] = round(auxiliar/len(pais),2)
        posição+=1


    return blueprint

def ChangePlace(cromossomos):
    aux = []

    for x in range(0, len(cromossomos)):
        aux = deepcopy(cromossomos[x])
        tam = int(len(cromossomos[x]) / 2)
        for y in range(0, len(cromossomos[x])):
            cromossomos[x][y] = aux[tam]
            tam += 1
            if tam == len(cromossomos[x]):
                tam = 0

    return cromossomos

"""
def BornAnIndividualUNIQUE(cromossomo):

    individuo = []


    for y in range(0,len(cromossomo)):

         porcentagem = int(cromossomo[y]*100)

         if random.randint(0, 100)< porcentagem:
               individuo.append(1)
         else:

               individuo.append(0)


    print(individuo)
"""


def Crossover(pais,tam, blueprint):

    # Essa função ira receber a lista de pais e jogara dois para fazer crossover

    filhos = []
    y = 0
    for x in range(0, len(pais) - 1):
        filhos.append(FGACrossover(pais[x], pais[x + 1]))
        y = y + 1

    filhos.append(FGACrossover(pais[y], pais[y - 1]))

    return BornAChild(filhos,tam, blueprint)

def FGACrossover(pai1,pai2):

    #Learning Rate
    LR = 0.15

    filho = deepcopy(pai1)
    PontoCorte = int(len(pai1)/2)
    aux = PontoCorte

    #Como o filho é copia do pai1, deve-se so modificar a metade da sua solução e da probabibilidade
    for x in range (int(PontoCorte/2), PontoCorte):

        filho[x] = pai2[x]
        filho[x+PontoCorte] = pai2[x+PontoCorte]
        aux += 1

    aux = PontoCorte
    # Aqui ira fazer o calculo da nova probabilidade
    for x in range (0,PontoCorte):

        if filho[x] == 1:
           novaProb = filho[aux]+LR
        else:
           novaProb = filho[aux]-LR

        if novaProb > 1:
            novaProb=1
        if novaProb < 0:
            novaProb=0
        filho[aux] = round(novaProb,2)
        aux+=1

    return filho

