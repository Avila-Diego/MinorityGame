import pyreadr
import pandas as pd
import matplotlib as plt

# Load rds file
data = pyreadr.read_r('../Result_out/0_Result_NetLogo_Merge.rds')
data = pd.DataFrame(data[None])

data.columns
# Index(['Simulation', 'Iteration', 'Population', 'LenMemory', 'NumberStrategy',
#        'MinorityGroup', 'n_zeros', 'StandarDeviation', 'max_score',
#        'avg_score', 'min_score', 'max_for_time_score', 'avg_for_time_score',
#        'min_for_time_score'],
#       dtype='object')

# Group by LenMemory, Simulation and NumberStrategy generate a mean
data_mean = data.groupby(['LenMemory', 'Simulation', 'NumberStrategy']).mean()
# Group by LenMemory, Simulation and NumberStrategy generate a std
data_std = data.groupby(['LenMemory', 'Simulation', 'NumberStrategy']).std()
# Append data_mean_n_zeros and data_std_n_zeros
data_n_zeros = pd.concat([data_mean['n_zeros'], data_std['n_zeros']], axis=1)

# Plot data_n_zeros
plt.plot(data_n_zeros)

2+2
