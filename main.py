from Ferramentas.Teste import Teste
from Benchmark import Benchmark
from Algoritmos import TrangenicGA
from Algoritmos import Theory_Of_ChaosGA
from Algoritmos import FluidGA
from Algoritmos import GABasico
from Algoritmos import HomogeneousGA
from Ferramentas.Plot import plot
from Ferramentas.Plot import salvar_resultados
# Transgenic GA

#teste = Teste(100, TrangenicGA.trangenicGA, False)
#teste.config_trans(benchmark=Benchmark.rastrigin, max_geracoes=250)
#teste.run()

# Theory of Chaos

#teste = Teste(10, Theory_Of_ChaosGA.chaosGA, False)
#teste.config_chaos(benchmark=Benchmark.ackley, max_geracoes=250)
#teste.teste()

# GA Basico

#teste = Teste(100, GABasico.GAbasico, False)
#teste.config_basico(benchmark=Benchmark.rastrigin, max_geracoes=250)
#teste.teste()

# Homogeneous GA

#teste = Teste(30, HomogeneousGA.homogeneousGA, False)
#teste.config_trans(benchmark=Benchmark.rastrigin, max_geracoes=250, prob_mut=0.2)
#teste.run()

# Fluid GA

#teste = Teste(10, FluidGA.FluidGA, False)
#teste.config_basico(benchmark=Benchmark.ackley, max_geracoes=250)
#teste.teste()

# ---------------------------------------------------------------------------------------------------- #

benchmark = Benchmark.schaffer

Basic = Teste(100, GABasico.GAbasico, False)
Basic.config_basico(benchmark=benchmark, max_geracoes=250)
mbi1, mgf1, nc1 = Basic.teste()

Theory = Teste(100, Theory_Of_ChaosGA.chaosGA, False)
Theory.config_chaos(benchmark=benchmark, max_geracoes=250)
mbi2, mgf2, nc2 = Theory.teste()

Trans = Teste(100, TrangenicGA.trangenicGA, False)
Trans.config_trans(benchmark=benchmark, max_geracoes=250)
mbi3, mgf3, nc3 = Trans.teste()

l = ['Basic GA', 'Theory of Chaos GA', 'Transgenic GA']
#mgf = [mgf1, mgf2, mgf3]
mbi = [mbi1, mbi2, mbi3]

#plot(mgf, l, 'Final Generation with ' + Benchmark.info(benchmark)[4], benchmark, 'Execution Number', 'Final Generation', True)
plot(mbi, l, benchmark, 'Best Individuals with ' + Benchmark.info(benchmark)[4], 'Execution Number', 'Best Individuals Fitness', True, (-0.01, 0.1))
salvar_resultados('Melhores Individuos com ' + Benchmark.info(benchmark)[4], mbi, ['Basic GA', 'Theory of Chaos GA', 'Trangenic GA'], benchmark)


# -------------------------------------------------------------------------------------------------- #
