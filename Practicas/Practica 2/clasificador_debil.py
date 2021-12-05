import random as rd

#Clase clasificador débil
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
            return 1
    elif c_d.dir == -1:
        if imagen[c_d.pixel] < c_d.umbral:
            return 1

    return -1

def obtener_error(clasificador, X, Y, D):
    error = 0.0
    for i, img in enumerate(X):
        if aplicar_clasificador_debil(clasificador, img) != Y[i]:
            error += D[i]
    
    clasificador.error = error
    return error