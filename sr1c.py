import struct
import math
from math import ceil
from math import sqrt
from random import randint
from random import uniform
from collections import namedtuple
from textura import Texture

def char(c):
    return struct.pack("=c", c.encode('ascii'))

def word(c):
    return struct.pack("=h", c)

def dword(c):
    return struct.pack("=l", c)

def color(r, g, b):
    return bytes([b, g, r])
2
V2 =  namedtuple('Vertex2',['x', 'y'])
V3 =  namedtuple('Vertex3',['x', 'y', 'z'])

class Obj(object):
    r = 0
    g = 0
    b = 0

    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertices=[]
        self.tvertices = []
        self.faces = []
        self.tfaces = []
        self.read()
    
    def read(self):
        self.materials = self.read_mtlfile("Bender2.mtl")
        for line in self.lines:
            if line:
                prefix, value = line.split(' ',1)

                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))  #map a cada parametro de esto los esta casteando a float , y list los pone en una lista
                elif prefix == 'f':
                    lista = [list(map(int, face.split('/')))for face in value.split(' ')]
                    lista.append(self.r)
                    lista.append(self.g)
                    lista.append(self.b)
                    self.faces.append(lista)
                elif prefix == 'usemtl':
                    Colores = value.split(' ')
                    self.rojo(Colores)
                    self.verde(Colores)
                    self.azul(Colores)

    def rojo(self, cm):
        cl1 = cm
        s1 = ''.join(cl1)
        self.r = ((self.materials[s1]["Kd"][0]))
        return self.r

    def verde(self, cm):
        cl2 = cm
        s2 = ''.join(cl2)
        self.g = ((self.materials[s2]["Kd"][1]))
        return self.g

    def azul(self, cm):
        cl3 = cm
        s3 = ''.join(cl3)
        self.b = ((self.materials[s3]["Kd"][2]))
        return self.b

    #https://github.com/ratcave/wavefront_reader/blob/master/wavefront_reader/reading.py
    def read_mtlfile(self, fname):
        materials = {}
        with open(fname) as f:
            lines = f.read().splitlines()

        for line in lines:
            if line:
                split_line = line.strip().split(' ', 1)
                if len(split_line) < 2:
                    continue

                prefix, data = split_line[0], split_line[1]
                if 'newmtl' in prefix:
                    material = {}
                    materials[data] = material
                elif materials:
                    if data:
                        split_data = data.strip().split(' ')

                        if len(split_data) > 1:
                            material[prefix] = tuple(float(d) for d in split_data)
                        else:
                            try:
                                material[prefix] = int(data)
                            except ValueError:
                                material[prefix] = float(data)

        return materials

