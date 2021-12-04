import numpy as np

"""
Generete array of elements
28  39  52
77  80  66   
7   18  24    
9   97  68
"""
A = np.array([[28, 39, 52], [77, 80, 66], [7, 18, 24], [9, 97, 68]])

"""
Generete vetor of elements
1   
0   
2    
0
"""
B = np.array([1, 0, 2, 0])

cols = np.arange(A.shape[1])

mask = B[:, None] == cols

A[mask].reshape(-1, 2)

2+2

# Pruebas para seleccionar elementos de manera eficiente
max_row = np.amax(tmp, axis = 1)
mask = np.array(tmp)[None, :]  == np.array(max_row)[:, None]
prueba = np.ma.masked_array(tmp, mask)

# Evaluación Monsalve
# evaluate_population(population, table, memory, m)
suma_table = np.sum(table, axis = 1)
score1 = np.sum(population * suma_table[None, None, :], axis = 2)
table_invert = np.where(np.array(table) > 0.5, 0, 1)
suma_table_invert = np.sum(table_invert, axis = 1)
population_invert = np.where(np.array(population) > 0.5, 0, 1)
score2 = np.sum(population_invert * suma_table_invert[None, None, :], axis = 2)