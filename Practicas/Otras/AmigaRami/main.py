import sys, pygame
import tkinter.filedialog
from casilla import *
from mapa import *
from pygame.locals import *
from estado import *

MARGEN=5
MARGEN_INFERIOR=60
TAM=30
NEGRO=(0,0,0)
BLANCO=(255, 255,255)
VERDE=(0, 255,0)
ROJO=(255, 0, 0)
AZUL=(0, 0, 255)
AMARILLO=(255, 255, 0)

# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------

# Devuelve si una casilla del mapa se puede seleccionar como destino
def bueno(mapi, pos):
    res= False

    if mapi.getCelda(pos.getFila(),pos.getCol())==0:
       res=True

    return res

# Devuelve si una posición de la ventana corresponde al mapa
def esMapa(mapi, posicion):
    res=False

    if posicion[0] > MARGEN and posicion[0] < mapi.getAncho()*(TAM+MARGEN)+MARGEN and \
    posicion[1] > MARGEN and posicion[1] < mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True

    return res

#PDevuelve si se ha pulsado el botón. Posición del botón: 20, mapa.getAlto()*(TAM+MARGEN)+MARGEN+10]
def pulsaBoton(mapi, posicion):
    res=False

    if posicion[0] > 20 and posicion[0] < 70 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True

    return res


# Construye la matriz para guardar el camino
def inic(mapi):
    cam=[]
    for i in range(mapi.alto):
        cam.append([])
        for j in range(mapi.ancho):
            cam[i].append('.')

    return cam


# función principal
def main():
    root= tkinter.Tk() #para eliminar la ventana de Tkinter
    root.withdraw() #se cierra
    file=tkinter.filedialog.askopenfilename() #abre el explorador de archivos

    pygame.init()
    destino=Casilla(-1,-1)

    reloj=pygame.time.Clock()

    if not file:     #si no se elige un fichero coge el mapa por defecto
        file='mapa.txt'

    mapi=Mapa(file)
    origen=mapi.getOrigen()
    camino=inic(mapi)

    anchoVentana=mapi.getAncho()*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension)
    pygame.display.set_caption("Practica 1")

    boton=pygame.image.load("boton.png").convert()
    boton=pygame.transform.scale(boton,[50, 30])

    personaje=pygame.image.load("pig.png").convert()
    personaje=pygame.transform.scale(personaje,[TAM, TAM])

    coste=-1
    running= True
    primeraVez=True

    while running:
        #procesamiento de eventos
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

            if event.type==pygame.MOUSEBUTTONDOWN:
                #obtener posición y calcular coordenadas matriciales
                pos=pygame.mouse.get_pos()
                colDestino=pos[0]//(TAM+MARGEN)
                filDestino=pos[1]//(TAM+MARGEN)
                casi=Casilla(filDestino, colDestino)
                if pulsaBoton(mapi, pos): #reinicializar
                    origen=mapi.getOrigen()
                    destino=Casilla(-1,-1)
                    camino=inic(mapi)
                    coste=-1
                    primeraVez=True
                elif esMapa(mapi, pos):
                    if bueno(mapi, casi):
                        if not primeraVez: #la primera vez el origen está en el mapa
                            origen=destino
                        else:
                            mapi.setCelda(int(origen.getFila()), int(origen.getCol()), 0) #se marca como libre la celda origen
                        destino=casi
                        camino=inic(mapi)
                        # llamar al A*
                        coste=aEstrella(mapi, origen, destino, camino)
                        if coste==-1:
                            tkinter.messagebox.showwarning(title='Error', message='No existe un camino entre origen y destino')
                        else:
                            primeraVez=False  # hay un camino y el destino será el origen para el próximo movimiento
                    else: # se ha hecho click en una celda roja
                        tkinter.messagebox.showwarning(title='Error', message='Esa casilla no es valida')


        #código de dibujo
        #limpiar pantalla
        screen.fill(NEGRO)
        #pinta mapa
        for fil in range(mapi.getAlto()):
            for col in range(mapi.getAncho()):
                if mapi.getCelda(fil, col)==2 and not primeraVez: #para que no quede negro el origen inicial
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                if mapi.getCelda(fil,col)==0:
                    if camino[fil][col]=='.':
                        pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    else:
                        pygame.draw.rect(screen, AMARILLO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)

                elif mapi.getCelda(fil,col)==1:
                    pygame.draw.rect(screen, ROJO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)

        #pinta origen
        screen.blit(personaje, [(TAM+MARGEN)*origen.getCol()+MARGEN, (TAM+MARGEN)*origen.getFila()+MARGEN])
        #pinta destino
        pygame.draw.rect(screen, VERDE, [(TAM+MARGEN)*destino.getCol()+MARGEN, (TAM+MARGEN)*destino.getFila()+MARGEN, TAM, TAM], 0)
        #pinta boton
        screen.blit(boton, [20, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        #pinta coste
        if coste!=-1:
            fuente= pygame.font.Font(None, 30)
            texto= fuente.render("Coste "+str(coste), True, AMARILLO)
            screen.blit(texto, [anchoVentana-120, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])

        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)


    pygame.quit()
    
#Devuelve el estado con el f menor
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
    
    if res == 2:
        return 1.5
    elif res == 1:
        return 1
def caminoReconstruido(n, caminos):
    if n.getPadre() is None:
        return
    
    caminos[n.getCasilla().getFila()][n.getCasilla().getCol()] = 'C'
    caminoReconstruido(n.getPadre(), caminos)

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






#---------------------------------------------------------------------
if __name__=="__main__":
    main()
