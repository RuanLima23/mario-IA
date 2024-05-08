import gym_super_mario_bros
from nes_py.wrappers import JoypadSpace
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
import random
import os
import matplotlib.pyplot as plt

# Criando a pasta de logs e gráficos
pasta_logs = "./logs-treinamentos"
pasta_graficos = "./graficos"
if not os.path.exists(pasta_logs):
    os.makedirs(pasta_logs)
if not os.path.exists(pasta_graficos):
    os.makedirs(pasta_graficos)

# Definindo as ações como lista
actions = list(range(len(SIMPLE_MOVEMENT)))

# Classe para representar um indivíduo ou solução
class Solution:
    def __init__(self, cromossomo=None):
        # Verifica se foi passado algum cromossomo
        if cromossomo:
            self.cromossomo = cromossomo
        # Se não, então irá gerar um array de 8000 ações que será nosso cromossomo inicial
        # A cada 1 segundo 20 ações são realizadas, o tempo da fase é 400 segundos
        # Portanto 20 x 400 = 8000 posições
        else:
            self.cromossomo = [random.choice(actions) for i in range(8000)]
        self.fitness = 0

# Função para avaliar um indivíduo
def avaliar(individuo, env):
    observation = env.reset()
    # Iniciamos o game por um while com um fitness zerado
    done = False
    fitness = 0
    # Inicializamos o índice do cromossomo zerado
    cromossomo_index = 0

    # Enquanto a condição for falsa, o jogo continua até o tempo acabar
    while not done:
        # Obtemos a ação do cromossomo atual
        action = individuo.cromossomo[cromossomo_index]
        # Incrementamos para a próxima ação do cromossomo
        cromossomo_index += 1

        # Se chegarmos ao final das ações do cromossomo, ele será reiniciado
        if cromossomo_index >= len(individuo.cromossomo):
            cromossomo_index = 0

        # Executando a ação no ambiente e obtendo as recompensas e informações
        observation, reward, done, info = env.step(action)

        # Atualizando o fitness com base nas informações do ambiente
        if info['flag_get'] == True:
            fitness += 10000

        # Podemos aumentar o fitness se o personagem avançar pelo mapa
        if info['x_pos'] < 300:
            fitness += 10

        if info['x_pos'] < 200:
            fitness += 50

        if info['x_pos'] < 100:
            fitness += 100

        if info['x_pos'] < 50:
            fitness += 150

        if info['x_pos'] < 25:
            fitness += 200

        if info['x_pos'] < 10:
            fitness += 250

        # Renderiza o jogo
        env.render()

    # No final, atribuímos o valor total do fitness
    individuo.fitness = fitness

# Encontra o melhor indivíduo para a reprodução
def encontrar_melhor_fitness(populacao):
    melhor_individuo = None
    melhor_fitness = 0

    # Itera sobre a população para encontrar o indivíduo com o melhor fitness
    for individuo in populacao:
        if individuo.fitness > melhor_fitness:
            melhor_fitness = individuo.fitness
            melhor_individuo = individuo

    return melhor_individuo

# Função para realizar a seleção dos melhores indivíduos
def selecao(populacao, melhores):
    # Encontra o melhor indivíduo na população
    melhor_individuo = encontrar_melhor_fitness(populacao)

    # Inicializa a lista de melhores indivíduos com o melhor indivíduo encontrado
    melhores_individuos = [melhor_individuo]

    # Se a quantidade de melhores indivíduos for menor que o valor especificado,
    # preenche com os indivíduos restantes da população, excluindo o melhor indivíduo
    if melhores > 1:
        restantes = melhores - 1
        populacao_ordenada = sorted(populacao, key=lambda x: x.fitness, reverse=True)
        for individuo in populacao_ordenada:
            if individuo != melhor_individuo:
                melhores_individuos.append(individuo)
                restantes -= 1
            if restantes == 0:
                break

    return melhores_individuos

# Função para realizar o cruzamento de dois indivíduos
def crossover(individuo1, individuo2):
    # Verifica se a quantidade de ações
    # Para o ponto de corte o cromossomo deve ter mais de 1 ação
    if len(individuo1.cromossomo) <= 1 or len(individuo2.cromossomo) <= 1:
        return individuo1, individuo2

    # Escolhe um ponto de corte aleatório
    ponto_corte = random.randint(1, len(individuo1.cromossomo) - 1)

    # Os novos cromossomos serão iniciados com o mesmo tamanho dos anteriores
    filho1 = Solution(len(individuo1.cromossomo))
    filho2 = Solution(len(individuo2.cromossomo))
    # Realizamos de fato o crossover a partir do ponto definido em cada cromossomo
    filho1.cromossomo = individuo1.cromossomo[:ponto_corte] + individuo2.cromossomo[ponto_corte:]
    filho2.cromossomo = individuo2.cromossomo[:ponto_corte] + individuo1.cromossomo[ponto_corte:]
    return filho1, filho2

