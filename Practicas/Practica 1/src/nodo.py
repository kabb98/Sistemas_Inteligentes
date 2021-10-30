from casilla import *
import math
class Nodo():
    def __init__(self, casilla: Casilla, padre = None):
        self.casilla = casilla
        self.f = 0
        self.g = 0
        self.h = 0
        self.coste = 0
        self.padre = padre
    
    def getF(self) -> float:
        return self.f

    def getG(self) -> float:
        return self.g

    def getH(self) -> float:
        return self.h
    
    def getPadre(self):
        return self.padre

    def __sub__(self, other) -> Casilla:
        return Casilla(abs(self.casilla.fila - other.casilla.fila), abs(self.casilla.col - other.casilla.col))

    

    #Distancias
    #Distancia de Manhattan
    def distanciaManhattan(self, other):
        return abs(self.casilla.fila - other.casilla.fila) + \
        abs(self.casilla.col - other.casilla.col)
    
    #Distancia Euclidea
    def distanciaEuclidea(self, other):
        return math.sqrt(((other.casilla.fila - self.casilla.fila)**2 + (other.casilla.col - self.casilla.col)**2 ))
    
    def distanciaDiagonal(self, other):
        dx = abs(other.casilla.fila - self.casilla.fila)
        dy = abs(other.casilla.col - self.casilla.col)

        mini = min(dx, dy)
        maxi = max(dx, dy)
        diagonalStep = mini
        straightSteps = maxi - mini

        return math.sqrt(2) * diagonalStep + straightSteps

    def distanciaChevychev(self, other):
        x = abs(self.casilla.fila - other.casilla.fila)
        y = abs(self.casilla.col - other.casilla.col)
        return max(x, y)

    #Sobrecarga del operador ==
    def __eq__(self, other):
        return self.casilla == other.casilla

    #Sobrecarga de la salida estandar
    def __repr__(self):
        return "(" + str(self.casilla.getFila()) + "," + str(self.casilla.getCol()) + ")"