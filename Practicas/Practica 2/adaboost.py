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
        best = None
        for i in range(0, A):
            Fk = cd.generar_clasificador_debil(dimension_datos)
            error = cd.obtener_error(Fk, X, Y, Dt)
            if error < menorError:
                menorError = error
                best = Fk
        
        #Capamos el error, hay dos casos cuando se pasa o es 0
        if menorError >= 1:
            menorError = 0.9999999
        #Y cuando es 0
        if menorError == 0:
            menorError = 0.0000001

        #Confianza
        alpha = 0.5 * np.log2((1 - menorError)/menorError)
        best.confianza = alpha
        
        alphas.append(alpha)
        
        clasificadores_debiles.append(best)

        #Actualizar Dt+1
        Z = 0
        for i in range(0, N):
            Dt[i] = Dt[i] *  math.pow(math.exp(1), -best.confianza * 1 if Y[i] == cd.aplicar_clasificador_debil(best, X[i]) else -1)
            Z = Z + Dt[i]
        
        #Normalizar
        for i in range(0, N):
            Dt[i] = Dt[i] / Z

    #for idx, fk in enumerate(clasificadores_debiles):
    #    print("Weak Learner " , idx, ": ", fk)
    
    return (clasificadores_debiles, alphas)