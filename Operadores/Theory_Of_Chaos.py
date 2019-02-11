import random

from deap import base
from deap import creator
from deap import tools
from Benchmark import Benchmark
from copy import deepcopy


def crossover(pais,numero_entradas):

    filhos = []
    y=0
    for x in range (0, len(pais)-1):
       filhos.append(crossoverSOLUTION(pais[x],pais[x+1],numero_entradas))
       y=y+1
    oi=0
    filhos.append(crossoverSOLUTION(pais[y], pais[y-1], numero_entradas))



    return filhos

def crossoverSOLUTION(pai1,pai2,numero_entradas):

        filho = deepcopy(pai1)

        tamMask = int((len(pai1)-6)/2)

        pontoCorte = len(pai1)-tamMask

        mask=binaryTogray(pai1[pontoCorte:])
        Lambda = pai1[tamMask:tamMask+6]

        for x in range (0, tamMask):
            if mask[x]==1:
                filho[x] = pai1[x]
            else:
                filho[x] = pai2[x]



        mascara = NewMask(Lambda,pai1[pontoCorte:],numero_entradas)
        pontoMascara = int(((len(pai2) - 6) / 2) + 6)

        for x in range(0,len(mascara)):
            filho[pontoMascara+x] = mascara[x]

        return filho

def NewMask(Lambda, Mask , numero_entradas):



        LambdaNoInterlavo = (4/((2**6)-1))*int("".join(str(i) for i in Lambda),2)
        Xn = []
        NewXN = []
        Cada = int(len(Mask)/numero_entradas)

        for x in range (0,numero_entradas):
            Xn.append(Mask[Cada*x:Cada*(x+1)])

        for x in range (0,numero_entradas):
           NewXN.append(grayTobinary(Xn[x]))


        newmask = []

        for y in range (0,len(NewXN)):
            newmaskXN =Chaoticfunction(LambdaNoInterlavo,(1/((2**Cada)-1))*int("".join(str(i) for i in NewXN[y]),2))
            newmaskINT=int(newmaskXN/(1/((2**Cada)-1)))
            newmaskBIN= dec2bin(newmaskINT,Cada)
            newmask += newmaskBIN

        return newmask

def Chaoticfunction (Lambda,Zn):
        newzen = Lambda*Zn*(1-Zn)
        return newzen

def dec2bin(n,tam):
    b = []
    while n != 0:
        b.append(n % 2)
        n = int(n / 2)
    while len(b)<tam:
        b.append(0)


    c = [b[len(b)-1-i] for i in range(len(b))]

    return c

def binaryTogray(binario):

    graycode = []

    graycode.append(binario[0])

    for x in range (0,len(binario)-1):
        if (binario[x]+binario[x+1])==0 or (binario[x]+binario[x+1])==2 :
            graycode.append(0)
        else:
            graycode.append(1)

    return graycode

def grayTobinary(gray):

    binario = []

    binario.append(gray[0])

    for x in range(0, len(gray) - 1):
        if (binario[x] + gray[x + 1]) == 0 or (binario[x] + gray[x + 1]) == 2:
            binario.append(0)
        else:
            binario.append(1)

    return binario

