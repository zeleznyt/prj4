import matplotlib.pyplot as plt
import numpy as np

src_matrix = np.arange(100)
result_matrix = np.zeros((20, 100))

for i in range(np.size(result_matrix, 0)):
    result_matrix[i, :] = np.sin(src_matrix * 0.1 * i) + i

plt.plot(np.transpose(result_matrix))
plt.show()