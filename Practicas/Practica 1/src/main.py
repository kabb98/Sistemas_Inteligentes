import sys
import pygame
import tkinter.filedialog
from casilla import *
from mapa import *
from pygame.locals import *
import math


from typing import Any, List


class Nodo(Casilla):
    def __init__(self, casilla: Casilla):
        self.casilla = casilla
        self.f = 0
        self.g = 0
        self.h = 0
        self.coste = 0
        self.padre = None

    def vecinos(self, mapa: Mapa) -> List:
        vecinos = []
        for i in range(self.casilla.getFila() - 1, self.casilla.getFila() + 2):
            for j in range(self.casilla.getCol() - 1, self.casilla.getCol() + 2):
                casilla = Casilla(i, j)
                nuevoNodo = Nodo(casilla)
                nuevoNodo.padre = self
                if(self.esValido(nuevoNodo, mapa)):
                    print("ENTRA!!!!!!!!!!!")
                    vecinos.append(nuevoNodo)
                    for vec in vecinos:
                        print(vec)

        return vecinos

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

    def esValido(self, current, mapa: Mapa):
        celda = mapa.getCelda(current.casilla.getCol(), current.casilla.getFila())
        print("Celda: " + str(celda))
        res = self != current and celda != 1
        if(res):
            print("Es valido")
        else:
            print("No es valido")
        return res

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

MARGEN = 5
MARGEN_INFERIOR = 60
TAM = 30
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)

# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------

# Devuelve si una casilla del mapa se puede seleccionar como destino


def bueno(mapi, pos):
    res = False

    if mapi.getCelda(pos.getFila(), pos.getCol()) == 0:
        res = True

    return res

# Devuelve si una posición de la ventana corresponde al mapa


def esMapa(mapi, posicion):
    res = False

    if posicion[0] > MARGEN and posicion[0] < mapi.getAncho()*(TAM+MARGEN)+MARGEN and \
            posicion[1] > MARGEN and posicion[1] < mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res = True

    return res

# PDevuelve si se ha pulsado el botón. Posición del botón: 20, mapa.getAlto()*(TAM+MARGEN)+MARGEN+10]


def pulsaBoton(mapi, posicion):
    res = False

    if posicion[0] > 20 and posicion[0] < 70 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res = True

    return res


# Construye la matriz para guardar el camino
def inic(mapi):
    cam = []
    for i in range(mapi.alto):
        cam.append([])
        for j in range(mapi.ancho):
            cam[i].append('.')

    return cam

# función principal


