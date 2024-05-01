import gym_super_mario_bros
from nes_py.wrappers import JoypadSpace
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
import random

# Definindo as ações disponíveis como lista
ACTIONS = list(range(len(SIMPLE_MOVEMENT)))

# Classe para representar um indivíduo
class Individuo:
    def __init__(self, cromossomo_length):
        self.cromossomo_length = cromossomo_length
        self.cromossomo = [random.choice(ACTIONS) for _ in range(cromossomo_length)]
        self.fitness = 0


# Função para avaliar um indivíduo

def avaliar(individuo, env):
    observation = env.reset()
    done = False
    fitness = 0
    for gene in individuo.cromossomo:
        action = SIMPLE_MOVEMENT[gene]
        print(action)
        observation, reward, done, info = env.step(action)
        fitness += reward
        if done:
            break
    individuo.fitness = fitness




# Função para realizar a seleção dos melhores indivíduos
def selecao(populacao, n_melhores):
    populacao_ordenada = sorted(populacao, key=lambda x: x.fitness, reverse=True)
    return populacao_ordenada[:n_melhores]


# Função para realizar o cruzamento de dois indivíduos
def crossover(individuo1, individuo2):
    ponto_corte = random.randint(1, len(individuo1.cromossomo) - 1)
    filho1 = Individuo(len(individuo1.cromossomo))
    filho2 = Individuo(len(individuo2.cromossomo))
    filho1.cromossomo = individuo1.cromossomo[:ponto_corte] + individuo2.cromossomo[ponto_corte:]
    filho2.cromossomo = individuo2.cromossomo[:ponto_corte] + individuo1.cromossomo[ponto_corte:]
    return filho1, filho2


# Função para realizar a mutação em um indivíduo
def mutacao(individuo, taxa_mutacao):
    for i in range(len(individuo.cromossomo)):
        if random.uniform(0, 1) < taxa_mutacao:
            individuo.cromossomo[i] = random.choice(ACTIONS)


# Função principal para resolver o problema usando algoritmo genético
def resolver(tamanho_populacao, taxa_mutacao, numero_geracoes):
    env = gym_super_mario_bros.make('SuperMarioBros-1-2-v1', apply_api_compatibility=True, render_mode="human")
    env = JoypadSpace(env, SIMPLE_MOVEMENT)

    populacao = [Individuo(len(SIMPLE_MOVEMENT[0])) for _ in range(tamanho_populacao)]

    for geracao in range(numero_geracoes):
        for individuo in populacao:
            avaliar(individuo, env)

        melhores = selecao(populacao, int(0.2 * tamanho_populacao))

        nova_populacao = melhores[:]

        while len(nova_populacao) < tamanho_populacao:
            pai1 = random.choice(melhores)
            pai2 = random.choice(melhores)
            filho1, filho2 = crossover(pai1, pai2)
            mutacao(filho1, taxa_mutacao)
            mutacao(filho2, taxa_mutacao)
            nova_populacao.extend([filho1, filho2])

        populacao = nova_populacao

        print(
            f"Geração {geracao}: Melhor solução -> Fitness: {melhores[0].fitness}, Cromossomo: {melhores[0].cromossomo}")

    env.close()


# Parâmetros do algoritmo genético
tamanho_populacao = 50
taxa_mutacao = 0.1
numero_geracoes = 20

# Executar o algoritmo genético
resolver(tamanho_populacao, taxa_mutacao, numero_geracoes)