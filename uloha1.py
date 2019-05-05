import numpy as np
import matplotlib.pyplot as plt
import os

def funkce(x):
    return np.sin(x)

def saveStr(Y, filepath):

    fout = open(filepath, 'w',encoding = 'UTF-8')
    for i in range(20):
        for j in range(100):
            fout.write(str(Y[i,j]))
            fout.write(' ')
    fout.close()

def loadStr(filepath):
    Y = np.zeros((20, 100))
    fin = open(filepath, 'r', encoding = 'UTF-8')
    splitted = fin.read().strip().split(' ')
    for i in range(20):
        for j in range(100):
            Y[i,j] = splitted[j+i*100]
    fin.close()
    return(Y)

if __name__ == '__main__':
    
    # Vytvoreni matice
    Y = np.zeros((20, 100))
    for i in range(20):
        vektor = funkce((np.array(range(100))*0.1)*(i))+i
        Y[i,:] = vektor

    # Jako text
    filepathStr = os.path.join(os.path.dirname(__file__), 'dataStr.txt') # Cesta do stejného adresáře jako skript
    saveStr(Y, filepathStr)
    plt.plot(loadStr(filepathStr).transpose())
    plt.show()
    # numpy save
    filepath = os.path.join(os.path.dirname(__file__), 'data.npy')
    np.save(filepath, Y)
    plt.plot(np.load(filepath).transpose())
    plt.show()