def main():
    root = tkinter.Tk()  # para eliminar la ventana de Tkinter
    root.withdraw()  # se cierra
    file = tkinter.filedialog.askopenfilename()  # abre el explorador de archivos

    pygame.init()
    destino = Casilla(-1, -1)

    reloj = pygame.time.Clock()

    if not file:  # si no se elige un fichero coge el mapa por defecto
        file = 'mapa.txt'

    mapi = Mapa(file)
    origen = mapi.getOrigen()
    camino = inic(mapi)

    anchoVentana = mapi.getAncho()*(TAM+MARGEN)+MARGEN
    altoVentana = MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN
    dimension = [anchoVentana, altoVentana]
    screen = pygame.display.set_mode(dimension)
    pygame.display.set_caption("Practica 1")

    boton = pygame.image.load("boton.png").convert()
    boton = pygame.transform.scale(boton, [50, 30])

    personaje = pygame.image.load("pig.png").convert()
    personaje = pygame.transform.scale(personaje, [TAM, TAM])

    coste = -1
    running = True
    primeraVez = True

    while running:
        # procesamiento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # obtener posición y calcular coordenadas matriciales
                pos = pygame.mouse.get_pos()
                colDestino = pos[0]//(TAM+MARGEN)
                filDestino = pos[1]//(TAM+MARGEN)
                casi = Casilla(filDestino, colDestino)
                if pulsaBoton(mapi, pos):  # reinicializar
                    origen = mapi.getOrigen()
                    destino = Casilla(-1, -1)
                    camino = inic(mapi)
                    coste = -1
                    primeraVez = True
                elif esMapa(mapi, pos):
                    if bueno(mapi, casi):
                        if not primeraVez:  # la primera vez el origen está en el mapa
                            origen = destino
                        else:
                            # se marca como libre la celda origen
                            mapi.setCelda(int(origen.getFila()),
                                          int(origen.getCol()), 0)
                        destino = casi
                        camino = inic(mapi)
                        # llamar al A*
                        coste = numeroVecinosValidos(mapi, origen, destino, camino)
                        #coste = aEstrella(mapi, origen, destino, camino)
                        if coste == -1:
                            tkinter.messagebox.showwarning(
                                title='Error', message='No existe un camino entre origen y destino')
                        else:
                            primeraVez = False  # hay un camino y el destino será el origen para el próximo movimiento
                    else:  # se ha hecho click en una celda roja
                        tkinter.messagebox.showwarning(
                            title='Error', message='Esa casilla no es valida')

        # código de dibujo
        # limpiar pantalla
        screen.fill(NEGRO)

        # pinta mapa
        for fil in range(mapi.getAlto()):
            for col in range(mapi.getAncho()):
                # para que no quede negro el origen inicial
                if mapi.getCelda(fil, col) == 2 and not primeraVez:
                    pygame.draw.rect(screen, BLANCO, [
                                     (TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                if mapi.getCelda(fil, col) == 0:
                    if camino[fil][col] == '.':
                        pygame.draw.rect(screen, BLANCO, [
                                         (TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    else:
                        pygame.draw.rect(screen, AMARILLO, [
                                         (TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)

                elif mapi.getCelda(fil, col) == 1:
                    pygame.draw.rect(
                        screen, ROJO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)

        # pinta origen
        screen.blit(personaje, [(TAM+MARGEN)*origen.getCol() +
                    MARGEN, (TAM+MARGEN)*origen.getFila()+MARGEN])
        # pinta destino
        pygame.draw.rect(screen, VERDE, [
                         (TAM+MARGEN)*destino.getCol()+MARGEN, (TAM+MARGEN)*destino.getFila()+MARGEN, TAM, TAM], 0)
        # pinta boton
        screen.blit(boton, [20, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        # pinta coste
        if coste != -1:
            fuente = pygame.font.Font(None, 30)
            texto = fuente.render("Coste "+str(coste), True, AMARILLO)
            screen.blit(texto, [anchoVentana-120,
                        mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])

        # actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)

    pygame.quit()

# Devuelve el nodo con el coste f menor

def numeroVecinosValidos(mapa: Mapa, origen: Casilla, destino: Casilla, caminos):
    vecinos: int = 0
    min = 10000
    
    x = 0
    y = 0

    for i in range(origen.getFila() - 1, origen.getFila() + 2):
        for j in range(origen.getCol() - 1, origen.getCol() + 2):
            if(mapa.getCelda(i, j) != 1 and  not (i == origen.getFila() and j == origen.getCol())):
                distMan = distanciaManhattan(Casilla(i, j), destino)
                if(distMan < min):
                    min = distMan
                    x = i
                    y = j
    
    vecinos += 1
    caminos[x][y] = 'X'

    return vecinos


def distanciaManhattan(origen: Casilla, destino: Casilla):
    return abs(destino.getFila() - origen.getFila()) + \
    abs(destino.getCol() - origen.getCol())

def mejorNodo(lista: List[Nodo]):
    index = 0
    for i in range(1, len(lista)):
        if lista[i].getF() < lista[index].getF():
            index = i
    return lista[index]


def aEstrella(mapi: Mapa, origen: Casilla, destino: Casilla, caminos):

    result: int = 0
    coste_total = -1
    listaFrontera: List[Nodo] = []
    listaInterior: List[Nodo] = []

    nodoInicial: Nodo = Nodo(origen)

    print(origen)
    print(destino)
    nodoMeta: Nodo = Nodo(destino)

    listaFrontera.append(nodoInicial)

    cont = 0

    while listaFrontera:
        #Cogemos el mejor nodo de la lista Frontera       
        best = min(listaFrontera, key=lambda nodo: nodo.f)
        caminos[best.casilla.getFila()][best.casilla.getCol()] = ' X'

        if(best == nodoMeta):
            coste_total = best.getF()
            while(best.getPadre()):
                best = best.getPadre()
            break
        else:
            try:
                listaFrontera.remove(best)
                listaInterior.append(best)

                for vecino in best.vecinos(mapi):
                    print(vecino)
                    if vecino not in listaInterior:
                        costeCasilla =  costeCelda(mapi, vecino, best)
                        tempG = best.getG() + costeCasilla

                        print("Coste mov: " + str(costeCasilla))
                        print("g temp: " + str(tempG))

                        cont += tempG
                        pos = listaFrontera.index(vecino)
                        # Si no está en la frontera se añade y ya
                        if vecino not in listaFrontera:
                            vecino.g = tempG
                            vecino.h = 0
                            vecino.f = vecino.getG() + vecino.getH()
                            vecino.padre = best
                            listaFrontera.append(vecino)
                        else:
                            nodoTemporal = listaFrontera[pos]
                            # Si ya existe en la frontera ver si es mejor
                            if(nodoTemporal.getG() > tempG):
                                nodoTemporal.g = tempG
                                nodoTemporal.h = 0
                                nodoTemporal.f = nodoTemporal.getG() + nodoTemporal.getH()
                                nodoTemporal.padre = best
            except ValueError:
                pass
    
    print("Acc: " + str(cont))
    return coste_total

# Devuelve -1 si el nodo esta en la lista, pos si existe


def existeEnLaLista(listaFrontera: List[Nodo], best: Nodo):
    pos: int = -1
    for i in range(len(listaFrontera)):
        if listaFrontera[i] == best:
            pos = i
    return pos


def costeCelda(mapi: Mapa, vecino: Nodo, best: Nodo) -> float:
    coste = 0

    verticales = set({Casilla(1, 0), Casilla(-1, 0),
                      Casilla(0, -1), Casilla(0, 1)})

    # [0,0][0,1][0,2]
    # [1,0][1,1][1,2]
    # [2,0][2,1][2,2]

    # Arriba -> 1,1 - 0,1 = 1,0
    # Abajo -> 1,1 - 2,1 = -1,0
    # Derecha -> 1,1 - 1,2 = 0,-1
    # Izquierda -> 1,1 - 1,0 = 0,1

    tempCasilla = best - vecino

    print(tempCasilla)
    if(best - vecino in verticales):
        coste = 1.0
    else:
        coste = 1.5

    return coste


# ---------------------------------------------------------------------
if __name__ == "__main__":
    main()
