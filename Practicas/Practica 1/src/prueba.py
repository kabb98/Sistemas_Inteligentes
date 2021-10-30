import matplotlib.pyplot as plt
import random  # para poder generar números aleatorios
# Generación de una lista (x) con 10 valores enteros #La lista y contendrá 10 valores reales
x = list(range(10, 20))
y = []  # Escritura en dos ficheros de ambas listas

archiX = open('datosX', "w")
archiY = open('datosY', "w")

for i in range(10):
    archiX.write(str(x[i])+'\n')
    # se generan valores siguiendo una distribución normal
    y.append(random.gauss(4, 2))
    archiY.write(str(y[i])+'\n')
archiX.close()
archiY.close()  # Abrir ficheros para lectura 

archiX=open('datosX', "r") 
archiY=open('datosY', "r") 

x=[] 
y=[] 

for linea in archiX:
    if linea[-1]=='\n': #eliminar el salto de línea 
        linea=linea[:-1] 
        x.append(int(linea)) 
archiX.close() 

for linea in archiY: 
    if linea[-1]=='\n': 
        linea=linea[:-1] 
        y.append(float(linea))
    
archiY.close() 

#Creación de la gráfica 
plt.title('Ejemplo de gráfico lineal')
plt.plot(x,y) 
#Pone título a los ejes 
plt.xlabel('X')
plt.ylabel('Y')
#Mostrar
plt.show()
