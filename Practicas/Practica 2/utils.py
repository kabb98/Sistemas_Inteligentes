import matplotlib.pyplot as plt

import numpy as np
def mostrar_imagen(imagen):
    plt.figure()
    plt.imshow(imagen)
    plt.show()

def adaptar_conjuntos(mnist_X, mnist_Y):
    X = mnist_X.reshape(60000, 784)
    return (X, mnist_Y)

def split_train_validation_set(X, Y):
    #Usaremos 80% para train, 20% para validation
    #Luego sacar el 50% de num y otro 50% de aleatorio -> Tanto para train como validation
    
    print(X.shape)
    N = int(0.8*len(X))
    X_Train = X[0:N]
    X_Validation = X[N:len(X)]

    Y_Train = Y[0:N]
    Y_Validation = Y[N:len(X)]

    

    return (X_Train, X_Validation, Y_Train, Y_Validation)

def creaConjunto(X, Y, num):
    filtro = (Y == num)
    zeros = np.count_nonzero(filtro)
    print("Zeros: ", zeros*2)
    indices = np.where(filtro)
    filtroDistinto = np.invert(filtro)
    
    Y_Izq = Y[indices]
    Y_Der = Y[np.where(filtroDistinto)]
    Y_Der = Y_Der[:zeros]
    
    X_Izq = X[indices]
    X_Der = X[np.where(filtroDistinto)]
    X_Der = X_Der[:zeros]

    
    X_res = np.concatenate((X_Izq, X_Der), axis=0)
    Y_res = np.concatenate((Y_Izq, Y_Der), axis=0)
    return (X_res, Y_res)
    
    
def addaptForTraining(Y, num):
    for n in Y:
        if n == num:
            n = 1
        else:
            n = -1
    return Y

def plot_arrays(X, Y, title):
    plt.title(title)
    plt.plot(X, Y)
    plt.show()