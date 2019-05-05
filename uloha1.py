import numpy as np
import matplotlib.pyplot as plt

def funkce(x):
    return np.sin(x)

if __name__ == '__main__':
    for i in range(20):
        matice = np.array(range(100))
        plt.plot(funkce((matice*0.1)*(i))+i)

    # pointa: plot umi pracovat se vstupem jako je matice, matice musi byt ve spravnem tvaru. 
    # plt.plot(Y)
    plt.show()
