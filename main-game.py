# # # Função para recuperar os logs salvos da ultima geração para rodar o jogo
# Cromossomo = [6, 5, 1, 2, 3, 2, 0, 6, 3, 3, 5, 5, 4, 4, 4, 5, 4, 3, 6, 1, 4, 1, 1, 3, 3, 6, 5, 2, 3, 5, 3, 6, 5, 3, 2, 3, 0, 2, 4, 6, 4, 3, 4, 2, 3, 6, 0, 0, 2, 0, 1, 0, 2, 2, 5, 3, 4, 6, 4, 3, 6, 2, 6, 0, 4, 1, 0, 5, 0, 0, 2, 0, 4, 6, 3, 2, 5, 2, 4, 4, 0, 3, 2, 0, 6, 0, 4, 3, 1, 3, 4, 1, 0, 4, 5, 5, 6, 6, 0, 0]
# #
# # from nes_py.wrappers import JoypadSpace
# # import gym_super_mario_bros
# # from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
# # env = gym_super_mario_bros.make('SuperMarioBros-v0')
# # env = JoypadSpace(env, SIMPLE_MOVEMENT)
# #
# # done = True
# # for step in range(5000):
# #     for indice in Cromossomo:
# #         for action in SIMPLE_MOVEMENT:
# #             if indice == action:
# #                 actions = action
# #                 if done:
# #                     state = env.reset()
# #                 state, reward, done, info = env.step(env.action_space.sample())
# #                 print(info)
# #                 env.render()
# #
# # env.close()
#
# from nes_py.wrappers import JoypadSpace
# import gym_super_mario_bros
# from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
# env = gym_super_mario_bros.make('SuperMarioBros-1-2-v0')
# env = JoypadSpace(env, SIMPLE_MOVEMENT)
#
# done = True
# for step in range(5000):
#     if done:
#         state = env.reset()
#     actions = env.action_space.sample()
#     state, reward, done, info = env.step(actions)
#     print(info)
#     env.render()
#
# env.close()