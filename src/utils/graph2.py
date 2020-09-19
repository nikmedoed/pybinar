# Copyright 2019 Nikita Muromtsev (nikmedoed)
# Licensed under the Apache License, Version 2.0 (the «License»)

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy
import random

def randomColor():
    return (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

def bulidXYZ (x, y, z, text="", ax=None, color=None):
    if not ax:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    if not color:
        color = randomColor()
    ax.scatter(x, y, z, c=color, s=100)
    for i in range(len(text)):
        ax.text(x[i], y[i], z[i], text[i], size=12, zorder=1, color='k')
    return ax

def buildCell(cell, ax= None):
    atoms = cell.atoms
    atrans = list(zip(*atoms))
    names = list(map(lambda x: x.name, cell.atoms))
    if ax:
        return bulidXYZ(*atrans, names, ax)
    else:
        plt.show()

def buildCells(cells):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in cells:
        ax = buildCell(i, ax)
    plt.show()

if __name__ == "__main__":
    bulidXYZ(
        [0.7378, -0.7378, 1.1125, 1.1126, 1.1125, -1.0718, -1.0717, -1.0717],
        [0.0000, 0.0000, -0.3153, -0.6256, 0.9409, -1.0210, 0.3422, 0.6788],
        [0.0000, 0.0000, -0.9044, 0.7252, 0.1791, -0.1943, 0.9814, -0.7870]
    )
    plt.show()