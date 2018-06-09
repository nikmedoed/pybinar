import os
from localisation import localisation
from atom import atom
from addons import *
from functools import reduce


class cell(object):
    def __init__(self, name="", local = localisation()):
        self.loc = local.loc(__file__) # text for this file
        self.file = name
        self.filemain = ""
        self.cell_abc = []
        self.cell_ang = []
        self.atoms = []
        main = True
        self.elements = set()
        self.atomcount = dict()
        with open(name, "r") as file:
            for i in file:
                if "_cell_length" in i:
                    self.cell_abc.append(float(i.split()[1]))
                if "_cell_angle" in i:
                    self.cell_ang.append(float(i.split()[1]))
                if main:
                    if len(i.split()) > 3 : main = False
                if main:
                    self.filemain += i
                else:
                    s = i.split()
                    if not (s[0] in self.elements):
                        self.elements.add(s[0])
                        self.atomcount[s[0]] = 0
                    self.atomcount[s[0]] += 1
                    self.atoms.append(atom(s[0], s[1], s[2], s[3], local).setpow(s[4]))
        self.atomcount = list(self.atomcount.items())
        self.atomcount.sort(key=lambda x: x[0])
        self.atoms.sort(key=lambda x: x.name)

    def printatoms(self):
        r = ""
        r += "\n"+"\n".join(list(map(str, self.atoms)))
        return r

    def printatomsNumeric(self):
        self.atomTEMPcount = dict.fromkeys(self.elements, 0)
        r = ""
        r += "\n".join(list(map(lambda x: numericListFromDic(self.atomTEMPcount, x.name) + str(x), self.atoms)))
        return r

    def __str__(self):
        # l = lambda a, b: str(a) + ":\t" + str(b)
        # if self.color:
        l = lambda a, b: "\x1b[36m" + a + ":\x1b[0m\t" + str(b)

        r = "\n".join(
            map(l,
            [
                "file",
                "cell_abc",
                "cell_ang",
                "elements",
                "atoms"
            ],
            [
                self.file,
                self.cell_abc,
                self.cell_ang,
                self.elements,
                self.printatoms()

            ]
        ))
        return r

class supercell(object):
    def __init__(self, cell, xyz, local = localisation()):
        self.loc = local.loc(__file__) # text for this file
        self.cell = cell
        self.xyz = xyz
        self.atoms = [] # список атомов, в каждом указана связанная с ним ячейка
        self.cells = [] # позиции ячеек
        self.Cmul = reduce(lambda x, y: x*y, self.xyz)
        cellnum = 0
        self.atomcount = list(map(lambda a: [a[0], a[1] * self.Cmul], self.cell.atomcount))
        if cell.atoms == []: local.seterr(self.loc["CellNull"])

        for x in range(self.xyz[0]):
            for y in range(self.xyz[1]):
                for z in range(self.xyz[2]):
                    temp = []
                    for i in cell.atoms:
                        temp.append((i + [x, y, z]).setcell(cellnum))
                    self.atoms.extend(temp)
                    cellnum += 1
                    self.cells.append([x, y, z])
        self.atoms.sort(key=lambda x: x.name)
        self.atomTEMPcount = dict.fromkeys(self.cell.elements, 0)

    def printatoms(self):
        r = ""
        r += "\n"+"\n".join(list(map(
            lambda x: str(x) + ("   \x1b[36mcell:\x1b[0m \x1b[31m%3d\x1b[0m %s" % (x.cell, str(self.cells[x.cell]))),
            self.atoms
        )))
        return r

    def printatomsNumeric(self):
        self.atomTEMPcount = dict.fromkeys(self.cell.elements, 0)
        r = ""
        r += "\n".join(list(map(lambda x: numericListFromDic(self.atomTEMPcount, x.name) + str(x), self.atoms)))
        return r

    def __str__(self):
        r = ""
        # r += "\x1b[36mcell:\x1b[0m\n" + str(self.cell) +
        r += "\nxyz:\t" + str()
        l = lambda a, b: "\x1b[36m" + a + ":\x1b[0m\t" + str(b)

        r = "\n".join(
            map(l,
            [
                "translations",
                "cells",
                "atoms"
            ],
            [
                self.xyz,
                self.cells,
                self.printatoms()
            ]
        ))
        return r


if __name__ == "__main__":
    local = localisation()
    c = cell("Fe4Si4O12_P1.cif", local)
    s = supercell(c, [2, 2, 2], local)
    # print(
    #     "\n".join([
    #         "\x1b[32mCell\x1b[0m",
    #         str(c),
    #         "\n\x1b[32mSupercell\x1b[0m",
    #         str(s)
    #     ])
    # )
    # print(s)
    print(s.printatomsNumeric())

