import clasificador_debil as cd
import numpy as np
import math as math

def entrenar(X, Y, T, A):
    clasificadores_debiles = []
    alphas = []
    
    N = len(X)
    Dt = np.ones(N) * 1/N
    dimension_datos = 784
    
    for t in range(0, T):
        menorError = 1.1
        
        #Entrenar ht
        Fk = None
        for i in range(0, A):
            Fp = cd.generar_clasificador_debil(dimension_datos)
            error = cd.obtener_error(Fp, X, Y, Dt)
            if error < menorError:
                menorError = error
                Fk = Fp
        
        #Capamos el error, hay dos casos cuando se pasa o es 0
        if menorError >= 1:
            menorError = 0.9999999
        #Y cuando es 0
        if menorError == 0:
            menorError = 0.0000001

        #Confianza
        alpha = 0.5 * np.log2((1 - menorError)/menorError)
        Fk.confianza = alpha
        
        alphas.append(alpha)
        
        clasificadores_debiles.append(Fk)

        #Actualizar Dt+1
        for i in range(0, N):
            Dt[i] *= (math.e ** (-Fk.confianza * cd.aplicar_clasificador_debil(Fk, X[i])))
        Z = np.sum(Dt)

        #Normalizar
        for i in range(0, N):
            Dt[i] /= Z
        
        print(Dt)
        
    #Devuelves el clasificador fuerte
    for deb in clasificadores_debiles:
        print(deb)
    return (clasificadores_debiles, alphas)

def aplicar_clasificar_fuerte_a_imagen(Hx, imagen):
    acc = 0
    for ht in Hx:
        acc += ht.confianza * cd.aplicar_clasificador_debil(ht, imagen)
    #print("Accuracy: " + str(acc))
    return 1 if acc > 0 else -1

def aplicar_clasificador_fuerte(X, Y, clasificadores, alphas):
    tasa_error = 0.0
    tasa_acierto = 0.0
    
    N = len(X)
    resultados = np.zeros(N)
    for idx, img in enumerate(X):
        if aplicar_clasificar_fuerte_a_imagen(clasificadores, img) != Y[idx]:
            tasa_error += 1
    
    #tasa_acierto = 1 - tasa_error
    
    muestraError(N, tasa_acierto, tasa_error)


def muestraError(N, tasa_acierto, tasa_error):
    print("El algoritmo ha acertado", tasa_acierto, "imagenes y tiene una tasa de  acierto del", (tasa_acierto/N) * 100, "%")
    print("El algoritmo ha fallado", tasa_error, "imagenes y tiene una tasa de error del", (tasa_error/N) * 100, "%")