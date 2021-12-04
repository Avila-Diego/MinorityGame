"""
THE MINORITY GAME

The minority game model is a game in which players try to win by 
choosing the group with the fewest people. This requires an odd
number of players.

The minimum parameters of the model are:
    N: number of players (odd)
    m: memory logintud
    s: number of strategies of each player

Additionally we define:
    n_predict: number of predictions in time
    n_simulation: number of simulations 

Acá el criterio de decisión es el de califcar ada una de las propuestas según el criterio propuesto por Sergio Monsalve.
"""
import numpy as np
import pandas as pd

def generate_population(N, s, m):
    """
    Generate a population of N agents with s strategies and m memory.
    """
    if N%2 == 0:
        raise ValueError("N must be odd.")
    else:
        return np.random.randint(2, size=(N, s, 2**m))

def generete_memory(m):
    """
    Generate a memory of size 2*m
    A vector of size 2*m is generated with 0 and 1 randomly.
    """
    return np.random.randint(2, size=2*m)

def product(*args, repeat=1):
    """
    Extracted from the library: itertools
    """
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

def table_strategy(m):
    """
    Generete table of strategies.
    Generates all possible combinations of 1 and 0 with m iterations
    """
    table = list(product([0,1], repeat=m))
    return table

def memory_last_time(memory, m, time):
    """
    Returns the last m elements of the memory element with a
    time delay.
    """
    if time == 0:
        return memory[-m:]
    else:
        return memory[-m-time:-time]

def position_straegy(table, memory, m, time):
    """
    Position a strategy in the table.
    """
    boleano = max(np.sum(table == memory_last_time(memory, m, time), axis = 1))  ==  np.sum(table == memory_last_time(memory, m, time), axis = 1)
    return boleano.tolist().index(True)
            

def forecast_strategy_full(population, table, memory, m, time):
    """
    Predicts the strategy given a memory of size m
    """
    position = position_straegy(table, memory, m, time)
    return population[:, :, position]

def score(population, table, memory, m, time):
    """
    Compute the score of a strategy with a memory.
    """
    forecast = forecast_strategy_full(population, table, memory, m, time)
    realization = memory[-time]
    tmp  = forecast == realization
    return tmp.astype(int)

def evaluate_population(population, table, memory, m):
    """
    Evaluate a population with a memory.
    """
    suma_table = np.sum(table, axis = 1)
    score1 = np.sum(population * suma_table[None, None, :], axis = 2)
    table_invert = np.where(np.array(table) > 0.5, 0, 1)
    suma_table_invert = np.sum(table_invert, axis = 1)
    population_invert = np.where(np.array(population) > 0.5, 0, 1)
    score2 = np.sum(population_invert * suma_table_invert[None, None, :], axis = 2)
    return score1 + score2

def select_strategy(m, memory, population, table):
    tmp = evaluate_population(population, table, memory, m)
    tmp = pd.DataFrame(tmp)
    max_row = tmp.max(axis = 1)
    array_strategy = []
    for i_agent in range(len(max_row)):
        i_strategy = np.random.choice(tmp.loc[i_agent][tmp.loc[i_agent] == max_row[i_agent]].index.values)
        array_strategy.append(i_strategy)
    return array_strategy

def select_group(m, memory, population, table):
    """
    Select a group of strategies.
    """
    strategy_select = select_strategy(m, memory, population, table)
    sample_population = population[:, :, position_straegy(table, memory, m, time = 0)]
    cols = np.arange(sample_population.shape[1])
    mask = np.array(strategy_select)[:, None] == cols
    return sample_population[mask]

def group_minoritary(group_select):
    if group_select.sum() > len(group_select)/2:
        return 0
    else:
        return 1

def update_puntuacion(win_group, puntuacion):
    i_puntuacion = group_select == win_group
    i_puntuacion = i_puntuacion.astype(int)
    return puntuacion + i_puntuacion

def summary_round(group_select):
    """
    Statistical summary of the round.
    """
    std_group_select = np.std(group_select)
    win_group = group_minoritary(group_select)
    n_wins = np.sum(group_select == win_group)
    return win_group, std_group_select, n_wins

def update_memory(memory, win_group, m):
    """
    Update the memory.
    """
    return np.append(memory[-((m*2)-1):], win_group)


np.random.seed(20211130)
N = 101
m_max = 16
s = 2
n_interation = 1000
max_simulation = 40

# m = 3
# interation = 1
# simulation = 1

# print("Memory: ", m)
# result = pd.DataFrame(columns=[
#     'Simulation', 'Iteration', 'Population', 'LenMemory',
#     'NumberStrategy', 'MinorityGroup', 
#     'n_wins', 'StandarDeviation'])

# print('Simulation: ', simulation)
# memory = generete_memory(m)
# table = table_strategy(m)
# puntuacion = np.zeros(N)

# population = generate_population(N, s, m)
# group_select = select_group(m, memory, population, table)
# win_group = group_minoritary(group_select)
# puntuacion = update_puntuacion(win_group, puntuacion)
# win_group, std_group_select, n_wins = summary_round(group_select)
# memory = update_memory(memory, win_group, m)

# result = result.append({
#     'Simulation': simulation+1,
#     'Iteration': interation+1,
#     'Population': N,
#     'LenMemory': m,
#     'NumberStrategy': s,
#     'MinorityGroup': win_group,
#     'n_wins': n_wins,
#     'StandarDeviation': std_group_select,
#     },
#     ignore_index=True
#     )

# 2+2

for m in range(2, m_max + 1):
    print("Memory: ", m)
    result = pd.DataFrame(columns=[
        'Simulation', 'Iteration', 'Population', 'LenMemory',
        'NumberStrategy', 'MinorityGroup', 
        'n_wins', 'StandarDeviation'])

    for simulation in range(max_simulation):
        print('Simulation: ', simulation)
        memory = generete_memory(m)
        table = table_strategy(m)
        puntuacion = np.zeros(N)

        for interation in range(n_interation):
            population = generate_population(N, s, m)
            group_select = select_group(m, memory, population, table)
            win_group = group_minoritary(group_select)
            puntuacion = update_puntuacion(win_group, puntuacion)
            win_group, std_group_select, n_wins = summary_round(group_select)
            memory = update_memory(memory, win_group, m)

            result = result.append({
                'Simulation': simulation+1,
                'Iteration': interation+1,
                'Population': N,
                'LenMemory': m,
                'NumberStrategy': s,
                'MinorityGroup': win_group,
                'n_wins': n_wins,
                'StandarDeviation': std_group_select,
                },
                ignore_index=True
                )

        result.to_csv(
            './result_RemplazoReglaM//Minority_game_N_' + str(N) + '_m_' + str(m) + '_s_' + str(s) + '.csv',
            index=False)
        pd.DataFrame(puntuacion).to_csv(
            './result_RemplazoReglaM//Minority_game_N_' + str(N) + '_m_' + str(m) + '_s_' + str(s) + '_puntuation.csv',
            index=False)

    result.to_csv('./result_RemplazoReglaM//Minority_game_N_' + str(N) + '_m_' + str(m) + '_s_' + str(s) + '.csv', index=False)
    pd.DataFrame(puntuacion).to_csv('./result_RemplazoReglaM//Minority_game_N_' + str(N) + '_m_' + str(m) + '_s_' + str(s) + '_puntuation.csv', index=False)

