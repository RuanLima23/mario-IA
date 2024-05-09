# from nes_py.wrappers import JoypadSpace
# import gym_super_mario_bros
# from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
#
# # Função para carregar os cromossomos da melhor geração a partir do arquivo de texto
# def carregar_melhor_geracao(nome_arquivo):
#     with open(nome_arquivo, 'r') as file:
#         melhor_geracao = []
#         for line in file:
#             cromossomo = line.strip().split(", ")
#             cromossomo = [int(action) for action in cromossomo]
#             melhor_geracao.append(cromossomo)
#     return melhor_geracao
#
# # Carregar a melhor geração
# melhor_geracao = carregar_melhor_geracao("log-1.txt")
#
# # Criar o ambiente do Super Mario Bros
# env = gym_super_mario_bros.make('uperMarioBros-1-2-v0')
# env = JoypadSpace(env, SIMPLE_MOVEMENT)
#
# # Iterar sobre os cromossomos da melhor geração e executar as ações no ambiente
# done = True
# for cromossomo in melhor_geracao:
#     if done:
#         state = env.reset()
#     for action in cromossomo:
#         state, reward, done, info = env.step(action)
#         env.render()
#
# env.close()

from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
env = gym_super_mario_bros.make('SuperMarioBros-1-2-v0')
env = JoypadSpace(env, SIMPLE_MOVEMENT)
print(SIMPLE_MOVEMENT)

movimentos = [1,1,1,1,1]
done = True
for step in range(8000):
    if done:
        state = env.reset()
    proximo_movimento = movimentos[step % len(movimentos)]

    state, reward, done, info = env.step(proximo_movimento)
    print(info)
    env.render()

env.close()