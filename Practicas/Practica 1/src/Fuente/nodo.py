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

    #Sobrecarga del operador ==
    def __eq__(self, other):
        return self.casilla == other.casilla

    def __repr__(self):
        return "(" + str(self.casilla.fila) + ", " + str(self.casilla.col) + ") [f: " + str(self.f) + ", g: " + str(self.g)+ ", h: " + str(self.h)