# Importamos las librerias que necesitaremos
import numpy as np
import matplotlib.pyplot as plt
import utils
import adaboost
import clasificador_debil as cd

# Cargamos la base de datos
npzfile = np.load("mnist.npz")
mnist_X = npzfile['x']
mnist_Y = npzfile['y']


#Adaptar los conjuntos X e Y a AdaBoost
(X, Y) = utils.adaptar_conjuntos(mnist_X, mnist_Y)

# Lanzar Adaboost
T = 20
A = 50


(pruebaX, pruebaY) = utils.crea_conjunto_entrenamiento(X, Y, 0)

#Entrenamos
(Hx, alphas) = adaboost.entrenar(pruebaX, pruebaY, T, A)


resultado = np.ones(len(X)//100)
posiciones = np.zeros(len(X)//100)
for idx in range(0, len(X)//100):
    sumatorio = 0
    for deb in Hx:
        sumatorio = sumatorio + deb.confianza * 1 if cd.aplicar_clasificador_debil(deb, X[idx]) else -1
    if sumatorio > 0:
        resultado[idx] =  1
    else:
        resultado[idx] = -1
    posiciones[idx] = idx

for idx, val in enumerate(resultado):
    pass#print("Pos: ", posiciones[idx], ", val: ", val)

total = np.count_nonzero(resultado == 1)

print("Total ceros con el algoritmo en los 600 primeros numeros: ", total)
cont = 0
for idx in range(0, 600):
    if Y[idx] == 0:
        cont = cont + 1

print("Hay ", cont, " ceros en los primeros 600 numeros")
utils.mostrar_imagen(mnist_X[0])
# Analisis y resultados de las pruebas realizadas
T = [0, 100, 200, 300, 400]      # Numero de clasificadores 
resultados = [0, 20, 35, 56, 68] # Resultados obtenidos de clasificacion
#utils.plot_arrays(T, resultados, "Porcentajes con valores de T")