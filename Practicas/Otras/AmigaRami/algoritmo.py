#Devuelve el estado con el f menor
from estado import *
from casilla import *
import time

def mejorEstado(listaFrontera):
    pos = 0

    for i in range(1, len(listaFrontera)):
        if listaFrontera[i].getF() < listaFrontera[pos].getF():
            pos = i
    return listaFrontera[pos]

def createExpPath(mapi):
    cam = []
    for i in range(mapi.alto):
        cam.append([])
        for j in range(mapi.ancho):
            cam[i].append(-1)
    
    return cam

def muestraCaminoExpandido(cam, mapi):
    print("Camino Expandido")
    for i in range(mapi.alto):
        for j in range(mapi.ancho):
            print(cam[i][j], end = " ")
        print()


def aEstrella(mapi, origen, destino, camino):
    #Comenzamos a contar el tiempo
    inicio = time.time_ns()

    #Estructuras de datos
    listaFrontera = []
    listaInterior = []
    expandedPath = createExpPath(mapi)
    
    #Nodos de los que sabemos su posicion
    estadoInicial = Estado(origen)
    estadoFinal = Estado(destino)
    
    #Añadimos el estado inicial a la lista frontera
    listaFrontera.append(estadoInicial)

    #Guardamos el orden para el camino expadido
    posOrden = 0

    #Itera mientra haya nodos
    while len(listaFrontera) > 0:
        #Sacamos el mejor nodo de la lista frontera
        n = mejorEstado(listaFrontera)
        
        fil = n.getCasilla().getFila()
        col = n.getCasilla().getCol()
        expandedPath[fil][col] = posOrden
        posOrden += 1

        #Si n es meta, acabamos
        if n == estadoFinal:
            #Fin tiempo ejecución
            fin = time.time_ns()

            #Guardamos la f del mejor nodo
            res = n.getF()
            
            #Estadisticas
            print("Coste: ", res)
            print("Nodos explorados: ", len(listaInterior))
            #g = float("{:.5f}".format(fin - inicio))
            print("Tiempo de ejecución: ", fin - inicio)

            #Caminos
            muestraCaminoReconstruido(n, camino)
            muestraCaminoExpandido(expandedPath, mapi)
            print

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
def muestraCaminoReconstruido(n, camino):
    while n.getPadre() is not None:
        camino[n.getCasilla().getFila()][n.getCasilla().getCol()] = 'X'
        n = n.getPadre()
    
    print("Camino")
    for i in range(len(camino)):
        for j in range(len(camino[i])):
            print(camino[i][j], end=" ")
        print()

#Saca los vecinos adyacentes a n que sean correctos
def vecinosAdyacentes(mapa, n):
    adyacentes = []
    #Posicion del nodo actual
    x = n.getCasilla().getFila()
    y = n.getCasilla().getCol()

    #Recorremos los vecinos y miramos si son correctos, y se añade a la lista
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if mapa.getCelda(i,j) == 0 and not (i == x and j == y):
                pos = Casilla(i, j)
                adyacentes.append(Estado(pos))
    return adyacentes

#Heuristica Manhattan
def manhattanHeuristic(actual, meta):
    res = abs(meta.getCasilla().getFila() - actual.getCasilla().getFila()) + \
        abs(meta.getCasilla().getCol() - actual.getCasilla().getCol())
    return res

#Heuristica Euclidea
def euclideaHeuristic(actual, meta):
    pass

#Heuristica Chevyshev
def chevyshevHeuristic(actual, meta):
    pass

#Heuristica Cuadratica
def cuadraticHeuritic(actual, meta):
    pass