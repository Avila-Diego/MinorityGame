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