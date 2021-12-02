# Importamos las librerias que necesitaremos
import numpy as np
import matplotlib.pyplot as plt

import clasificador_debil as cd
import adaboost
import utils

# Cargamos la base de datos
npzfile = np.load("mnist.npz")
mnist_X = npzfile['x']
mnist_Y = npzfile['y']


#Adaptar los conjuntos X e Y a AdaBoost
(X, Y) = utils.adaptar_conjuntos(mnist_X, mnist_Y)

# Lanzar Adaboost
T = 15
A = 50


(pruebaX, pruebaY) = utils.crea_conjunto_entrenamiento(X, Y, 0)

#Tamaño de la muestra
N = len(pruebaX)

#Entrenamos
(Hx, alphas) = adaboost.entrenar(pruebaX, pruebaY, T, A)


resultado = np.ones(N)
posiciones = np.zeros(N)
aciertos = 0
fallos = 0

#Para ver si va
for idx in range(0, N):
    sumatorio = 0
    for deb in Hx:
        sumatorio = sumatorio + deb.confianza * 1 if cd.aplicar_clasificador_debil(deb, X[idx]) else -1
    if sumatorio > 0:
        resultado[idx] =  1
    else:
        resultado[idx] = -1
    posiciones[idx] = idx

for i in resultado:
    if i == 1:
        aciertos += 1
    else:
        fallos += 1

tasa_aciertos = aciertos / N
tasa_fallos = fallos / N

print("La tasa de aciertos es: ", tasa_aciertos, " %")
print("La tasa de fallos es: ", tasa_fallos, " %")

#for i in range(N):
#    if pruebaY[i]:
#        print("Pos :", i)

#sumatorio = 0

#for deb in Hx:
#    sumatorio = sumatorio + deb.confianza * 1 if cd.aplicar_clasificador_debil(deb, pruebaX[1]) else -1

#print("Valor: ", sumatorio)
#if sumatorio > 0:
#    print("La imagen es un 0")
#else:
#    print("La imagen no es un 0")

#utils.mostrar_imagen(pruebaX[1].reshape(28, 28))

total = np.count_nonzero(resultado == 1)
print("Total ceros con el algoritmo en los ", N, " primeros numeros: ", total)



cont = 0
for idx in range(0, N):
    if Y[idx] == 0:
        cont = cont + 1

print("Hay ", cont, " ceros en los primeros ", N, " numeros")
#utils.mostrar_imagen(mnist_X[0])
# Analisis y resultados de las pruebas realizadas
T = [0, 100, 200, 300, 400]      # Numero de clasificadores 
resultados = [0, 20, 35, 56, 68] # Resultados obtenidos de clasificacion
#utils.plot_arrays(T, resultados, "Porcentajes con valores de T")