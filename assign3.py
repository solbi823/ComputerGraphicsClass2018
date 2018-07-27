


import math
import numpy as np
M= np.arange(2,27,1)

print(M)

M=M.reshape(5,5)
print(M)

M[1:4,1:4]=0
print(M)

M=np.dot(M,M)
print(M)

v=np.dot(M[0,0:5],M[0, 0:5])
v=math.sqrt(v)
print(v)
