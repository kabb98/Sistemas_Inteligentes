#Devuelve el estado con el f menor
from estado import *
from casilla import *


def mejorEstado(listaFrontera):
    pos = 0

    for i in range(1, len(listaFrontera)):
        if listaFrontera[i].getF() < listaFrontera[pos].getF():
            pos = i
    return listaFrontera[pos]

def aEstrella(mapi, origen, destino, camino):
    listaFrontera = []
    listaInterior = []
    estadoInicial = Estado(origen)
    estadoFinal = Estado(destino)

    listaFrontera.append(estadoInicial)

    while len(listaFrontera) > 0:
        n = mejorEstado(listaFrontera)

        if n == estadoFinal:
            res = n.getF()
            caminoReconstruido(n, camino)
            return res
        else:
            listaInterior.append(n)
            listaFrontera.remove(n)

            for m in vecinosAdyacentes(mapi, n):
                if m not in listaInterior:
                    #Calculamos el coste
                    g_m = n.getG() + costeDesplazamiento(n, m)
                    if m not in listaFrontera:
                        m.setG(g_m)
                        m.setH(0)
                        m.setF(m.getG() + m.getH())
                        m.setPadre(n)
                        listaFrontera.append(m)
                    elif g_m < m.getG():
                        m.setG(g_m)
                        m.setH(0)
                        m.setF(m.getG() + m.getH())
                        m.setPadre(n)
    return -1

#Sacamos la suma del valor abs de las filas y columnas
#Si da 1 => Movimiento vertical
#Si no si = 2 => Movimiento diagonal
def costeDesplazamiento(n, m):
    res = abs(n.getCasilla().getFila() - m.getCasilla().getFila()) + \
        abs(n.getCasilla().getCol() - m.getCasilla().getCol())
    
    if res == 1:
        return 1
    else:
        return 1.5

#Reconstrucción de camino
def caminoReconstruido(n, caminos):
    while n.getPadre() is not None:
        caminos[n.getCasilla().getFila()][n.getCasilla().getCol()] = 'C'
        n = n.getPadre()

#Saca los vecinos adyacentes a n que sean correctos
def vecinosAdyacentes(mapi, n):
    adyacentes = []
    #Posicion del nodo actual
    x = n.getCasilla().getFila()
    y = n.getCasilla().getCol()

    #Recorremos los vecinos y miramos si son correctos, y se añade a la lista
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if mapi.getCelda(i,j) == 0 and not (i == x and j == y):
                pos = Casilla(i, j)
                adyacentes.append(Estado(pos))
    return adyacentes


#Heuristica Manhattan
def manhattanHeuristic(actual, meta):
    res = abs(meta.getCasilla().getFila() - actual.getCasilla().getFila()) + \
        abs(meta.getCasilla().getCol() - actual.getCasilla().getCol())
    return res