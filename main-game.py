import gym_super_mario_bros
from nes_py.wrappers import JoypadSpace
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from random import random
import numpy as np

# Tamanho do cromossomo (número de ações)
TAMANHO_CROMOSSOMO = 7

class Individuo():
    def __init__(self, limite_espacos, geracao=0):
        self.limite_espacos = limite_espacos
        self.nota_avaliacao = 0
        self.geracao = geracao
        self.cromossomo = np.random.randint(2, size=TAMANHO_CROMOSSOMO)  # Cromossomo binário inicial aleatório

    def avaliacao(self):
        # Aqui você precisa executar o jogo com o cromossomo e avaliar o tempo necessário para concluir a fase
        # A nota de avaliação pode ser inversamente proporcional ao tempo, quanto menor o tempo, melhor a nota
        # Você precisará adaptar essa parte para a integração com o jogo
        nota = TAMANHO_CROMOSSOMO - np.sum(self.cromossomo)
        self.nota_avaliacao = nota

    def crossover(self, outro_individuo):
        corte = round(random() * TAMANHO_CROMOSSOMO)
        filho1 = np.concatenate((self.cromossomo[:corte], outro_individuo.cromossomo[corte:]))
        filho2 = np.concatenate((outro_individuo.cromossomo[:corte], self.cromossomo[corte:]))
        filhos = [Individuo(self.limite_espacos, self.geracao + 1),
                  Individuo(self.limite_espacos, self.geracao + 1)]
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos

    def mutacao(self, taxa_mutacao):
        for i in range(len(self.cromossomo)):
            if random() <= taxa_mutacao:
                self.cromossomo[i] = 1 if self.cromossomo[i] == 0 else 0
        return self

class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao, taxa_mutacao, numero_geracoes):
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao = taxa_mutacao
        self.numero_geracoes = numero_geracoes
        self.populacao = []
        self.melhor_solucao = None
        self.lista_solucoes = []

    def inicializa_populacao(self):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(limite_espacos=None))  # Limite de espacos não utilizado aqui

    def ordena_populacao(self):
        self.populacao = sorted(self.populacao, key=lambda individuo: individuo.nota_avaliacao, reverse=True)

    def seleciona_pai(self):
        soma_avaliacao = sum(individuo.nota_avaliacao for individuo in self.populacao)
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
            if soma > valor_sorteado:
                return individuo

    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("Geração %s -> Melhor Nota: %s Cromossomo: %s" % (melhor.geracao, melhor.nota_avaliacao, melhor.cromossomo))

    def resolver(self):
        self.inicializa_populacao()

        for individuo in self.populacao:
            individuo.avaliacao()

        self.ordena_populacao()
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)

        self.visualiza_geracao()

        for geracao in range(self.numero_geracoes):
            nova_populacao = []

            for _ in range(0, self.tamanho_populacao, 2):
                pai1 = self.seleciona_pai()
                pai2 = self.seleciona_pai()

                filhos = pai1.crossover(pai2)
                nova_populacao.extend([filho.mutacao(self.taxa_mutacao) for filho in filhos])

            self.populacao = nova_populacao

            for individuo in self.populacao:
                individuo.avaliacao()

            self.ordena_populacao()
            self.visualiza_geracao()
            self.lista_solucoes.append(self.populacao[0].nota_avaliacao)

        print("\nMelhor solução -> Geração: %s Nota: %s Cromossomo: %s" %
              (self.melhor_solucao.geracao, self.melhor_solucao.nota_avaliacao, self.melhor_solucao.cromossomo))

        return self.melhor_solucao.cromossomo

# Parâmetros do algoritmo genético
tamanho_populacao = 10
taxa_mutacao = 0.01
numero_geracoes = 10

# Execução do algoritmo genético
ag = AlgoritmoGenetico(tamanho_populacao, taxa_mutacao, numero_geracoes)
melhor_cromossomo = ag.resolver()

# Salvando os resultados em um arquivo de texto
with open('resultados.txt', 'w') as arquivo:
    arquivo.write("Melhor solução -> Geração: %s Nota: %s Cromossomo: %s\n" %
                  (ag.melhor_solucao.geracao, ag.melhor_solucao.nota_avaliacao, ag.melhor_solucao.cromossomo))
    arquivo.write("Lista de notas por geração:\n")
    for i, nota in enumerate(ag.lista_solucoes):
        arquivo.write("Geração %s: %s\n" % (i, nota))

