from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
import Benchmark as ben
from Benchmark import info
import numpy as np
from matplotlib.ticker import LinearLocator, FormatStrFormatter

rastrigin = 0
ackley = 1
keane = 2
shubert = 3
shubert3 = 4
schaffer = 5
zdt1 = 6
zdt2 = 7

rastrigin_str = "Rastrigin"
ackley_str = "Ackley"
keane_str = "Keane"
shubert_str = "Shubert"
shubert3_str = "Shubert 3"
schaffer_str = "Schaffer"
zdt1_str = "ZDT1"
zdt2_str = "ZDT2"

def plot3D(funcao ,limMi = None, limMa = None):
    if limMi == None:
        limMi = info(funcao)[0]
    if limMa == None:
        limMa = info(funcao)[1]

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    x = np.linspace(limMi, limMa, 300)
    y = np.linspace(limMi, limMa, 300)
    X, Y = np.meshgrid(x, y)
    Z = call(funcao, [X, Y])

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('f(x)(' + get_str(funcao) + ')')
    ax.set_title(get_str(funcao))
    plt.savefig('superficie na função ' + get_str(funcao) + '.pdf')

    fig.tight_layout()

    plt.show()

#def plot2D(funcao ,limMi, limMa):
#    results = [[], [], []]
#    x = np.linspace(limMi, limMa, 300)
#    plt.plot(x, results)
#    plt.show()

def call(funcao,list_entradas):
    if funcao == 0:
        return ben.rastrigin(list_entradas)[0]
    elif funcao == 1:
        return ben.ackley(list_entradas)[0]
    elif funcao == 2:
        return ben.keane(list_entradas)[0]
    elif funcao == 3:
        return ben.shubert(list_entradas)[0]
    elif funcao == 4:
        return ben.shubert3(list_entradas)[0]
    elif funcao == 5:
        return ben.schaffer(list_entradas)[0]
    elif funcao == 6:
        return ben.zdt1(list_entradas)
    elif funcao == 7:
        return ben.zdt2(list_entradas)
    else:
        return None

def get_str(funcao):
    if funcao == 0:
        return rastrigin_str
    elif funcao == 1:
        return ackley_str
    elif funcao == 2:
        return keane_str
    elif funcao == 3:
        return shubert_str
    elif funcao == 4:
        return shubert3_str
    elif funcao == 5:
        return schaffer_str
    elif funcao == 6:
        return zdt1_str
    elif funcao == 7:
        return zdt2_str
    else:
        return None

if __name__ == "__main__":
    plot3D(schaffer)
