import random
from deap import base, creator, tools, algorithms

# Dados do problema
T = {
    1: {1: 12+2, 2: 12+3},
    2: {1: 10+2, 2: 10+3},
    3: {1: 8+2, 2: 8+3},
    4: {1: 4+2, 2: 4+3}
}

num_ordens = len(T)  # Número de ordens
num_maquinas = 2  # Número de máquinas de enfesto

# Função objetivo para algoritmo genético
def objetivo(individual):
    tempos_maquinas = [sum(T[i][j] for i in range(1, num_ordens + 1) if individual[i-1] == j) for j in range(1, num_maquinas + 1)]
    return max(tempos_maquinas),

# Definindo o problema como um problema de minimização
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Gerando indivíduos
toolbox.register("indices", random.sample, list(range(1, num_maquinas + 1)) * num_ordens, num_ordens)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Registrando operadores genéticos
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", objetivo)

# Configurando a população e evoluindo
pop = toolbox.population(n=100)
algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=10, verbose=False)

# Obtendo o melhor indivíduo e sua avaliação
best_ind = tools.selBest(pop, k=1)[0]
best_fit = objetivo(best_ind)

# Imprimindo resultados
print('Tempo total mínimo necessário:', best_fit[0])
print('Alocação de ordens de produção em máquinas:')
for i, machine in enumerate(best_ind, start=1):
    print(f'Ordem {i} na máquina {machine}')