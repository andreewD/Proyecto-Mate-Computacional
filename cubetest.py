import sys
import math
from operator import itemgetter
import pygame

ancho = 800
alto = 600
negro = 0,0,0
VistaDistancia = 4

class Point3D:

    def __init__(self, x, y, z):
        self.x, self.y, self.z = float(x), float(y), float(z)

 	
	#Rota el punto alrededor del eje x segun una angulo engrados.
	
    def rotaX(self, angulo):
        rad = angulo * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

	#Rota el punto alrededor del eje y segun una angulo engrados.
	
    def rotaY(self, angulo):
        rad = angulo * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

	
	#Rota el punto alrededor del eje z segun una angulo engrados.
	
    def rotaZ(self, angulo):
        rad = angulo * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

	
    #Transforma el punto 3D a 2D usando persepectiva de proyeccion
	
    def project(self, win_width, win_height, fov, VistaDistancia):
        factor = fov / (VistaDistancia + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)


class Simulation:

    def __init__(self, ancho, alto):
        pygame.init()

        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Cubo RGB")

        self.clock = pygame.time.Clock()

        self.vertices = [
            Point3D(-1,1,-1),
            Point3D(1,1,-1),
            Point3D(1,-1,-1),
            Point3D(-1,-1,-1),
            Point3D(-1,1,1),
            Point3D(1,1,1),
            Point3D(1,-1,1),
            Point3D(-1,-1,1)
        ]
        #Define los vertices con los que conecta cada cara
        self.faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]
        # Define los colores de cada cara
        self.colors = [(255,0,255),(255,0,0),(0,255,0),(0,0,255),(0,255,255),(255,255,0)]
        self.angle = 0
    

    def Xaxis(self, t):

        for vertice in self.vertices:
            # Rota el punto alrededor del eje x luego el eje y al final el eje z
            rotar = vertice.rotaX(self.angle)
            # Trasnforma el punto de 3D a 2D 256
            proyecion = rotar.project(self.screen.get_width(), self.screen.get_height(), 256, VistaDistancia)
            # Pone el punto en la lista de traformacion de vertices
            t.append(proyecion)


    def Yaxis(self, t):

        for vertice in self.vertices:
            # Rota el punto alrededor del eje x luego el eje y al final el eje z
            rotar = vertice.rotaY(self.angle)
            # Trasnforma el punto de 3D a 2D 256
            proyecion = rotar.project(self.screen.get_width(), self.screen.get_height(), 256, VistaDistancia)
            # Pone el punto en la lista de traformacion de vertices
            t.append(proyecion)


    def Zaxis(self, t):

        for vertice in self.vertices:
            # Rota el punto alrededor del eje x luego el eje y al final el eje z
            rotar = vertice.rotaZ(self.angle)
            # Trasnforma el punto de 3D a 2D 256
            proyecion = rotar.project(self.screen.get_width(), self.screen.get_height(), 256, VistaDistancia)
            # Pone el punto en la lista de traformacion de vertices
            t.append(proyecion)
    
    def Randomrotation(self, t):
        for vertice in self.vertices:
            # Rota el punto alrededor del eje x luego el eje y al final el eje z
            rotar = vertice.rotaX(self.angle).rotaY(self.angle).rotaZ(self.angle)
            # Trasnforma el punto de 3D a 2D 256
            proyecion = rotar.project(self.screen.get_width(), self.screen.get_height(), 256, VistaDistancia)
            # Pone el punto en la lista de traformacion de vertices
            t.append(proyecion)


    def run(self):

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(60)
            self.screen.fill(negro)

            pressed = pygame.key.get_pressed()
    

            # Arreglo para la tranformada de los vertices
            t = []

            if pressed[pygame.K_x]:
                self.Xaxis(t)
            if pressed[pygame.K_y]:
                self.Yaxis(t)
            if pressed[pygame.K_z]:
                self.Zaxis(t)
            else:
                self.Randomrotation(t)

            # Calcula el promedio del valor dez de cada cara
            avg_z = []
            i = 0

            for f in self.faces:
                z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
                avg_z.append([i,z])
                i = i + 1

			
			#Dibuja las caras usando un algoritmo
            for tmp in sorted(avg_z,key=itemgetter(1),reverse=True):
                face_index = tmp[0]
                f = self.faces[face_index]
                pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
                             (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y),
                             (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y),
                             (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y)]
                pygame.draw.polygon(self.screen,self.colors[face_index],pointlist)

            self.angle += 1

            pygame.display.flip()

if __name__ == "__main__":
    Simulation(ancho, alto).run()