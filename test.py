# Import do emulador
import gym_super_mario_bros
from nes_py.wrappers import JoypadSpace
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
# Import da biblioteca random que será util para gerar valores aleatórios em certos pontos
import random
# Import da biblioteca OS para criar arquivos de logs de treinamento
import os

# Definindo as ações como lista
actions = list(range(len(SIMPLE_MOVEMENT)))

# Classe para representar um indivíduo ou solução
class Solution:
    def __init__(self, cromossomo=None):
        # Verifica se foi passado algum cromossomo
        if cromossomo:
            self.cromossomo = cromossomo
        # Se não, então irá gerar um array de 100 ações que será nosso cromossomo inicial
        # Se não fizermos isso, o fitness dificilmente aumentará,e o treinamento ficará mais lento
        else:
            self.cromossomo = [random.choice(actions) for i in range(100)]
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
        # Imcrementamos para a próxima ação do cromossomo
        cromossomo_index += 1

        # Se chegarmos ao final das ações do cromossomo, ele será reiniciado
        if cromossomo_index >= len(individuo.cromossomo):
            cromossomo_index = 0

        # Executando a ação no ambiente e obtendo as recompensas e informações
        observation, reward, done, info = env.step(action)

        # Atualizando o fitness com base nas informações do ambiente
        # Reward vai variar entre numeros positivos e negativos, pois representa a recompensa recebida após executar a ação.
        fitness += reward
        # Score se resume em derrotar inimigos
        fitness += info['score'] / 10
        # Coins se resume a coleta de moedas
        fitness += info['coins'] * 10

        # Podemos diminuir o fitness com perdas de vida
        if info['life'] < 2:
            fitness -= 100

        # Podemos diminuir o fitness se o personagem não avançar o suficiente pelo mapa
        if info['x_pos'] < 100:
            fitness -= 50

        # Renderiza o jogo
        env.render()

    # No final, atribuímos o valor total do fitness
    individuo.fitness = fitness


# Função para realizar a seleção dos melhores indivíduos
def selecao(populacao, melhores):
    # Utilizamos o sorted para ordenar a população de acordo com o fitness
    # Utilizamos a função lambda para especificar a chave de ordenamento dos elementos, que nesse caso é o fitness
    populacao_ordenada = sorted(populacao, key=lambda x: x.fitness, reverse=True)
    # Retorna os melhores indivíduos ordenados
    return populacao_ordenada[:melhores]


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
            # Se sofrer adicionamos uma ação aleatória
            individuo.cromossomo[i] = random.choice(actions)

# Função para iniciar o treinamento
def resolver(tamanho_populacao, taxa_mutacao, numero_geracoes, pasta_log):
    # Verifica se a pasta de log existe, senão a cria
    if not os.path.exists(pasta_log):
        os.makedirs(pasta_log)

    # Obtém o número do último treinamento realizado para gerar o nome do próximo arquivo de log
    ultimo_treinamento = 0
    for filename in os.listdir(pasta_log):
        if filename.startswith("log-"):
            numero_treinamento = int(filename.split("-")[-1].split(".")[0])
            if numero_treinamento > ultimo_treinamento:
                ultimo_treinamento = numero_treinamento

    # Incrementa o número do último treinamento para gerar o nome do próximo arquivo de log
    proximo_treinamento = ultimo_treinamento + 1
    nome_arquivo_log = f"log-treinamento{proximo_treinamento}.txt"
    caminho_arquivo_log = os.path.join(pasta_log, nome_arquivo_log)

    # Criando o ambiente do emulador
    env = gym_super_mario_bros.make('SuperMarioBros-1-2-v0')
    env = JoypadSpace(env, SIMPLE_MOVEMENT)

    # Iniciamos a população com indivíduos aleatorios
    populacao = [Solution() for i in range(tamanho_populacao)]

    # Abre o arquivo de log para escrita
    with open(caminho_arquivo_log, 'w') as log_file:
        # Iteramos sobre o número de gerações
        for geracao in range(numero_geracoes):
            # Iteramos sobre os indivíduos dentro da população
            for individuo in populacao:
                avaliar(individuo, env)

            # Selecionamos os melhores para reprodução
            melhores = selecao(populacao, int(0.2 * tamanho_populacao))

            # Nova população é criada a partir da seleção dos melhores
            nova_populacao = melhores[:]

            # Preenchemos a nova população com cruzamento e mutação até atingir o tamanho da população original
            while len(nova_populacao) < tamanho_populacao:
                if melhores:
                    # Escolhemos aleatoriamente dois pais da lista dos melhores indivíduos
                    pai1 = random.choice(melhores)
                    pai2 = random.choice(melhores)
                else:
                    # Se não houver indivíduos na lista de melhores, criamos novos indivíduos aleatórios
                    pai1 = Solution()
                    pai2 = Solution()

                # Cruzamento entre os cromossomos selecionados
                filho1, filho2 = crossover(pai1, pai2)
                # Mutação nos cromossomos gerados
                mutacao(filho1, taxa_mutacao)
                mutacao(filho2, taxa_mutacao)
                # Adicionamos os novos cromossomos a nova população
                nova_populacao.extend([filho1, filho2])

            # Próxima geração
            populacao = nova_populacao

            melhor_fitness = max(populacao, key=lambda x: x.fitness).fitness
            # Log dos melhores fitness para controle
            print(f"Geração {geracao}: Melhor solução -> Fitness: {melhor_fitness}")

            # Salvar o melhor fitness no arquivo de log
            log_file.write(f"Geração {geracao}: Melhor fitness -> {melhor_fitness}\n")

            # Adicionar os dados de cada indivíduo na geração ao arquivo de log
            for i, individuo in enumerate(populacao):
                log_file.write(f"Indivíduo {i}: Fitness -> {individuo.fitness}, Cromossomo -> {individuo.cromossomo}\n")

    # Encerra o emulador
    env.close()

# Parâmetros do algoritmo genético
tamanho_populacao = 10
taxa_mutacao = 0.1
numero_geracoes = 190
pasta_log = "./logs-treinamentos"

# Executar o algoritmo genético
resolver(tamanho_populacao, taxa_mutacao, numero_geracoes, pasta_log)