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


def position_straegy(table, memory):
    """
    Position a strategy in the table.
    """
    return np.argmax(np.sum(np.array(table) == memory, axis = 1))

def forecast_strategy_full(population, table, memory):
    """
    Predicts the strategy given a memory of size m
    """
    position = position_straegy(table, memory)
    return population[:, :, position]

def score(population, table, memory):
    """
    Compute the score of a strategy with a memory.
    """
    forecast = forecast_strategy_full(population, table, memory)
    realization = memory
    tmp  = forecast == realization
    return True

def update_score(score_strategy, group_select, win_group, interaction, s):
    """
    Evaluate a population with a memory.
    """
    tmp = group_select == win_group
    score_strategy[:,interaction%s] = tmp.astype(int)
    return score_strategy

def select_strategy(score_strategy):
    tmp = pd.DataFrame(score_strategy)
    max_row = tmp.max(axis = 1)
    array_strategy = []
    for i_agent in range(len(max_row)):
        i_strategy = np.random.choice(tmp.loc[i_agent][tmp.loc[i_agent] == max_row[i_agent]].index.values)
        array_strategy.append(i_strategy)
    return array_strategy


def select_group(memory, population, table, score_strategy):
    """
    Select a group of strategies.
    """
    strategy_select = select_strategy(score_strategy)
    sample_population = population[:, :, position_straegy(table, memory)]
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
    return np.append(memory[-((m)-1):], win_group)

np.random.seed(20211130)
N = 101
m_max = 16
s = 2
n_interaction = 1000
max_simulation = 40

for m in range(1, m_max + 1):
    print("Memory: ", m)
    result = pd.DataFrame(columns=[
        'Simulation', 'Iteration', 'Population', 'LenMemory',
        'NumberStrategy', 'MinorityGroup', 
        'n_wins', 'StandarDeviation'])

    for simulation in range(max_simulation):
        print('Simulation: ', simulation)
        memory = np.random.randint(2, size=m)
        population = generate_population(N, s, m)
        table = table_strategy(m)
        score_strategy = np.array(np.zeros((N, s)))
        # puntuacion = np.zeros(N)

        for interaction in range(n_interaction):
            group_select = select_group(memory, population, table, score_strategy)
            win_group = group_minoritary(group_select)
            # puntuacion = update_puntuacion(win_group, puntuacion)
            score_strategy = update_score(score_strategy, group_select, win_group, interaction, s)
            win_group, std_group_select, n_wins = summary_round(group_select)
            memory = update_memory(memory, win_group, m)

            result = result.append({
                'Simulation': simulation+1,
                'Iteration': interaction+1,
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
            './Result_CalculoEstrategia/Minority_game_N_' + str(N) + '_m_' + str(m) + '_s_' + str(s) + '.csv',
            index=False)
        # pd.DataFrame(puntuacion).to_csv(
        #     './Result_CalculoEstrategia/Minority_game_N_' + str(N) + '_m_' + str(m) + '_s_' + str(s) + '_puntuation.csv',
        #     index=False)

    result.to_csv('./Result_CalculoEstrategia/Minority_game_N_' + str(N) + '_m_' + str(m) + '_s_' + str(s) + '.csv', index=False)
    # pd.DataFrame(puntuacion).to_csv('./Result_CalculoEstrategia/Minority_game_N_' + str(N) + 
    # '_m_' + str(m) + '_s_' + str(s) + '_puntuation.csv', index=False)
