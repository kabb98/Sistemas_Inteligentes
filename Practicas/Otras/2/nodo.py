import casilla

class Nodo():
    #Constructor
    def __init__(self, pos, padre = None):
        self.pos = pos
        self.padre = padre
        self.coste = 0
        self.f = self.g = self.h = 0
    
    #Devuelve el coste
    def getCoste(self):
        return self.coste
    
    #Devuelve la f
    def getF(self):
        return self.f

    #Devuelve la funcion g
    def getG(self):
        return self.g
    
    #Devuelve la funcion h
    def getH(self):
        return self.h
    
    #Devuelve el padre del nodo
    def getPadre(self):
        return self.padre
    
    #Devuelve la posicion/casilla
    def getPosicion(self):
        return self.pos
    
    #Setter del padre
    def setPadre(self, p):
        self.padre = p
    
    #Setter de la funcion f
    def setF(self, f):
        self.f = f

    #Setter de la funcion g    
    def setG(self, g):
        self.g = g
    
    #Setter de la funcion h
    def setH(self, h):
        self.h = h

    #Setter del coste
    def setCoste(self, coste):
        self.coste = coste
    
    #Sobrecarga del operador ==
    def __eq__(self, otro):
        return self.pos.getFila() == otro.pos.getFila() and self.pos.getCol() == otro.pos.getCol()

    #Sobrecarga del operador <, usaremos la f para ello
    def __lt__(self, otro):
        return self.f < otro.f