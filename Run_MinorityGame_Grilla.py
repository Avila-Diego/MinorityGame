
import pandas as pd
import Model_MinorityGame_Grilla as MMG

# s_group = range(2, 3) # (2, 3, 4, 5, 6)
memory = 2
number_of_agents_x = 11
strategies_per_agent = 2
memory_max = 2
n_interaction = 1000
max_simulation = 10

result = pd.DataFrame(columns=[
    'Simulation', 'Iteration', 'Population',
    'LenMemory', 'NumberStrategy', 'MinorityGroup',
    'n_zeros', 'StandarDeviation', 'max_score',
    'avg_score', 'min_score', 'max_for_time_score',
    'avg_for_time_score', 'min_for_time_score'])

for simulation in range(max_simulation):
    print(' simulation: ', simulation)
    MMG.setup()

    for interaction in range(n_interaction):
        MMG.go()
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
    result.to_csv('ReplicateNetLogo_Result_N' + str(number_of_agents_x) + '_s_' + str(strategies_per_agent) + '.csv', index=False)
