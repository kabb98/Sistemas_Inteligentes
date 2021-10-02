
import pygame
import tkinter.filedialog
from pygame.locals import *
from casilla import *
from mapa import *
from nodo import *
from typing import List

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
                        #coste = numeroVecinosValidos(mapi, origen, destino, camino)
                        coste = aEstrella(mapi, origen, destino, camino)
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

def esCorrecto(fila, columna, origen, mapa) -> bool:
    correcto: bool = False
    if(not (fila == origen.getFila() and columna == origen.getCol())):
        if bueno(mapa, Casilla(fila, columna)):
            correcto = True
    return correcto

def distanciaManhattan(origen: Casilla, destino: Casilla) -> float:
    return abs(destino.getFila() - origen.getFila()) + \
    abs(destino.getCol() - origen.getCol())

def vecinos(nodo: Nodo, mapa: Mapa) -> List:
    vecinos: List = []
    for i in range(nodo.casilla.getFila() - 1, nodo.casilla.getFila() + 2):
        for j in range(nodo.casilla.getCol() - 1, nodo.casilla.getCol() + 2):
            if esCorrecto(i, j, nodo.casilla, mapa):
                vecinos.append(Nodo(Casilla(i, j), nodo))

    return vecinos

def reconstruyeCamino(best: Nodo, caminos):
    coste = best.getF()
    
    while(best.getPadre()):
        best = best.getPadre()
        caminos[best.casilla.getFila()][best.casilla.getCol()] = 'X'
    return coste

def iniciaEstados(mapi):
    estados = []
    for i in range(mapi.alto):
        estados.append([])
        for j in range(mapi.ancho):
            estados[i].append(-1)
    return estados

def aEstrella(mapi: Mapa, origen: Casilla, destino: Casilla, caminos) -> float:
    coste_total: float = -1
    listaFrontera: List[Nodo] = []
    listaInterior: List[Nodo] = []

    estados = iniciaEstados(mapi)

    nodoInicial: Nodo = Nodo(origen)
    nodoMeta: Nodo = Nodo(destino)

    nodoInicial.h = nodoInicial.distanciaManhattan(nodoMeta)
    listaFrontera.append(nodoInicial)

    orden = 0
    while listaFrontera:
        #Cogemos el mejor nodo de la lista Frontera       
        best = min(listaFrontera, key=lambda nodo: nodo.f)
        estados[best.casilla.fila][best.casilla.col] = orden
        orden += 1

        """Hemos llegado a la meta"""
        if(best == nodoMeta):
            coste_total = reconstruyeCamino(best, caminos)
            for i in range(mapi.alto):
                for j in range(mapi.ancho):
                    print(estados[i][j], end = " ")
                print()
            break
        else:
            """Expandimos nodo"""
            listaFrontera.remove(best)
            listaInterior.append(best)

            """Vemos los hijos validos"""
            for hijo in vecinos(best, mapi):
                if hijo not in listaInterior:
                    g_m = best.g + costeCelda(hijo, best)
                    if hijo not in listaFrontera:
                        hijo.g = g_m
                        hijo.h = hijo.distanciaManhattan(nodoMeta)
                        hijo.f = hijo.g + hijo.h
                        hijo.padre = best
                        listaFrontera.append(hijo)
                    else:
                        if g_m < hijo.g:
                            hijo.padre = best
                            hijo.g = g_m
                            hijo.h = hijo.distanciaManhattan(nodoMeta)
                            hijo.f = hijo.g + hijo.h
    return coste_total

def costeCelda(vecino: Nodo, best: Nodo) -> float:
    coste: float = 0.0
    hijo: Casilla = vecino - best
    
    verticales = [Casilla(-1,0), Casilla(0,-1), Casilla(0,1), Casilla(1,0)]
    diagonales = [Casilla(-1, -1), Casilla(-1, 1), Casilla(1, -1), Casilla(1,1)]
    if hijo in verticales:
        coste = 1.0
    elif hijo in diagonales:
        coste = 1.5
    return coste

# ---------------------------------------------------------------------
if __name__ == "__main__":
    main()
