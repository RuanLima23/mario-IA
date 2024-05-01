class Produto():
    def __init__(self,nome,espaco,valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor

"""# Class Individuo"""

from random import random

class Individuo():
    def __init__(self, espacos, valores, limite_espacos, geracao=0):
        self.espacos = espacos
        self.valores = valores
        self.limite_espacos = limite_espacos
        self.nota_avaliacao = 0
        self.espaco_usado = 0
        self.geracao = geracao
        self.cromossomo = []

        # vai criar o cromossomo com valores aleatorios
        for i in range(len(espacos)):
            if random() < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")

    def avaliacao(self):
        nota = 0
        soma_espacos = 0
        for i in range(len(self.cromossomo)):
            print()
        #     if self.cromossomo[i] == '1':
        #         nota += self.valores[i]
        #         soma_espacos += self.espacos[i]
        # if soma_espacos > self.limite_espacos:
        #     nota = 1
        self.nota_avaliacao = nota
        self.espaco_usado = soma_espacos

    def crossover(self, outro_individuo):
        corte = round(random() * len(self.cromossomo))

        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]


        filhos = [Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1),
                  Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1)]
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos

    def mutacao(self, taxa_mutacao):
        for i in range(len(self.cromossomo)):
            if random() <= taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        return self

"""# Class AlgoritmoGenetico"""

class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = []

    def inicializa_populacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(espacos, valores, limite_espacos))
        self.melhor_solucao = self.populacao[0]

    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)

    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo

    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
        return soma

    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai

    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("G:%s -> Valor: %s Espaço: %s Cromossomo: %s" % (self.populacao[0].geracao,
                                                               melhor.nota_avaliacao,
                                                               melhor.espaco_usado,
                                                               melhor.cromossomo))

    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espacos):
        self.inicializa_populacao(espacos, valores, limite_espacos)

        for individuo in self.populacao:
            individuo.avaliacao()

        self.ordena_populacao()

        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)

        self.visualiza_geracao()

        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []

            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)

                filhos = self.populacao[pai1].crossover(self.populacao[pai2])

                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))

            #antiga população vai para o "lixo"
            self.populacao = list(nova_populacao)

            for individuo in self.populacao:
                individuo.avaliacao()

            self.ordena_populacao()

            self.visualiza_geracao()

            melhor = self.populacao[0]

            self.lista_solucoes.append(melhor.nota_avaliacao)

            self.melhor_individuo(melhor)

        print("\nMelhor solução -> G: %s Valor: %s Espaço: %s Cromossomo: %s" %
              (self.melhor_solucao.geracao,
               self.melhor_solucao.nota_avaliacao,
               self.melhor_solucao.espaco_usado,
               self.melhor_solucao.cromossomo))

        return self.melhor_solucao.cromossomo


"""# Main"""

#import matplotlib.pyplot as plt

listaProdutos = []
listaProdutos.append(Produto("Geladeira Dako", 0.751, 999.90))
listaProdutos.append(Produto("Iphone 6", 0.0000899, 2911.12))
listaProdutos.append(Produto("TV 55' ", 0.400, 4346.99))
listaProdutos.append(Produto("TV 50' ", 0.290, 3999.90))
listaProdutos.append(Produto("TV 42' ", 0.200, 2999.00))
listaProdutos.append(Produto("Notebook Dell", 0.00350, 2499.90))
listaProdutos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
listaProdutos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
listaProdutos.append(Produto("Microondas LG", 0.0544, 429.90))
listaProdutos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
listaProdutos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
listaProdutos.append(Produto("Geladeira Consul", 0.870, 1199.89))
listaProdutos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
listaProdutos.append(Produto("Notebook Asus", 0.527, 3999.00))


# for produto in listaProdutos:
#     print(produto.nome)



espacos = []
valores = []
nomes = []


for produto in listaProdutos:
    espacos.append(produto.espaco)
    valores.append(produto.valor)
    nomes.append(produto.nome)

#limite da capacidade da carga no caminhão
limite = 3


# individuo1 = Individuo(espacos,valores,limite)
# print(individuo1.cromossomo)

# individuo1 = Individuo(espacos,valores,limite)
# print('Espaços = %s' % str(individuo1.espacos))
# print('Valores = %s' % str(individuo1.valores))
# print('Cromossomo = %s' % str(individuo1.cromossomo))

# print('\nComponentes da Carga')
# for i in range(len(listaProdutos)):
#     if individuo1.cromossomo[i]=='1':
#         print("Nome: %s R$ %s " % (listaProdutos[i].nome,listaProdutos[i].valor))



# #avaliação

# individuo1 = Individuo(espacos,valores,limite)
# individuo1.avaliacao()
# print('Nota = %s' % individuo1.nota_avaliacao)
# print('Espaço usado = %s' % individuo1.espaco_usado)



# #crossover

