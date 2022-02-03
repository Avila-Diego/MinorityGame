"""
Program replicate the NetLogo model of Minority Game.
"""

# Import libraries
import numpy as np
import pandas as pd

global history, avg_score, stdev_score, turtles, current_strategy, score, strategies_scores, choice, minority, strategies_per_agent, number_of_agents, memory, num_picked_zero

def initialize_system():
    global history, avg_score, stdev_score, memory
    history = np.random.randint(2 ** memory)
    avg_score = 0
    stdev_score = 0
    return True

def create_strategy():
    global memory
    return np.random.randint(2, size = 2 ** memory)

def assign_strategies():
    global strategies_per_agent
    strategies_local = []
    
    # for i in range(strategies_per_agent):
    #     tmp = create_strategy()
    #     strategies_local.append(tmp)
    #     while len(np.unique(strategies_local, axis = 0)) != len(strategies_local):
    #         tmp = create_strategy()
    #         strategies_local[i] = tmp

    strategies_tmp = np.random.choice(list(range(0,2 ** (2 ** memory))), size = strategies_per_agent, replace = False)
    for i in range(strategies_per_agent):
        tmp = np.array(list(map(int, str(format(strategies_tmp[i], 'b')))))
        while len(tmp) < 2 ** memory:
            tmp = np.insert(tmp, 0, 0)
        strategies_local.append(tmp)
    return np.array(strategies_local)


# global history, avg_score, stdev_score, turtles, current_strategy, score, strategies_scores, choice, minority
def initialize_turtles():
    global strategies_per_agent, number_of_agents, turtles, current_strategy, score, strategies_scores
    turtles = []
    for i in range(number_of_agents):
        tmp = assign_strategies()
        turtles.append(tmp)
    current_strategy = np.random.randint(strategies_per_agent, size = number_of_agents)
    score = np.zeros(number_of_agents)
    strategies_scores = np.zeros((number_of_agents, strategies_per_agent))
    turtles = np.array(turtles)
    return True

def select_strategy():
    global turtles, current_strategy, history, choice
    # choice_tmp = []
    # for i in range(turtles.shape[0]):
    #     choice_tmp.append(turtles[i, current_strategy[i], history])
    # choice = choice_tmp
    
    turtles_tmp = turtles[:, :, history]
    mask = np.arange(turtles.shape[1]) == current_strategy[:, None]
    choice = turtles_tmp[mask]
    return True

def update_system():
    global choice, number_of_agents, score, minority, avg_score, stdev_score, num_picked_zero
    num_picked_zero = number_of_agents - sum(choice)
    if num_picked_zero <= (number_of_agents - 1) / 2:
        minority = 0
    else:
        minority = 1
    avg_score = np.mean(score)
    stdev_score = np.std(score)
    return True

def setup():
    initialize_system()
    initialize_turtles()
    select_strategy()
    update_system()
    select_strategy()

def go():
    global history, minority, memory
    update_scores_and_strategy()
    history = int(binary(history)[-(memory-1):] + str(minority), 2)
    select_strategy()
    update_system()
    select_strategy()
    return True

def update_scores_and_strategy():
    global turtles, strategies_scores, minority, history, current_strategy, score
    increment_scores()

    tmp = np.random.rand(strategies_scores.shape[0], strategies_scores.shape[1])
    tmp = tmp + strategies_scores
    current_strategy =  np.argmax(tmp, axis = 1)
    # tmp = pd.DataFrame(strategies_scores)
    # max_row = tmp.max(axis = 1)
    # current_strategy = []
    # for i_agent in range(len(max_row)):
    #     i_strategy = np.random.choice(tmp.loc[i_agent][tmp.loc[i_agent] == max_row[i_agent]].index.values)
    #     current_strategy.append(i_strategy)

    # for i in range(turtles.shape[0]):
    #     if choice[i] == minority:
    #         score[i] += 1
    score = score + (choice == np.repeat(minority, len(choice)))

    return True

def increment_scores():
    global turtles, strategies_scores, minority, history
    tmp = turtles[:,:,history] == minority
    strategies_scores = strategies_scores + tmp
    return True

def binary(decimal_num):
    global memory
    binary_num = format(decimal_num, 'b')
    while len(binary_num) < memory:
        binary_num = '0' + binary_num
    return binary_num

# s_group = range(2, 3) # (2, 3, 4, 5, 6)
# memory = 2
# number_of_agents = 101
# strategies_per_agent = 2
memory_max = 16
n_interaction = 1000
max_simulation = 30

result = pd.DataFrame(columns=[
    'Simulation', 'Iteration', 'Population',
    'LenMemory', 'NumberStrategy', 'MinorityGroup',
    'n_zeros', 'StandarDeviation', 'max_score',
    'avg_score', 'min_score', 'max_for_time_score',
    'avg_for_time_score', 'min_for_time_score'])

for number_of_agents in (
    # 11, 25, 101, 1001
    # 25,
    35,
    51,
    75,
    # 101,
    301,
    601,
    # 1001,
    3001,
    6001,
    10001
    ):
    print('number_of_agents:', number_of_agents)
    for strategies_per_agent in (
        2,
        3,
        # 4,
        # 6,
        # 8,
        # 16
        ):
        print(' strategies_per_agent:', strategies_per_agent)
        for memory in range(2, memory_max + 1):
            print("  m: ", memory)

            if memory == 1 and strategies_per_agent > 4:
                raise ValueError("You need to increase the memory variable or\n decrease the strategies_per_agent variable")
                exit()

            if number_of_agents%2 == 0:
                raise ValueError("N must be odd.")

            for simulation in range(max_simulation):
                # print(' simulation: ', simulation)
                setup()
                
                for interaction in range(n_interaction):
                    go()
                    # print(minority, history)

                    result = result.append({
                        'Simulation': simulation+1,
                        'Iteration': interaction+1,
                        'Population': number_of_agents,
                        'LenMemory': memory,
                        'NumberStrategy': strategies_per_agent,
                        'MinorityGroup': minority,
                        'n_zeros': num_picked_zero,
                        'StandarDeviation': stdev_score,
                        'max_score': max(score),
                        'avg_score': avg_score,
                        'min_score': min(score),
                        'max_for_time_score': max(score) / n_interaction,
                        'avg_for_time_score': avg_score / n_interaction,
                        'min_for_time_score': min(score) / n_interaction
                        },
                        ignore_index=True
                        )
                result.to_csv('../Result_tmp/ReplicateNetLogo_Result_N' + str(number_of_agents) + '_s_' + str(strategies_per_agent) + '.csv', index=False)

            2+2
        result.to_csv('../Result_tmp/ReplicateNetLogo_Result_N_' + str(number_of_agents) + '_s_' + str(strategies_per_agent) + '.csv', index=False)