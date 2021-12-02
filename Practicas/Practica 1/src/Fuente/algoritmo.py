from typing import List
from nodo import *
from heuristicas import *
from mapa import *

def esCorrecto(fila, columna, origen, mapa) -> bool:
    correcto: bool = False

    if(fila != origen.getFila() or columna != origen.getCol()) and \
            mapa.getCelda(fila, columna) == 0:
        correcto = True
    return correcto


def vecinos(nodo: Nodo, mapa: Mapa) -> List:
    vecinos: List = []
    for i in range(nodo.casilla.getFila() - 1, nodo.casilla.getFila() + 2):
        for j in range(nodo.casilla.getCol() - 1, nodo.casilla.getCol() + 2):
            if esCorrecto(i, j, nodo.casilla, mapa):
                vecinos.append(Nodo(Casilla(i, j), nodo))

    return vecinos


def reconstruyeCamino(n: Nodo, caminos):
    while(n.getPadre()):
        caminos[n.casilla.getFila()][n.casilla.getCol()] = 'X'
        n = n.getPadre()


def iniciaEstados(mapi):
    estados = []
    for i in range(mapi.alto):
        estados.append([])
        for j in range(mapi.ancho):
            estados[i].append(-1)
    return estados


def camino_expandido(camino, mapi):
    for i in range(mapi.alto):
        for j in range(mapi.ancho):
            print(camino[i][j], end=" ")
        print()

#Devuelve el coste de moverse de n -> vecino
def costeCelda(vecino: Nodo, n: Nodo) -> float:
    x = abs(n.casilla.fila - vecino.casilla.fila)
    y = abs(n.casilla.col - vecino.casilla.col)
    if x + y == 1:
        return 1.0
    else:
        return 1.5


def printLista(list):
    for nodo in list:
        print(nodo)

def aEstrella(mapi: Mapa, origen: Casilla, destino: Casilla, caminos) -> float:
    #Coste, -1 si no encuentra camino
    coste_total: float = -1

    #Estructuras para guardar nodos
    listaFrontera: List[Nodo] = []
    listaInterior: List[Nodo] = []
    estados = iniciaEstados(mapi)

    #Creamos nodos inicio y meta
    nodoInicial: Nodo = Nodo(origen)
    nodoMeta: Nodo = Nodo(destino)
    
    #Se añade a la lista frontera el origen
    listaFrontera.append(nodoInicial)

    orden = 0
    while listaFrontera:
        # Cogemos el mejor nodo de la lista Frontera
        n: Nodo = listaFrontera[0]
        estados[n.casilla.fila][n.casilla.col] = orden
        orden += 1

        """Hemos llegado a la meta"""
        if(n == nodoMeta):
            coste_total = n.f
            reconstruyeCamino(n, caminos)
            camino_expandido(estados, mapi)
            print("Coste: ", coste_total)
            print("Nodos explorados: ", len(listaInterior))
            break
        else:
            """Expandimos nodo"""
            listaInterior.append(n)
            listaFrontera.remove(n)

            """Vemos los hijos validos"""
            for hijo in vecinos(n, mapi):
                if hijo not in listaInterior:
                    g_m = n.g + costeCelda(hijo, n)
                    if hijo not in listaFrontera:
                        hijo.padre = n
                        hijo.g = g_m
                        hijo.h = distanciaDiagonal(hijo, nodoMeta)
                        hijo.f = hijo.g + hijo.h
                        listaFrontera.append(hijo)
                        listaFrontera.sort(key=lambda nodo: nodo.f)
                    elif g_m < hijo.g:
                        hijo.padre = n
                        hijo.g = g_m
                        hijo.h = distanciaDiagonal(hijo, nodoMeta)
                        hijo.f = hijo.g + hijo.h
                    
    return coste_total