# individuo1 = Individuo(espacos,valores,limite)
# print('Cromossomo = %s' % str(individuo1.cromossomo))

# individuo2 = Individuo(espacos,valores,limite)
# print('Cromossomo = %s' % str(individuo2.cromossomo))


# filhos = individuo1.crossover(individuo2)
# print('Cromossomo = %s' % str(filhos[0].cromossomo))
# print('Cromossomo = %s' % str(filhos[1].cromossomo))

# #Mutação
# individuo1 = Individuo(espacos,valores,limite)
# print('Antes Cromossomo = %s' % str(individuo1.cromossomo))

# individuo1.mutacao(0.05)
# print('Depois Cromossomo = %s' % str(individuo1.cromossomo))


# #criação da população
# tamanho_populacao = 20
# ag = AlgoritmoGenetico(tamanho_populacao)
# ag.inicializa_populacao(espacos,valores,limite)
# for i in range(ag.tamanho_populacao):
#     print('***** Indivíduo %s *****\n' % i,
#           'Espaços = %s\n' % str(ag.populacao[i].espacos),
#           'Valores = %s\n' % str(ag.populacao[i].valores),
#           'Cromossomo = %s\n' % str(ag.populacao[i].cromossomo))



# # #ordena_populacao (avaliação)
# tamanho_populacao = 20
# ag = AlgoritmoGenetico(tamanho_populacao)
# ag.inicializa_populacao(espacos,valores,limite)
# for individuo in ag.populacao:
#     individuo.avaliacao()
# ag.ordena_populacao()
# for i in range(ag.tamanho_populacao):
#     print('***** Indivíduo %s *****\n' % i,
#           'Espaços = %s\n' % str(ag.populacao[i].espacos),
#           'Valores = %s\n' % str(ag.populacao[i].valores),
#           'Cromossomo = %s\n' % str(ag.populacao[i].cromossomo),
#           'Nota = %s\n' % str(ag.populacao[i].nota_avaliacao))



# #melhor solução
# tamanho_populacao = 20
# ag = AlgoritmoGenetico(tamanho_populacao)
# ag.inicializa_populacao(espacos,valores,limite)
# for individuo in ag.populacao:
#     individuo.avaliacao()
# ag.ordena_populacao()
# ag.melhor_individuo(ag.populacao[0])
# print('Melhor solução para o problema: %s' % ag.melhor_solucao.cromossomo,
#       'Nota = %s\n' % ag.melhor_solucao.nota_avaliacao)



# #Soma das avaliações
# tamanho_populacao = 20
# ag = AlgoritmoGenetico(tamanho_populacao)
# ag.inicializa_populacao(espacos,valores,limite)
# for individuo in ag.populacao:
#     individuo.avaliacao()
# ag.ordena_populacao()
# ag.melhor_individuo(ag.populacao[0])
# soma = ag.soma_avaliacoes()
# print("Soma das avaliações: %s" % soma)



# #seleciona_pai
# tamanho_populacao = 20
# ag = AlgoritmoGenetico(tamanho_populacao)
# ag.inicializa_populacao(espacos,valores,limite)
# for individuo in ag.populacao:
#     individuo.avaliacao()
# ag.ordena_populacao()
# ag.melhor_individuo(ag.populacao[0])
# soma = ag.soma_avaliacoes()

# for individuo_gerados in range(0,ag.tamanho_populacao,2):
#     pai1 = ag.seleciona_pai(soma)
#     pai2= ag.seleciona_pai(soma)

#     print('***** Indivíduo %s *****\n' % pai1,
#           'Espaços = %s\n' % str(ag.populacao[pai1].espacos),
#           'Valores = %s\n' % str(ag.populacao[pai1].valores),
#           'Cromossomo = %s\n' % str(ag.populacao[pai1].cromossomo),
#           'Nota = %s\n' % str(ag.populacao[pai1].nota_avaliacao))

#     print('***** Indivíduo %s *****\n' % pai2,
#           'Espaços = %s\n' % str(ag.populacao[pai2].espacos),
#           'Valores = %s\n' % str(ag.populacao[pai2].valores),
#           'Cromossomo = %s\n' % str(ag.populacao[pai2].cromossomo),
#           'Nota = %s\n' % str(ag.populacao[pai2].nota_avaliacao))

#     input('espera....')




# #Final
tamanho_populacao = 20
taxa_mutacao = 0.01
numero_geracoes = 1000


ag = AlgoritmoGenetico(tamanho_populacao)
resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite)

for i in range(len(listaProdutos)):
    if resultado[i] == '1':
        print("Nome: %s R$ %s " % (listaProdutos[i].nome,
                                listaProdutos[i].valor))


#print(ag.lista_solucoes)

# plt.plot(ag.lista_solucoes)
# plt.title("Acompanhamento das melhores gerações")
# plt.show()