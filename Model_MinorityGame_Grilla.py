"""
Minority game program on a grid.
"""

# Import libraries
import numpy as np
import pandas as pd

global history, avg_score, stdev_score, turtles, current_strategy, score, strategies_scores, choice, minority, strategies_per_agent, number_of_agents, number_of_agents_x, memory, num_picked_zero

def initialize_system():
    global history, avg_score, stdev_score, memory, number_of_agents, number_of_agents_x
    number_of_agents = number_of_agents_x ** 2
    history = np.random.randint(2 ** memory, size = number_of_agents)
    avg_score = 0
    stdev_score = 0
    return True

def create_strategy():
    global memory
    return np.random.randint(2, size = 2 ** memory)

def assign_strategies():
    global strategies_per_agent
    strategies_local = []

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
    global turtles, current_strategy, history, choice, number_of_agents
    
    choice = []
    for i in range(number_of_agents):
        choice.append(turtles[i, current_strategy[i], history[i]])
        
    return True

def update_system():
    global choice, number_of_agents_x, score, minority, avg_score, stdev_score, num_picked_zero
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
    update_history()
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
    score = score + (choice == np.repeat(minority, len(choice)))

    return True

def MinorityGroupIs(list):
    if sum(list) == len(list)/2:
        list = list[-(len(list)-1):]
    if sum(list) < len(list)/2:
        return 1
    else:
        return 0
    
def fMinority_local(i):
    global minority_local, number_of_agents_x, number_of_agents, choice
    choice_tmp = [choice[i]]
    # If it is one end of the frame then
    if i == 0:
        choice_tmp.append(choice[i+1])
        choice_tmp.append(choice[i+number_of_agents_x])
        choice_tmp.append(choice[i+number_of_agents_x+1])
    elif i == number_of_agents - 1:
        choice_tmp.append(choice[i-1])
        choice_tmp.append(choice[i-number_of_agents_x])
        choice_tmp.append(choice[i-number_of_agents_x-1])
    elif i == number_of_agents_x - 1:
        choice_tmp.append(choice[i-1])
        choice_tmp.append(choice[i+number_of_agents_x])
        choice_tmp.append(choice[i+number_of_agents_x-1])
    elif i == number_of_agents - number_of_agents_x:
        choice_tmp.append(choice[i+1])
        choice_tmp.append(choice[i-number_of_agents_x])
        choice_tmp.append(choice[i-number_of_agents_x+1])
    elif i > 0 and i < number_of_agents_x - 1:
        choice_tmp.append(choice[i-1])
        choice_tmp.append(choice[i+1])
        choice_tmp.append(choice[i-1+number_of_agents_x])
        choice_tmp.append(choice[i + number_of_agents_x])
        choice_tmp.append(choice[i+1+number_of_agents_x])
    elif i > number_of_agents - number_of_agents_x and i < number_of_agents - 1:
        choice_tmp.append(choice[i-1])
        choice_tmp.append(choice[i+1])
        choice_tmp.append(choice[i-1-number_of_agents_x])
        choice_tmp.append(choice[i - number_of_agents_x])
        choice_tmp.append(choice[i+1-number_of_agents_x])
    elif i % number_of_agents_x == 0:
        choice_tmp.append(choice[i+1])
        choice_tmp.append(choice[i-number_of_agents_x])
        choice_tmp.append(choice[i-number_of_agents_x+1])
        choice_tmp.append(choice[i+number_of_agents_x])
        choice_tmp.append(choice[i+number_of_agents_x+1])
    elif (i + 1) % number_of_agents_x == 0:
        choice_tmp.append(choice[i-1])
        choice_tmp.append(choice[i-number_of_agents_x])
        choice_tmp.append(choice[i-number_of_agents_x-1])
        choice_tmp.append(choice[i+number_of_agents_x])
        choice_tmp.append(choice[i+number_of_agents_x-1])
    else:
        choice_tmp.append(choice[i-1])
        choice_tmp.append(choice[i+1])
        choice_tmp.append(choice[i-number_of_agents_x])
        choice_tmp.append(choice[i-number_of_agents_x+1])
        choice_tmp.append(choice[i-number_of_agents_x-1])
        choice_tmp.append(choice[i+number_of_agents_x])
        choice_tmp.append(choice[i+number_of_agents_x+1])
        choice_tmp.append(choice[i+number_of_agents_x-1]) 
    return MinorityGroupIs(choice_tmp)
    


def increment_scores():
    global turtles, strategies_scores, minority_local, history
    # tmp = turtles[:,:,history] == minority
    minority_local = []
    for i in range(number_of_agents):
        minority_local.append(fMinority_local(i))
        
    for i in range(number_of_agents):
        strategies_scores[i] = strategies_scores[i] + (minority_local[i] == turtles[i,:,3])
        
    return True

def binary(decimal_num):
    global memory
    binary_num = format(decimal_num, 'b')
    while len(binary_num) < memory:
        binary_num = '0' + binary_num
    return binary_num

def update_history():
    global history, memory
    for i in range(memory):
        history[i] = int(binary(history[i])[-(memory-1):] + str(minority_local[i]), 2)
    return True

memory = 2
number_of_agents_x = 11
strategies_per_agent_max = 11
memory_max = 2
n_interaction = 1000
max_simulation = 15

result = pd.DataFrame(columns=[
    'Simulation', 'Iteration', 'Population',
    'LenMemory', 'NumberStrategy', 'MinorityGroup',
    'n_zeros', 'StandarDeviation', 'max_score',
    'avg_score', 'min_score', 'max_for_time_score',
    'avg_for_time_score', 'min_for_time_score'])

for strategies_per_agent in range(2, strategies_per_agent_max+1):
    print(' strategies_per_agent: ', strategies_per_agent)
    
    for simulation in range(max_simulation):
        print(' simulation: ', simulation)
        setup()

        for interaction in range(n_interaction):
            if interaction % 500 == 0:
                print(' interaction: ', interaction)
                
            go()

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
        result.to_csv('ReplicateNetLogo_Result_N' + str(number_of_agents_x) + '_s_' + str(strategies_per_agent) + '.csv', index=False)
