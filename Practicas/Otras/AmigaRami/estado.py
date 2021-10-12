import math
from casilla import *


class Estado():
    def __init__(self, casilla: Casilla, padre = None):
        self.casilla = casilla
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = padre

    def getF(self):
        return self.f

    def getG(self):
        return self.g

    def getH(self):
        return self.h

    def getPadre(self):
        return self.parent
    def getCasilla(self):
        return self.casilla

    def setF(self, f):
        self.f = f

    def setG(self, g):
        self.g = g

    def setH(self, h):
        self.h = h

    def setPadre(self, parent):
        self.parent = parent

    def __eq__(self, other):
        return self.casilla == other.casilla
