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

#Separamos entre el conjunto de validación y entrenamiento
X_Train, X_Validation, Y_Train, Y_Validation = utils.split_train_validation_set(X, Y)


#Ya tenemos el conjunto de entrenamiento bien
(X_Train, Y_Train) = utils.creaConjunto(X_Train, Y_Train, 0)
Y_Train = utils.addaptForTraining(Y_Train, 0)

#Lo mismo para el de validación)
(X_Validation, Y_Validation) = utils.creaConjunto(X_Validation, Y_Validation, 0)
Y_Validation = utils.addaptForTraining(Y_Validation, 0)

#Entrenamos
T = 10
A = 30

(Hx, alphas) = adaboost.entrenar(X_Train, Y_Train, T, A)

#Aplicamos el clasificador fuerte al conjunto de validación
adaboost.aplicar_clasificador_fuerte(X_Validation, Y_Validation, Hx, alphas)