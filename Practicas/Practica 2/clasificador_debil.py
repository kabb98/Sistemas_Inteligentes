import random as rd

#Dimension con la que vamos a trabajar. En nuestro caso 28*28

class clasificador_debil():
    def __init__(self, pixel, umbral, dir):
        self.pixel = pixel
        self.umbral = umbral
        self.dir = dir
        self.error = 0
        self.confianza = 0
        
    def __repr__(self):
        return "Pixel: " + str(self.pixel) + ", Umbral: " + str(self.umbral) + ", Error: " + str(self.error) + " Confianza: " + str(self.confianza)

def generar_clasificador_debil(dimension_datos):
    pixel = rd.randint(0, dimension_datos-1)
    umbral = rd.randint(0, 255)
    dir = rd.choice([-1, 1])
    
    return clasificador_debil(pixel, umbral, dir)

def aplicar_clasificador_debil(c_d, imagen):
    #Tenemos que ver la dirección
    #Si la direccion es positiva, miramos en la parte positiva del plano
    if c_d.dir == 1:
        if imagen[c_d.pixel] > c_d.umbral:
            return True
    elif c_d.dir == -1:
        if imagen[c_d.pixel] < c_d.umbral:
            return True

    return False


def obtener_error(clasificador, X, Y, D):
    error = 0.0
    contador = 0
    for img in X:
        res = aplicar_clasificador_debil(clasificador, img)
        if res != Y[contador]:
            error = error + D[contador]
        contador = contador + 1
    
    clasificador.error = error
    return error