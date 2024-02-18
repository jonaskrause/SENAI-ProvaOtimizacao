import pulp

# Definição das ordens e dutos
ordens = ['Ordem1', 'Ordem2', 'Ordem3', 'Ordem4']
dutos = ['E1', 'C1']

# Tempo de processamento para cada ordem em cada duto
tempo_processamento = {
    ('Ordem1', 'E1'): 18+2,
    ('Ordem1', 'C1'): 4+4,
    ('Ordem2', 'E1'): 14+2,
    ('Ordem2', 'C1'): 4+4,
    ('Ordem3', 'E1'): 12+2,
    ('Ordem3', 'C1'): 6+4,
    ('Ordem4', 'E1'): 6+2,
    ('Ordem4', 'C1'): 6+4
}

# Ordenar as ordens com base no tempo total de processamento em ambos os dutos
ordens = sorted(ordens, key=lambda o: sum(tempo_processamento[o, d] for d in dutos))

# Criação do problema de programação linear inteira
prob = pulp.LpProblem("Scheduling", pulp.LpMinimize)

# Variáveis de decisão
x = pulp.LpVariable.dicts("x", [(o, d) for o in ordens for d in dutos], cat='Binary')
espera = pulp.LpVariable.dicts("espera", ordens, lowBound=0, cat='Continuous')

# Função objetivo
prob += pulp.lpSum(x[o, d] * tempo_processamento[o, d] for o in ordens for d in dutos) + pulp.lpSum(espera[o] for o in ordens)

# Restrições
for o in ordens:
    for d in dutos:
        prob += x[o, d] >= 0  # Garante que a variável de decisão seja binária

# Restrição: Todas as ordens devem ser processadas em ambos os dutos
for o in ordens:
    prob += pulp.lpSum(x[o, d] for d in dutos) == 2

# Restrição: Tempo de espera
for o in ordens:
    prob += espera[o] >= (tempo_processamento[o, 'E1'] - tempo_processamento[o, 'C1']) * (x[o, 'E1'] - x[o, 'C1'])

# Resolvendo o problema
prob.solve()

# Exibindo os resultados
for d in dutos:
    ordens_duto = [o for o in ordens if pulp.value(x[o, d]) == 1]
    print(f"Ordem das ordens no {d}: {', '.join(ordens_duto)}")
#
#