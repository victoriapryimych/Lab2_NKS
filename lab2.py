import itertools as it
from math import log, factorial

import networkx as nx
import numpy as np

link_matrix = [[0, 0, 1, 1, 0, 0, 0],
               [0, 0, 1, 0, 1, 0, 1],
               [0, 0, 0, 1, 1, 0, 1],
               [0, 0, 0, 0, 1, 1, 0],
               [0, 0, 0, 0, 0, 1, 1],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]]
probabilities = [0.56, 0.79, 0.32, 0.53, 0.40, 0.71, 0.02]
start_nodes = [1, 2]
end_nodes = [6, 7]

T = 2061
K = 1


def lab2(probabilities, link_matrix):
    for p in probabilities:
        if p <= 0 or p > 1:
            print("Ймовірність має бути в межах від 0 до 1, не включаючи 0")
            exit(1)
    if len(link_matrix) != len(link_matrix[0]):
        print("Матриця зв'язків системи має бути квадратною")
        exit(1)
    for i in link_matrix:
        for j in i:
            if j != 1 and j != 0:
                print("Значення елементів матриці зв'язків системи може бути 0 або 1")
                exit(1)

    a = np.asarray(link_matrix)
    graph = nx.DiGraph(a)
    path_list = []
    for start_node in start_nodes:
        for end_node in end_nodes:
            for path in nx.all_simple_paths(graph, source=start_node - 1, target=end_node - 1):
                path_list.append(path)
    '''print('Усі можливі шляхи, якими можна пройти від початку до кінця схеми:')
    for path in path_list:
        print([n + 1 for n in path])'''

    all_states = [list(state) for state in it.product(range(2), repeat=len(link_matrix))]
    working_states = []
    for state in all_states:
        for path in path_list:
            count = 0
            for n in path:
                if state[n] == 1:
                    count += 1
            if count == len(path):
                working_states.append(state)
                break

    working_states_prob = []
    for state in working_states:
        state_prob = 1
        for i in range(len(state)):
            if state[i] == 0:
                state_prob *= 1 - probabilities[i]
            else:
                state_prob *= probabilities[i]
        working_states_prob.append(state_prob)
    '''print("Усі працездатні стани системи з ймовірностями знаходження в цих станах:")
    print("Вершини" + " " * 17 + "Ймовірність")
    list(map(lambda x, y, z: print(x, y, z), working_states, "  " * len(working_states), working_states_prob))'''
    sys_prob = sum(working_states_prob)
    # print("P = {}".format(sys_prob))
    return sys_prob


def reliability_gains(p_sys, q_sys, t_sys, p_res, q_res, t_res):
    g_q = q_res / q_sys
    g_p = p_res / p_sys
    g_t = t_res / t_sys
    print("Виграш надійності за ймовірністю відмов = {}\n"
          "Виграш надійності за ймовірністю безвідмовної роботи = {}\n"
          "Виграш надійності за середнім часом безвідмовної роботи = {}\n".format(g_q, g_p, g_t))


def separate_unloaded(t, k, p_sys, q_sys, t_sys):
    reserved_probabilities = list(map(lambda x: 1 - (1 - x) ** (k + 1) / factorial(k + 1), probabilities))
    p_res = lab2(reserved_probabilities, link_matrix)
    q_res = 1 - p_res
    t_res = -t / log(p_res)
    print("Для системи із роздільним ненавантаженим резервуванням\n"
          "Ймовірність безвідмовної роботи = {}\n"
          "Ймовірність відмови = {}\n"
          "Середній час безвідмовної роботи = {}".format(p_res, q_res, t_res))
    reliability_gains(p_sys, q_sys, t_sys, p_res, q_res, t_res)


def separate_loaded(t, k, p_sys, q_sys, t_sys):
    reserved_probabilities = list(map(lambda x: 1 - (1 - x) ** (k + 1), probabilities))
    p_res = lab2(reserved_probabilities, link_matrix)
    q_res = 1 - p_res
    t_res = -t / log(p_res)
    print("Для системи із роздільним навантаженим резервуванням\n"
          "Ймовірність безвідмовної роботи = {}\n"
          "Ймовірність відмови = {}\n"
          "Середній час безвідмовної роботи = {}".format(p_res, q_res, t_res))
    reliability_gains(p_sys, q_sys, t_sys, p_res, q_res, t_res)


def general_unloaded(t, k, p_sys, q_sys, t_sys):
    q_res = pow(q_sys, (k + 1)) / factorial(k + 1)
    p_res = 1 - q_res
    t_res = -t / log(p_res)
    print("Для системи із загальним ненавантаженим резервуванням\n"
          "Ймовірність безвідмовної роботи = {}\n"
          "Ймовірність відмови = {}\n"
          "Середній час безвідмовної роботи = {}".format(p_res, q_res, t_res))
    reliability_gains(p_sys, q_sys, t_sys, p_res, q_res, t_res)


def general_loaded(t, k, p_sys, q_sys, t_sys):
    q_res = pow(q_sys, (k + 1))
    p_res = 1 - q_res
    t_res = -t / log(p_res)
    print("Для системи із загальним навантаженим резервуванням\n"
          "Ймовірність безвідмовної роботи = {}\n"
          "Ймовірність відмови = {}\n"
          "Середній час безвідмовної роботи = {}".format(p_res, q_res, t_res))
    reliability_gains(p_sys, q_sys, t_sys, p_res, q_res, t_res)


p_sys = lab2(probabilities, link_matrix)
q_sys = 1 - p_sys
t_sys = -T / log(p_sys)
print("Для системи без резервування\n"
      "Ймовірність безвідмовної роботи = {}\n"
      "Ймовірність відмови = {}\nСередній наробіток до відмови = {}\n".format(p_sys, q_sys, t_sys))

separate_unloaded(T, K, p_sys, q_sys, t_sys)
separate_loaded(T, K, p_sys, q_sys, t_sys)
