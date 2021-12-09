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

def generate_population(N_gp, s_gp, m_gp):
    """
    Generate a population of N agents with s strategies and m memory.
    """
    if N_gp%2 == 0:
        raise ValueError("N must be odd.")
    else:
        prueba = []
        population = np.random.randint(2, size=(N_gp, s_gp, 2**m_gp))
        for i_pop in range(population.shape[0]):
            while np.array_equal(population[i_pop, 0, :], population[i_pop, 1, :]):
                population[i_pop, 1, :] = np.random.randint(2, size=2**m_gp)
        return population

def product(*args, repeat):
    """
    Extracted from the library: itertools
    """
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

def table_strategy(m_ts):
    """
    Generete table of strategies.
    Generates all possible combinations
    of 1 and 0 with m iterations
    """
    return np.asarray(list(product([0,1], repeat=m_ts)))

def position_straegy(table_ps, memory_ps):
    """
    Position a strategy in the table.
    """
    return np.argmax(np.sum(table_ps == memory_ps, axis = 1))

def forecast_strategy_full(population_fsf, table_fsf, memory_fsf):
    """
    Predicts the strategy given a memory of size m
    """
    return population_fsf[:, :, position_straegy(table_fsf, memory_fsf)]

def select_strategy(score_strategy_ss):
    tmp = np.random.rand(score_strategy_ss.shape[0], score_strategy_ss.shape[1])
    tmp = tmp + score_strategy_ss
    return np.argmax(tmp, axis = 1)

def select_group(memory_sg, population_sg, table_sg, score_strategy_sg):
    """
    Select a group of strategies.
    """
    strategy_select = select_strategy(score_strategy_sg)
    sample_population_sg = population_sg[:, :, position_straegy(table_sg, memory_sg)]
    cols = np.arange(sample_population_sg.shape[1])
    mask = np.array(strategy_select)[:, None] == cols
    return sample_population_sg[mask]

def group_minoritary(group_select_gm):
    if group_select_gm.sum() > len(group_select_gm)/2:
        return 0
    else:
        return 1

def update_puntuacion(win_group_up, puntuacion_up, group_select_up):
    i_puntuacion = group_select_up == win_group_up
    i_puntuacion = i_puntuacion.astype(int)
    return puntuacion_up + i_puntuacion

def update_score(score_strategy_us, group_select_us, win_group_us, interaction_us, s_us):
    """
    Evaluate a population with a memory.
    """
    score_strategy_us_tmp = score_strategy_us.copy()
    tmp = group_select_us == win_group_us
    score_strategy_us_tmp[:,interaction_us%s] = score_strategy_us_tmp[:,interaction_us%s] + tmp.astype(int)
    # score_strategy_us_tmp[:,interaction_us%s_us] = tmp.astype(int)
    return score_strategy_us_tmp

def summary_round(group_select_sr):
    """
    Statistical summary of the round.
    """
    std_group_select_sr = np.std(group_select_sr)
    win_group = group_minoritary(group_select_sr)
    n_wins = np.sum(group_select_sr == win_group)
    return win_group, std_group_select_sr, n_wins

def update_memory(memory_um, win_group_um, m_um):
    """
    Update the memory.
    """
    return np.append(memory_um[-((m_um)-1):], win_group_um)

np.random.seed(20211130)
N_group = range(101, 102) # (11, 101, 1001, 10001, 100001)
m_max = 15
s_group = range(2, 3) # (2, 3, 4, 5, 6)
n_interaction = 500
max_simulation = 30

for N in N_group:
    print("N =", N)
    for s in s_group:
        print("  s =", s)
        for m in range(2, m_max + 1):
            print("    m: ", m)
            result = pd.DataFrame(columns=[
                'Simulation', 'Iteration', 'Population', 'LenMemory',
                'NumberStrategy', 'MinorityGroup',
                'n_wins', 'StandarDeviation'])

            for simulation in range(max_simulation):
                print('       simulation: ', simulation)
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

            result.to_csv('./Result_CalculoEstrategia/N_' + str(N) + '_s_' + str(s) + '/Minority_game_N_' + str(N) + '_m_' + str(m) + '_s_' + str(s) + '.csv', index=False)