import random

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

# Função para calcular o tempo total de processamento de uma solução
def calcular_tempo_total(sol, tempo_processamento):
    tempo_total = 0
    for i, duto in enumerate(sol):
        for ordem in duto:
            tempo_total += tempo_processamento[ordem, dutos[i]]
    return tempo_total

# Função para avaliar a aptidão de uma solução
def avaliar_aptidao(sol, tempo_processamento):
    tempo_total = calcular_tempo_total(sol, tempo_processamento)
    return tempo_total

# Função para selecionar indivíduos para reprodução
def selecao(populacao, aptidoes):
    selecionados = random.choices(populacao, weights=aptidoes, k=2)
    return selecionados

# Função para realizar crossover entre dois indivíduos
def crossover(individuo1, individuo2):
    ponto_corte = random.randint(1, len(individuo1) - 1)
    filho1 = individuo1[:ponto_corte] + individuo2[ponto_corte:]
    filho2 = individuo2[:ponto_corte] + individuo1[ponto_corte:]
    return filho1, filho2

# Função para realizar mutação em um indivíduo
def mutacao(individuo, taxa_mutacao):
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            random.shuffle(individuo[i])
    return individuo

# Parâmetros do algoritmo genético
tamanho_populacao = 20
taxa_mutacao = 0.1
num_geracoes = 100

# Inicialização da população aleatória
populacao = [[random.sample(ordens, len(ordens)) for _ in range(len(dutos))] for _ in range(tamanho_populacao)]

# Avaliação da aptidão da população inicial
aptidoes = [avaliar_aptidao(individuo, tempo_processamento) for individuo in populacao]

# Evolução da população
for geracao in range(num_geracoes):
    # Seleção dos indivíduos para reprodução
    selecionados = selecao(populacao, aptidoes)   
    # Reprodução (crossover)
    filhos = []
    for i in range(0, len(selecionados), 2):
        filho1, filho2 = crossover(selecionados[i], selecionados[i+1])
        filhos.extend([filho1, filho2])   
    # Mutação
    for i in range(len(filhos)):
        filhos[i] = mutacao(filhos[i], taxa_mutacao)   
    # Avaliação da aptidão dos filhos
    aptidoes_filhos = [avaliar_aptidao(individuo, tempo_processamento) for individuo in filhos]  
    # Substituição da população pelos filhos, se forem melhores
    for i in range(len(filhos)):
        if aptidoes_filhos[i] < aptidoes[i]:
            populacao[i] = filhos[i]
            aptidoes[i] = aptidoes_filhos[i]

# Encontrando a melhor solução para o duto C1 na população final
melhor_indice = aptidoes.index(min(aptidoes))
melhor_sol_c1 = populacao[melhor_indice][1]  # Acessando apenas o duto C1

# Exibindo o resultado apenas para o duto C1
print("Ordem das ordens no C1:", ', '.join(melhor_sol_c1))
