"""
Working Voronoi Diagram Generator

"""

import random as r
import math as m
import pygame as pg
from pygame import gfxdraw


def makeMap(numPoints, mapSize):

    # Generate random colors so I can see what's happened.
    colors = []
    for color in range(numPoints):
        red = r.randint(0, 255)
        grn = r.randint(0, 255)
        blu = r.randint(0, 255)
        colors.append((red, grn, blu))

    # Generate the base points.
    ct = 0
    basePoints = []
    for point in range(numPoints):
        x = r.randint(0, mapSize)
        y = r.randint(0, mapSize)
        basePoints.append((x, y, colors[ct]))
        ct += 1

    # Generate all the other points on the map.
    points = []
    for x in range(mapSize):
        for y in range(mapSize):
            distance = mapSize * 2
            for bp in basePoints:
                newDistance = m.sqrt(((x - bp[0]) ** 2) + ((y - bp[1]) ** 2))
                if newDistance < distance:
                    distance = newDistance
                    color = bp[2]
            points.append([x, y, color])

    return points


def colorer(surf, points):
    for p in points:
        gfxdraw.pixel(surf, p[0], p[1], p[2])


def main():
    # Get points.
    points = makeMap(20, 400)
    print("points: ", points)

    # Setup pygame screens.
    pg.init()
    size = (400, 400)
    surf = pg.display.set_mode(size)

    done = False

    # Control fps of window.
    clock = pg.time.Clock()
    fps = 40

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        colorer(surf, points)

        pg.display.flip()

        # Control FPS.
        clock.tick(fps)


if __name__ == "__main__":
    main()