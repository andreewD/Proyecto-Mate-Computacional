# Write a program to keeping track of a cube
# of edge length 2 centered at (0,0,1).
# Use a world coordinate system, a local coordinate
# system, and a camara coordinate system.
# Draw the cube on the creen and allow the
# user to rotate around the cube's center or
# around the world origin.

import pygame
import numpy as np
from math import *

from pygame.constants import BLEND_PREMULTIPLIED

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0,0,230)
Colores = [(236,112,99),(142,68,173),(41,128,185),(26,188,156),(29,131,72),(241,196,15),(245,176,65),(229,152,102)]

WIDTH, HEIGHT = 1000, 1000
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 150

circle_pos = [WIDTH/2, HEIGHT/2]  # x, y

angle = 0

points = []

# all the cube vertices
points.append(np.matrix([-1,1,0]))
points.append(np.matrix([1,1,0]))
points.append(np.matrix([1,-1,0]))
points.append(np.matrix([-1,-1,0]))
points.append(np.matrix([-1,1,2]))
points.append(np.matrix([1,1,2]))
points.append(np.matrix([1,-1,2]))
points.append(np.matrix([-1,-1,2]))


projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])


projected_points = [
    [n, n] for n in range(len(points))
]


def connect_points(i, j, points):
    pygame.draw.line(
        screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))


clock = pygame.time.Clock()
while True:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # update stuff
    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])
    angle += 0.02

    traslation_x = np.matrix([[1,0,0,1],[1,0,0,0],[1,0,0,0],[0,0,0,1]])

    screen.fill(WHITE)

    # drawining stuff
    i = 0
    for point in points:
        rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        # maxt = np.matrix([rotated2d.getA()[0],rotated2d.getA()[1],rotated2d.getA()[2],rotated2d.getA()[1]])
        # matrux = np.dot(traslation_x,maxt)
        # rotated2d = np.matrix([matrux.getA()[0],matrux.getA()[1],matrux.getA()[2]])


        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, Colores[i], (x, y), 5)
        i += 1

    for p in range(4):
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        connect_points(p, (p+4), projected_points)

    # #Proyeccion Del Eje Coordenado
    # ejex = np.dot(projection_matrix, np.matrix([[10],[0],[0]]))
    # ejey = np.dot(projection_matrix, np.matrix([[0],[20],[0]]))
    # ejez = np.dot(projection_matrix, np.matrix([[0],[0],[30]]))
    # #EjeX
    # ejexx = int( ejex.getA()[0][0] * scale) + circle_pos[0]
    # ejexy = int( ejex.getA()[1][0] * scale) + circle_pos[1]
    # #EjeY
    # ejeyx = int( ejey.getA()[0][0] * scale) + circle_pos[0]
    # ejeyy = int( ejey.getA()[1][0] * scale) + circle_pos[1]
    # #EjeZ
    # ejezx = int( ejez.getA()[0][0] * scale) + circle_pos[0]
    # ejezy = int( ejez.getA()[1][0] * scale) + circle_pos[1]
    # #Dibujando los Ejes Coordenados en la Grafica
    # pygame.draw.line(screen, BLUE, (circle_pos[0], circle_pos[1]), (ejexx,ejexy), 2)
    # pygame.draw.line(screen, BLUE, (circle_pos[0], circle_pos[1]), (ejeyx,ejeyy), 2)
    # pygame.draw.line(screen, BLUE, (circle_pos[0], circle_pos[1]), (ejezx,ejezy), 2)

    #Proyeccion Del Eje Coordenado
    #EjeX
    ejexx = int(-50 * scale) + circle_pos[0]
    ejexy = int(50 * scale) + circle_pos[1]
    #EjeY
    ejeyx = int(50 * scale) + circle_pos[0]
    ejeyy = int(0 * scale) + circle_pos[1]
    #EjeZ
    ejezx = int(0 * scale) + circle_pos[0]
    ejezy = int(50 * scale) + circle_pos[1]
    #Dibujando los Ejes Coordenados en la Grafica
    pygame.draw.line(screen, RED, (circle_pos[0], circle_pos[1]), (ejexx,ejexy), 2)
    pygame.draw.line(screen, RED, (circle_pos[0], circle_pos[1]), (ejeyx,ejeyy), 2)
    pygame.draw.line(screen, RED, (circle_pos[0], circle_pos[1]), (ejezx,-ejezy), 2)

    pygame.display.update()