# Função para realizar a mutação em um indivíduo
def mutacao(individuo, taxa_mutacao):
    # Definimos a taxa como 0,1
    # Percorre todas as ações do cromossomo, se alguma cair menor que 0,1 então sofrerá mutação
    for i in range(len(individuo.cromossomo)):
        if random.uniform(0, 1) < taxa_mutacao:
            # Se sofrer, adicionamos uma ação aleatória
            individuo.cromossomo[i] = random.choice(actions)

# Função para iniciar o treinamento
def resolver(tamanho_populacao, taxa_mutacao, numero_geracoes):

    # Criando o ambiente do emulador
    env = gym_super_mario_bros.make('SuperMarioBros-1-2-v0')
    env = JoypadSpace(env, SIMPLE_MOVEMENT)

    # Iniciamos a população com indivíduos aleatórios
    populacao = [Solution() for i in range(tamanho_populacao)]

    # Obtém o número do último treinamento realizado para gerar o nome do próximo arquivo de log
    ultimo_treinamento = 0
    for filename in os.listdir(pasta_logs):
        if filename.startswith("log-"):
            numero_treinamento = int(filename.split("-")[-1].split(".")[0])
            if numero_treinamento > ultimo_treinamento:
                ultimo_treinamento = numero_treinamento

    # Incrementa o número do último treinamento para gerar o nome do próximo arquivo de log
    proximo_treinamento = ultimo_treinamento + 1
    nome_arquivo_log = f"log-{proximo_treinamento}.txt"
    caminho_arquivo_log = os.path.join(pasta_logs, nome_arquivo_log)

    # Abre o arquivo de log para escrita
    with open(caminho_arquivo_log, 'w', encoding='utf-8') as log_file:
        # Mostra quantas gerações tem o treinamento
        log_file.write(f"Número de Gerações nesse treinamento: {numero_geracoes}\n")
        log_file.write('\n')
        # Lista para gerar o gráfico
        melhores_por_geracao = []
        # Iteramos sobre o número de gerações
        for geracao in range(numero_geracoes):
            # Iteramos sobre os indivíduos dentro da população
            for individuo in populacao:
                avaliar(individuo, env)

            melhor_fitness = max(populacao, key=lambda x: x.fitness).fitness
            # Log dos melhores fitness para controle
            print(f"Geração {geracao}: Melhor solução -> Fitness: {melhor_fitness}")

            # Salvar o melhor fitness no arquivo de log
            log_file.write(f"Geração {geracao}: Melhor fitness -> {melhor_fitness}\n")

            # Adicionar os dados de cada indivíduo na geração ao arquivo de log
            for i, individuo in enumerate(populacao):
                log_file.write(f"Indivíduo {i}: Fitness -> {individuo.fitness}, Cromossomo -> {individuo.cromossomo}\n")
                log_file.write('\n')

            # Selecionamos os melhores para reprodução
            melhores = selecao(populacao, int(0.2 * tamanho_populacao))
            melhores_por_geracao.append(melhores[0])

            # Nova população é criada a partir da seleção dos melhores
            nova_populacao = melhores[:]

            # Preenchemos a nova população com cruzamento e mutação até atingir o tamanho da população original
            while len(nova_populacao) < tamanho_populacao:
                if melhores:
                    pai1 = random.choice(melhores)
                    pai2 = random.choice(melhores)
                else:
                    pai1 = Solution()
                    pai2 = Solution()

                filho1, filho2 = crossover(pai1, pai2)
                mutacao(filho1, taxa_mutacao)
                mutacao(filho2, taxa_mutacao)
                nova_populacao.extend([filho1, filho2])

            # Próxima geração
            populacao = nova_populacao

        # Salvando o gráfico
        melhor_fitnesses = [melhor.fitness for melhor in melhores_por_geracao]
        plt.plot(melhor_fitnesses)
        plt.title("Melhor Fitness por Geração")
        plt.xlabel("Geração")
        plt.ylabel("Fitness")
        plt.savefig(f"{pasta_graficos}/grafico-{proximo_treinamento}.png")
        plt.close()

    # Encerra o emulador
    env.close()

# Parâmetros do algoritmo genético
tamanho_populacao = 1
taxa_mutacao = 0.1
numero_geracoes = 1

# Executar o algoritmo genético
resolver(tamanho_populacao, taxa_mutacao, numero_geracoes)

