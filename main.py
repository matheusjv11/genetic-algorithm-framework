from Ferramentas.Teste import Teste
from Benchmark import Benchmark
from Algoritmos import TrangenicGA
from Algoritmos import Theory_Of_ChaosGA
from Algoritmos import GABasico
from Ferramentas.Plot import plot

# Transgenic GA

#teste = Teste(100, TrangenicGA.trangenicGA, False)
#teste.config_trans(benchmark=Benchmark.rastrigin, max_geracoes=250)
#teste.teste()

# Theory of Chaos

#teste = Teste(10, Theory_Of_ChaosGA.chaosGA, False)
#teste.config_chaos(benchmark=Benchmark.ackley, max_geracoes=250)
#teste.teste()

# GA Basico

#teste = Teste(100, GABasico.GAbasico, False)
#teste.config_basico(benchmark=Benchmark.rastrigin, max_geracoes=250)
#teste.teste()

# ---------------------------------------------------------------------------------------------------- #

benchmark = Benchmark.rastrigin

Basic = Teste(100, GABasico.GAbasico, True)
Basic.config_basico(benchmark=benchmark, max_geracoes=250)
mbi1, mgf1, nc = Basic.teste()

Theory = Teste(100, Theory_Of_ChaosGA.chaosGA, True)
Theory.config_chaos(benchmark=benchmark, max_geracoes=250)
mbi2, mgf2, nc = Theory.teste()

Trans = Teste(100, TrangenicGA.trangenicGA, True)
Trans.config_trans(benchmark=benchmark, max_geracoes=250)
mbi3, mgf3, nc = Trans.teste()

l = ['Basic GA', 'Theory of Chaos GA', 'Transgenic GA']
mgf = [mgf1, mgf2, mgf3]
mbi = [mbi1, mbi2, mbi3]

plot(mgf, l, 'Final Generation with ' + Benchmark.info(benchmark)[4], 'Execution Number', 'Final Generation', True)
plot(mbi, l, 'Best Individuals with ' + Benchmark.info(benchmark)[4], 'Execution Number', 'Best Individual', True)