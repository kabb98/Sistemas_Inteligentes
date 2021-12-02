import math

########################### HEURISTICAS ########################### 
def sinHeuristica():
    return 0

#Distancia de Manhattan
def distanciaManhattan(curr, meta):
    return abs(curr.casilla.fila - meta.casilla.fila) + \
    abs(curr.casilla.col - meta.casilla.col)

#Distancia Euclidea
def distanciaEuclidea(curr, meta):
    return math.sqrt(((meta.casilla.fila - curr.casilla.fila)**2 + (meta.casilla.col - curr.casilla.col)**2 ))

def distanciaDiagonal(curr, meta):
    x = abs(meta.casilla.fila - curr.casilla.fila)
    y = abs(meta.casilla.col - curr.casilla.col)

    d_min = min(x, y)
    d_max= max(x, y)
    diagonalStep = d_min
    straightSteps = d_max - d_min

    return math.sqrt(2) * diagonalStep + straightSteps

def distanciaChebyshev(curr, meta):
    x = abs(curr.casilla.fila - meta.casilla.fila)
    y = abs(curr.casilla.col - meta.casilla.col)
    return max(x, y)

def distanciaCuadratica(curr, meta):
    return ((meta.casilla.fila - curr.casilla.fila)**2 + (meta.casilla.col - curr.casilla.col)**2 )
