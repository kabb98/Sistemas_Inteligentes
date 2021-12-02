import matplotlib.pyplot as plt
import numpy as np
def mostrar_imagen(imagen):
    plt.figure()
    plt.imshow(imagen)
    plt.show()

def adaptar_conjuntos(mnist_X, mnist_Y):
    X = mnist_X.reshape(60000, 784)
    print(X.shape)
    return (X, mnist_Y)

def crea_conjunto_entrenamiento(X, Y, item):
    conjuntoX = []
    conjuntoY = []
    
    #Tamaño 600 de los conjuntos
    tam = len(X)//100
    
    for i in range(0, tam):
        if Y[i] == item:
            conjuntoX.append(X[i])
            conjuntoY.append(True)
        elif Y[i] != item:
            conjuntoX.append(X[i])
            conjuntoY.append(False)

    return (conjuntoX, conjuntoY)
            
            

def plot_arrays(X, Y, title):
    plt.title(title)
    plt.plot(X, Y)
    plt.show()