class Bitmap():
    r = 0
    g = 0
    b = 0
    red = 255
    green = 255
    blue = 255

    framebuffer = []

    def __Init__(self, width, height):
        self.width = width
        self.height = height 
        self.framebuffer = []
        self.zbuffer = []
        self.glClear()
    
    #crea la imagen
    def glCreateWindow(self, width, height):
        self.h = 0
        self.x = 0
        self.y = 0
        self.xw = 0
        self.yw = 0
        self.height = height
        self.width = width
        self.heighty = 0
        self.widthx = 0
        self.framebuffer = [
            [
                color(self.r, self.g, self.b) for x in range(self.width)#Cielo
            ]
            for y in range(self.height)
        ]
        self.zbuffer = [
            [
                -float('inf') for x in range(self.width)
            ]
            for y in range(self.height)
        ]

    def glViewPort(self, x, y, widthx, heighty):
        self.x = x
        self.y = y
        self.widthx = widthx
        self.heighty = heighty

    #pinta el fondo del color determinado
    def glClear(self):
        self.framebuffer = [
            [
                color(self.r, self.g, self.b) for x in range(self.width)#Cielo
            ]
            for y in range(self.height)     
        ]
        self.zbuffer = [
            [
                -float('inf') for x in range(self.width)
            ]
            for y in range(self.height)
        ]

    def cambioPoint(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def transform(self, vertex, translate=(0, 0,0), scale=(1, 1,1)):
        return V3(
            round(self.decoX((vertex[0] + translate[0]) * scale[0])),
            round(self.decoY((vertex[1] + translate[1]) * scale[1])),
            round(self.decoX((vertex[2] + translate[2]) * scale[2]))
            # round((vertex[0] + translate[0]) * scale[0]),
            # round((vertex[1] + translate[1]) * scale[1]),
            # round((vertex[2] + translate[2]) * scale[2])
        )

    def sum(self, v0,v1):
        return V3(v0.x + v1.x, v0.y + v1.y,v0.z + v1.z)

    def sub(self, v0, v1):
        return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

    def mul(self, v0, k):
        return V3(v0.x * k, v0.y * k, v0.z * k)

    def dot(self, v0, v1):
        return (v0.x * v1.x + v0.y * v1.y + v0.z * v1.z)

    def cross(self, v0, v1):
        return V3(
            v0.y * v1.z - v0.z * v1.y,
            v0.z * v1.x - v0.x * v1.z,
            v0.x * v1.y - v0.y * v1.x
            )
    
    def length(self, v0):
        return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

    def norm(self, v0):
        l = self.length(v0)
    
        if l == 0:
           return V3(0,0,0)
    
        return V3(v0.x/l, v0.y/l, v0.z/l)

    def load(self, filename, translate, scale):
            model = Obj(filename)

            for face in model.faces:
                vcount = len(face)

                for j in range(vcount):
                    f1 = face[j][0]
                    f2 = face[(j+1)%vcount][0]

                    v1 = model.vertices[f1-1]
                    v2 = model.vertices[f2-1]

                    x1 = (v1[0] + translate[0])*scale[0]
                    y1 = (v1[1] + translate[1])*scale[1]
                    x2 = (v2[0] + translate[0])*scale[0]
                    y2 = (v2[1] + translate[1])*scale[1]

                    self.glLine(x1, y1, x2, y2)

    def load2(self, filename, translate, scale, texture = None):
        # declaramos un objeto con el nombre del archivo
        modelo = Obj(filename)
        #print(modelo.faces) 
        
        light = V3(0, 0, 1)

        for face in modelo.faces:

            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1

            a = self.transform(modelo.vertices[f1], translate, scale)
            b = self.transform(modelo.vertices[f2], translate, scale)
            c = self.transform(modelo.vertices[f3], translate, scale)
          
            normal = self.norm(self.cross(self.sub(b, a), self.sub(c, a)))
            intensity = self.dot(normal, light)
            grey = round(255 * intensity)
            
            
            #r = int(face[4]*255)
            #g = int(face[5]*255)
            #b = int(face[5]*255)

            #print(r)
            #print(g)
            #print(b)

            if grey < 0:
                continue 

            if intensity<0:
                continue

            self.triangle2(a, b, c, color(round(100 * intensity), round(100 * intensity), round(100 * intensity)))

    def bbox(self, A, B, C):
        xs =sorted([A.x, B.x, C.x])
        ys =sorted([A.y, B.y, C.y])
        return V2(xs[0],ys[0]), V2(xs[2], ys[2])

    '''
    Line sweeping
    def triangle(self, A, B, C, color = None):
        if A.y > B.y:
            A, B = B, A
        if A.y > C.y:
            A, C = C, A
        if B.y > C.y: 
            B, C = C, B

        dx_ac = C.x - A.x
        dy_ac = C.y - A.y
        if dy_ac == 0:
            return 
        mi_ac = dx_ac/dy_ac

        dx_ab = B.x - A.x
        dy_ab = B.y - A.y
        if dy_ab != 0:
            mi_ab = dx_ab/dy_ab
            for y in range(A.y, B.y + 1):
                xi = round(A.x - mi_ac * (A.y - y))
                xf = round(A.x - mi_ab * (A.y - y))

                if xi > xf:
                    xi, xf = xf, xi
                for x in range(xi, xf + 1):
                    self.point(x, y)
        dx_bc = C.x - B.x
        dy_bc = C.y - B.y
        if dy_bc:
            mi_bc = dx_bc/dy_bc
            for y in range(B.y, C.y + 1):
                xi = round(A.x - mi_ac * (A.y - y))
                xf = round(B.x - mi_bc * (B.y - y))

                if xi > xf:
                    xi, xf = xf, xi
                for x in range(xi, xf + 1):
                    self.point(x, y)

        
    '''
    def barycentric(self, A, B, C, P):
        cx, cy, cz = self.cross(
            V3(B.x - A.x, C.x- A.x, A.x - P.x),
            V3(B.y - A.y, C.y- A.y, A.y-P.y)
        )
        #[cx/cz cy/cz cz/cz]
        if cz == 0: 
            return -1, -1, -1

        u = cx/cz
        v = cy/cz
        w = 1 - u - v
        return w, v, u
    
    def triangle2(self, A, B, C, color=None, texture=None, texture_coords=(), intensity=1):

        bbox_min, bbox_max = self.bbox(A,B,C)
        
        for x in range(bbox_min.x, bbox_max.x +1):
            for y in range(bbox_min.y,bbox_max.y+1):
                w, v, u = self.barycentric(A, B, C, V2(x,y))

                if w < 0  or v<0 or u<0:
                    continue
                #==================Esto se vuelve a la normalidad=========================
                z = A.z * w + B.z*v + C.z * u

                if z > self.zbuffer[x][y]:
                    self.point(x,y, color)
                    self.zbuffer[x][y] = z
                
    def point(self, xw, yw, color):
        self.framebuffer[yw][xw] = color
   
    #se selecciona el color que se desea para el fondo
    def glClearColor(self, r, g, b):
        self.r = ceil(r*255)
        self.g = ceil(g*255)
        self.b = ceil(b*255)
        
    def glVertex(self, x, y):
        xw = ceil((x + 1)*(self.widthx/2)) + self.x
        yw = ceil((y + 1)*(self.heighty/2)) + self.y
        self.point(xw, yw,color(self.red,self.green,self.blue))
            

    def glColor(self, r, g, b):
        self.r = ceil(r*255)
        self.g = ceil(g*255)
        self.b = ceil(b*255) 

    def glLine(self, x1, y1, x2, y2):
        a = round((x1+1)*(self.widthx/2)+self.x)
        ab = round((x2+1)*(self.widthx/2)+self.x)
        ba = round((y1+1)*(self.heighty/2)+self.y)
        b = round((y2+1)*(self.heighty/2)+self.y)
        i = 0
        while i <= 1: 
            x = a + (ab - a) * i
            y = b + (ba - b) * i
                
            self.glVertex(self.coorX(x),self.coorY(y))
            i += 0.01

    def coorX(self,a):
        ansX = 2*((a-self.x)/self.widthx)-1
        return ansX
    def coorY(self,b):
        ansY = 2*((b-self.y)/self.heighty)-1
        return ansY


    def decoX(self, x):
        resultadoX = (((x+1)/2)*self.widthx)+self.x
        return resultadoX
    def decoY(self, y):
        resultadoY = (((y+1)/2)*self.heighty)+self.y
        return resultadoY


    def frange(self,x, y, jump):
        while x < y:
            yield x
            x += jump   

    def glFinish(self, filename):
        f = open(filename, "wb")
        #estandar
        f.write(char('B'))
        f.write(char('M'))
        #file size
        f.write(dword(14 + 40 + self.width * self.height * 3))
        #reserved
        f.write(dword(0))
        #data offset
        f.write(dword(54))
        #header size
        f.write(dword(40))
        #width
        f.write(dword(self.width))
        #height
        f.write(dword(self.height))
        #planes
        f.write(word(1))
        #bits per pixel
        f.write(word(24))
        #compression
        f.write(dword(0))
        #image size
        f.write(dword(self.width * self.height * 3))
        #x pixels per meter
        f.write(dword(0))
        #y pixels per meter
        f.write(dword(0))
        #number of colors
        f.write(dword(0))
        #important colors
        f.write(dword(0))
        #image data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])
        #close file
        f.close()



