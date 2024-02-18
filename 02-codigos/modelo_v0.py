from pulp import LpVariable, LpProblem, LpMinimize, lpSum, LpMaximize

# O solver utilizado neste código é o CBC (Coin-or branch and cut), que é o solver padrão utilizado pelo PuLP quando não especificado explicitamente. 
# O CBC é um solver de código aberto para programação linear e inteira mista desenvolvido pelo COIN-OR (Computational Infrastructure for Operations Research). 
# Ele implementa uma combinação de algoritmos de branch-and-bound, cutting plane e branch-and-cut para resolver problemas de otimização linear e inteira mista.

# Dados do problema
T = {
    1: {1: 12+2, 2: 12+3},
    2: {1: 10+2, 2: 10+3},
    3: {1: 8+2, 2: 8+3},
    4: {1: 4+2, 2: 4+3}
    # +2 e +3 adicionados para representar o "setup" da máquina 1 e 2
}

num_ordens = len(T)  # Número de ordens
num_maquinas = 2  # Número de máquinas de enfesto

# Inicialização do problema de programação linear
problema = LpProblem("Modelo_V0", LpMinimize)

# Variáveis de decisão
X = {}
for i in range(1, num_ordens + 1):
    for j in range(1, num_maquinas + 1):
        X[i, j] = LpVariable('X[%i,%i]' % (i, j), cat='Binary')

# Função objetivo
objetivo = LpVariable("objetivo", lowBound=0, cat='Continuous')  # Variável para representar o máximo dos tempos
problema += objetivo  # Objetivo de maximizar o máximo dos tempos

for j in range(1, num_maquinas + 1):
    problema += objetivo >= lpSum(T[i][j] * X[i, j] for i in range(1, num_ordens + 1))  # Garantindo que objetivo >= max(tempo_maquina_j)

# Restrições
for i in range(1, num_ordens + 1):
    problema += (lpSum(X[i, j] for j in range(1, num_maquinas + 1)) == 1)

# Resolvendo o problema
problema.solve()

# Verificando se encontrou solução ótima
if problema.status == 1:
    print('Tempo total mínimo necessário:', objetivo.value())
    print('Alocação de ordens de produção em máquinas:')
    for i in range(1, num_ordens + 1):
        for j in range(1, num_maquinas + 1):
            if X[i, j].value() == 1:
                print('Ordem', i, 'na máquina', j)
else:
    print('O problema não possui solução ótima.')