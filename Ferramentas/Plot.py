import matplotlib.pyplot as plt

def plot(matriz, legends, titulo = '', titulo_x = '', titulo_y = '', salvar = False, dir = ''):
    x = [i for i in range(1, len(matriz[0])+1)]
    for m, l in zip(matriz, legends):
        plt.plot(x, m, label=l)
    plt.legend(loc='best')
    plt.title(titulo)
    plt.xlabel(titulo_x)
    plt.ylabel(titulo_y)
    if salvar:
        plt.savefig(dir + titulo + '.pdf')
    plt.show()

