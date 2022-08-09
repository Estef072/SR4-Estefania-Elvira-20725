# Estefania Elvira 
# Ejercicio 4
# Fecha 08/08/22


import struct
from collections import namedtuple
from obj import Obj
from mathLi import *
#import numpy as np

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])

def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    # 4 bytes
    return struct.pack('=l', d)

# Guarda color
def _color(r, g, b):
    # Acepta valores de 0 a 1, además tendrá el tamaño de 1 Byte
    return bytes([ int(b * 255), int(g* 255), int(r* 255)])

def baryCoords(A, B, C, P):
    # u es para A, v es para B, w es para C
    try:
        #PCB/ABC
        u = (((B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)) /
            ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)))

        #PCA/ABC
        v = (((C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)) /
            ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)))

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w

# Variables globales

BLACK = _color(0,0,0)
WHITE = _color(1,1,1)


class Renderer(object):
    #Constructor
    def __init__(self, width, height):
        # Crea un nuevo Renderer de color negro
        self.curr_color = WHITE
        self.clear_color = BLACK
        self.glCreateWindow(width, height)

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        # Crea una ventana dibujando en todos los pixeles
        self.glClear()
        # El viewPort tendrá las mismas dimensiones que la ventana
        self.glViewport(0,0, width, height)

    # Crea el viewport
    def glViewport(self, x, y, width, height):
        self.vpX = int(x)
        self.vpY = int(y)
        self.vpWidth = int(width)
        self.vpHeight = int(height)

    # Determina que color quiero para el fondo
    def glClearColor(self, r, g, b):
        # Color que le quiero asignar a los pixeles de fondo
		# Tedrá 3 Bytes
        self.clear_color = color(r, g, b)

    def glClear(self):
        #Crea una lista 2D de pixeles y a cada valor le asigna 3 bytes de color
        # Recorre todo el ancho y altura y a cada una le asigna el color de 
		# limpieza que es negro
        self.pixels = [[ self.clear_color for y in range(self.height)] for x in range(self.width)]

        self.zbuffer = [[ -float('inf') for y in range(self.height)] for x in range(self.width)]

    def glViewportClear(self, color = None):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                self.glPoint(x,y, color)
    
    # Color del dibujo
    def glColor(self, r, g, b):
        self.curr_color = color(r,g,b)

    # Dibujar un punto
    def glPoint(self, x, y, color = None): # Pide color y si se le da lo coloca y si no coloca el dafault
        if x < self.vpX or x >= self.vpX + self.vpWidth or y < self.vpY or y >= self.vpY + self.vpHeight:
            return

        # Para que acepte solo enteros
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[int(x)][int(y)] = color or self.curr_color

    # Dibujar un punto normalizado
    def glPoint_NDC(self, x, y, color = None): # Pide color y si se le da lo coloca y si no coloca el dafault
        x = int( (x + 1) * (self.vpWidth / 2) + self.vpX )
        y = int( (y + 1) * (self.vpHeight / 2) + self.vpY)

        # Dibujar solamente dentro de las coordenadas
		# Rangos normalizados
        if x < self.vpX or x >= self.vpX + self.vpWidth or y < self.vpY or y >= self.vpY + self.vpHeight:
            return

        # Para que acepte solo enteros
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[int(x)][int(y)] = color or self.curr_color

    def glLine(self, v0, v1, color = None):
        x0 = v0.x
        x1 = v1.x
        y0 = v0.y
        y1 = v1.y

        # Evitar división por 0, si encuentra el mismo punto no dibuja una línea sino que un punto
        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y1,color)
            return

        # Pendiente
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        # Para determinar si está muy inclinado
        steep = dy > dx # Hay más desplazamiento en dy que en dx

        # Cambia de eje si está muy inclinado, o sea, más de 1 de pendiente (arriba)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # Se está dibujando de derecha a izquierda, se tiene que dibujar de izquierda a derecha
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        # Pendiente
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        # Determina en cual de los dos pixeles cae cada vez que vaya cambiando de posición la línea
        offset = 0

		# Verá si ya se apsó del límite para pasarse a otro pixel y dibujarlo
        limit = 0.5

        m = dy/dx
        y = y0

        # Range no incluye el último número, entonces se le suma 1
        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color)
            else:
                self.glPoint(x, y, color)

            # Calcula el siguiente valor de y
            offset += m
            if offset >= limit:
                # Y va creciendo y límite también para que se vaya dibujando bien todo
                y += 1 if y0 < y1 else -1
                limit += 1

    def glTriangle_standard(self, A, B, C, color = None):

        # Se cambian de lugar
        if A.y < B.y:
            A, B = B, A
        if A.y < C.y:
            A, C = C, A
        if B.y < C.y:
            B, C = C, B

        def flatBottomTriangle(v1, v2, v3):
            try:
                d_21 = (v2.x - v1.x) / (v2.y - v1.y)
                d_31 = (v3.x - v1.x) / (v3.y - v1.y)
            except:
                pass
            else:
                x1 = v2.x
                x2 = v3.x
                for y in range(v2.y, v1.y + 1):
                    self.glLine(V2(int(x1),y), V2(int(x2),y), color)
                    x1 += d_21
                    x2 += d_31

        def flatTopTriangle(v1, v2, v3):
            try:
                d_31 = (v3.x - v1.x) / (v3.y - v1.y)
                d_32 = (v3.x - v2.x) / (v3.y - v2.y)
            except:
                pass
            else:
                x1 = v3.x
                x2 = v3.x

                for y in range(v3.y, v1.y + 1):
                    self.glLine(V2(int(x1),y), V2(int(x2),y), color)
                    x1 += d_31
                    x2 += d_32

        if B.y == C.y:
            # triangulo con base inferior plana
            flatBottomTriangle(A, B, C)
        elif A.y == B.y:
            # triangulo con base superior plana
            flatTopTriangle(A, B, C)
        else:
            # dividir el triangulo en dos
            # dibujar ambos casos
            # Teorema de intercepto
            D = V2(A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x)   , B.y)
            flatBottomTriangle(A, B, D)
            flatTopTriangle(B, D, C)

    def glTriangle_bc(self, A, B, C, texCoords = (), texture = None, color = None, intensity = 1):
        #Bounding Box
        minX = round(min(A.x, B.x, C.x))
        minY = round(min(A.y, B.y, C.y))
        maxX = round(max(A.x, B.x, C.x))
        maxY = round(max(A.y, B.y, C.y))

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u, v, w = baryCoords(A, B, C, V2(x, y))

                if u >= 0 and v >= 0 and w >= 0:

                    z = A.z * u + B.z * v + C.z * w

                    if texture:
                        tA, tB, tC = texCoords
                        tx = tA[0] * u + tB[0] * v + tC[0] * w
                        ty = tA[1] * u + tB[1] * v + tC[1] * w
                        color = texture.getColor(tx, ty)

                    if z > self.zbuffer[x][y]:

                        self.glPoint(x,y, _color( color[2] * intensity / 255,
                                                  color[1] * intensity / 255,
                                                  color[0] * intensity / 255) )
                        self.zbuffer[x][y] = z


    def glTransform(self, vertex, translate=V3(0,0,0), scale=V3(1,1,1)):
        return V3(vertex[0] * scale.x + translate.x,
                  vertex[1] * scale.y + translate.y,
                  vertex[2] * scale.z + translate.z)

    # Función para cargar modelo en pantalla
    def glLoadModel(self, filename, texture = None, translate = V3(0,0,0), scale = V3(1,1,1)):
        # Se carga el modelo con el nombre
        model = Obj(filename)

        # Dirección de la luz
        light = V3(0,0,-1)
        light = normalized(light)

        for face in model.faces:
            # Cuantos vértices tiene la cara
            vertCount = len(face)

            for v in range(vertCount):
                vert0 = model.vertices[face[0][0] - 1]
                vert1 = model.vertices[face[1][0] - 1]
                vert2 = model.vertices[face[2][0] - 1]

                vt0 = model.texcoords[face[0][1] - 1]
                vt1 = model.texcoords[face[1][1] - 1]
                vt2 = model.texcoords[face[2][1] - 1]

                a = self.glTransform(vert0, translate, scale)
                b = self.glTransform(vert1, translate, scale)
                c = self.glTransform(vert2, translate, scale)

                if vertCount == 4:
                    vert3 = model.vertices[face[3][0] - 1]
                    vt2 = model.texcoords[face[3][1] - 1]
                    d = self.glTransform(vert3, translate, scale)

                normal = cruz(resta(vert1,vert0), resta(vert2,vert0))
                normal = normalized(normal) # la normalizamos
                intensity = punto(int(normal), int(-light))

                if intensity > 1:
                    intensity = 1
                elif intensity < 0:
                    intensity = 0

                self.glTriangle_bc(a, b, c, texCoords = (vt0,vt1,vt2), texture = texture, intensity = intensity)
                if vertCount == 4:
                    self.glTriangle_bc(a, c, d, texCoords = (vt0,vt2,vt3), texture = texture, intensity = intensity)

    # Creación del Bitmap
    def glFinish(self, filename):
        #Crea un archivo BMP y lo llena con la información dentro de self.pixels
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            # Por cada pixel se tienen 3 Bytes
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color Table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
