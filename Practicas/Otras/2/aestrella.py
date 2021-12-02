from casilla import *
from nodo import *
import math


# Devuelve el nodo con menor f
def mejorNodoFrontera(lista):
    min = lista[0]

    for nodo in lista:
        if nodo < min:
            min = nodo
    return min


# Comprueba si dos posiciones son distintas
def esDistinto(xNodo, yNodo, x, y):
    return xNodo != x or yNodo != y

# Devuelve la fila y la col en valor absoluto
def getFilaCol(actual, vecino):
    fila = abs(vecino.getPosicion().getFila() - actual.getPosicion().getFila())
    col = abs(vecino.getPosicion().getCol() - actual.getPosicion().getCol())
    return fila, col

# Calculamos el coste
def calculaCoste(actual, vecino):
    fila, col = getFilaCol(actual, vecino)

    if(fila + col == 2):
        vecino.setCoste(1.5)
    else:
        vecino.setCoste(1)

# Devuelve una lista con los nodos del vecindario
def nodosAlrededor(actual, mapa):
    nodos = []
    xAct = actual.getPosicion().getFila()
    yAct = actual.getPosicion().getCol()

    for i in range(-1, 2):
        for j in range(-1, 2):
            x = xAct + i
            y = yAct + j
            if ((mapa.getCelda(x, y) == 0) and esDistinto(xAct, yAct, x, y)):
                nuevoNodo = Nodo(Casilla(x, y))
                calculaCoste(actual, nuevoNodo)
                nodos.append(nuevoNodo)

    return nodos


# Calcula el coste de llegar desde el origen a la destino, si no hay -> -1
def aEstrella(mapi, origen, destino, camino):

    coste = -1
    listInt = []
    listFront = []

    encontrado = False

    meta = Nodo(destino)
    listFront.append(Nodo(origen))

    mejor = None

    # Iteramos hasta que no haya nodos
    while len(listFront) != 0:
        mejor = mejorNodoFrontera(listFront)

        # Si es meta -> FIN
        if (mejor == meta):
            encontrado = True
            break
        else:
            # Expandimos
            listInt.append(mejor)
            listFront.remove(mejor)

            neighbors = nodosAlrededor(mejor, mapi)
            # Iteramos sobre los vecinos que no esten en la listInt
            for vec in neighbors:
                if (vec not in listInt):
                    g = mejor.getG() + vec.getCoste()
                    # Si no esta en la frontera se anyade sin mirar nada masa
                    if (vec not in listFront):
                        vec.setG(g)
                        h = heuristicas(vec, meta)
                        vec.setH(h)
                        vec.setF(g + h)
                        vec.setPadre(mejor)
                        listFront.append(vec)
                    else:
                        # Si g es mejor se recalcula todo
                        if (g < vec.getG()):
                            vec.setG(g)
                            h = heuristicas(vec, meta)
                            vec.setH(h)
                            vec.setF(g + h)
                            vec.setPadre(mejor)

    # Si hemos llegado a la meta entra aqui
    if encontrado:
        coste = mejor.getF()
        ultimo = mejor
        # Reconstruimos camino
        while (mejor.getPadre()):
            x = mejor.getPosicion().getFila()
            y = mejor.getPosicion().getCol()
            camino[x][y] = 'X'
            mejor = mejor.getPadre()
        
        
        print("Matriz de nodos explorados")
        explorados = creaMatrizExplorados(mapi)
        mostrarExplorados(explorados, listInt, mapi, ultimo)

        print("Coste: ", coste)
        print("Nodos explorados: ", len(listInt))

    return coste


#################################################################################
################################## HEURISTICAS ##################################
#################################################################################


# H = 0
def sinHeuristica():
    return 0

# Distancia Manhattan
def manhattan(actual, meta):
    x, y = getFilaCol(actual, meta)
    return x + y

# Distancia Euclidea
def euclidea(actual, meta):
    x = meta.getPosicion().getFila() - actual.getPosicion().getFila()
    y = meta.getPosicion().getCol() - actual.getPosicion().getCol()
    return math.sqrt(pow(x, 2) + pow(y, 2))

# Distancia Chevyshev
def chebyshev(actual, meta):
    return max(getFilaCol(actual, meta))


# Distancia Cuadratica
def cuadratica(actual, meta):
    x = meta.getPosicion().getFila() - actual.getPosicion().getFila()
    y = meta.getPosicion().getCol() - actual.getPosicion().getCol()

    return pow(x, 2) + pow(y, 2)

# Desde aqui llamamos a las otras heuristicas
def heuristicas(act, meta):
    return euclidea(act, meta)


########################## FUNCIONES NODOS EXPLORADOS  #################

# Crea la matriz para mostrar como se va explorando el mapa
def creaMatrizExplorados(mapi):
    matriz = []
    for i in range(mapi.alto):
        matriz.append([])
        for j in range(mapi.ancho):
            matriz[i].append(-1)

    return matriz

#Mostramos los nodos explorados en consola
def mostrarExplorados(explorados, listInt, mapi, ult):
    #Sacamos la matrix de explorados
    for index, nodo in enumerate(listInt):
        x = nodo.getPosicion().getFila()
        y = nodo.getPosicion().getCol()
        explorados[x][y] = index
    explorados[ult.getPosicion().getFila()][ult.getPosicion().getCol()] = len(listInt)

    #Mostramos
    for i in range(mapi.alto):
        for j in range(mapi.ancho):
            print(explorados[i][j], end=" ")
        print()