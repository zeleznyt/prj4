import numpy as np
import matplotlib.pyplot as plt

def funkce(x):
    return np.sin(x)

if __name__ == '__main__':
    Y = np.zeros((20, 100))
  
    for i in range(20):
        vektor = funkce((np.array(range(100))*0.1)*(i))+i
        Y[i,:] = vektor

    plt.plot(Y.transpose())
    plt.show()
