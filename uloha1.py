import numpy as np
import matplotlib.pyplot as plt

def funkce(x):
    return np.sin(x)

if __name__ == '__main__':
    Y = np.array([np.zeros(100)])
  
    for i in range(20):
        vektor = funkce((np.array(range(100))*0.1)*(i))+i
        Y =(np.append(Y, [vektor], axis=0))

    # pointa: plot umi pracovat se vstupem jako je matice, matice musi byt ve spravnem tvaru. 
    plt.plot(Y.transpose())
    plt.show()
