# Write a program to present a cube on the screen.
# Controls allow rotation around any coordinate axis and
# around an arbitrary axis specified by the user.
# The cube should have colored faces and
# be rendered with perspective.

import pygame
import numpy as np
from math import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
COLORES = [(236,112,99),(142,68,173),(41,128,185),(26,188,156),(29,131,72),(241,196,15),(245,176,65),(229,152,102)]
COLORES2 = [(255,0,255),(255,0,0),(0,255,0),(0,0,255),(0,255,255),(255,255,0)]
WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100

circle_pos = [WIDTH/2, HEIGHT/2]  # x, y

angle = 0

points = []

# all the cube vertices
points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1,  1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))

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

# Inputs para el eje a eleccion del usuario
# u_x = 3/sqrt(50)
# u_y = 4/sqrt(50)
# u_z = 5/sqrt(50)

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

    # rotation_any_axis = np.matrix([
    #     [cos(angle)+pow(u_x, 2)*(1-cos(angle)),
    #      u_x*u_y*(1-cos(angle)) - u_z*sin(angle),
    #      u_x*u_z*(1-cos(angle))+u_y*sin(angle)],

    #     [u_y*u_x*(1-cos(angle))+u_z*sin(angle),
    #      cos(angle)+pow(u_y, 2)*(1-cos(angle)),
    #      u_y*u_z*(1-cos(angle))-u_x*sin(angle)],

    #     [u_z*u_x*(1-cos(angle))-u_y*sin(angle),
    #      u_z*u_y*(1-cos(angle)) + u_x*sin(angle),
    #      cos(angle)+pow(u_z, 2)*(1-cos(angle))]
    # ])

    angle += 0.01

    screen.fill(WHITE)
    # drawining stuff

    i = 0
    for point in points:
        # Rotacion en todos los ejes
        rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
        rotated2d = np.dot(rotation_y,rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        # Rotacion en eje especifico
        # rotated2d = np.dot(rotation_any_axis, point.reshape((3, 1)))

        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, RED, (x, y), 5)
        i += 1

    pygame.draw.polygon(screen,COLORES2[0],((
        projected_points[0][0], projected_points[0][1]), (projected_points[1][0], projected_points[1][1]),
    (projected_points[2][0], projected_points[2][1]), (projected_points[3][0], projected_points[3][1])))

    pygame.draw.polygon(screen,COLORES2[1],((
        projected_points[0][0], projected_points[0][1]), (projected_points[1][0], projected_points[1][1]),
    (projected_points[5][0], projected_points[5][1]), (projected_points[4][0], projected_points[4][1])))

    pygame.draw.polygon(screen,COLORES2[2],((
        projected_points[3][0], projected_points[3][1]), (projected_points[0][0], projected_points[0][1]),
    (projected_points[4][0], projected_points[4][1]), (projected_points[7][0], projected_points[7][1])))
    
    pygame.draw.polygon(screen,COLORES[3],((
        projected_points[2][0], projected_points[2][1]), (projected_points[3][0], projected_points[3][1]),
    (projected_points[7][0], projected_points[7][1]), (projected_points[6][0], projected_points[6][1])))

    pygame.draw.polygon(screen,COLORES[4],((
        projected_points[1][0], projected_points[1][1]), (projected_points[2][0], projected_points[2][1]),
    (projected_points[6][0], projected_points[6][1]), (projected_points[5][0], projected_points[5][1])))

    pygame.draw.polygon(screen,COLORES[5],((
        projected_points[6][0], projected_points[6][1]), (projected_points[7][0], projected_points[7][1]),
    (projected_points[4][0], projected_points[4][1]), (projected_points[5][0], projected_points[5][1])))
    
    for p in range(4):
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        connect_points(p, (p+4), projected_points)
    
    

    pygame.display.update()
