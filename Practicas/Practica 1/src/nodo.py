from casilla import *
import math
class Nodo(Casilla):
    def __init__(self, casilla: Casilla, padre = None):
        self.casilla = casilla
        self.f = 0
        self.g = 0
        self.h = 0
        self.coste = 0
    
    def getF(self):
        return self.f

    def getG(self):
        return self.g

    def getH(self):
        return self.h
    
    def getPadre(self):
        return self.padre

    def __sub__(self, other) -> Casilla:
        return Casilla(self.casilla.fila - other.casilla.fila, self.casilla.col - other.casilla.col)

    

    #Distancias
    #Distancia de Manhattan
    def distanciaManhattan(self, other):
        return abs(other.casilla.fila - self.casilla.fila) + \
        abs(other.casilla.col - self.casilla.col)
    
    #Distancia Euclidea
    def distanciaEuclidea(self, other):
        return math.sqrt(((other.casilla.fila - self.casilla.fila)**2 + (other.casilla.col - self.casilla.col)**2 ))
    
    #Sobrecarga del operador ==
    def __eq__(self, other):
        """Devuelve true si la fila y columna son iguales"""
        return self.casilla == other.casilla

    #Sobrecarga de la salida estandar
    def __repr__(self):
        return "Coste f: " + str(self.f) + \
            "Coste g: " + str(self.g) + \
            "Coste h: " + str(self.h)