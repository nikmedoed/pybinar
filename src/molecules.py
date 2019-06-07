# Copyright 2019 Nikita Muromtsev (nikmedoed)
# Licensed under the Apache License, Version 2.0 (the «License»)

from src.types.atom import atom
from src.types import cell
from src.localisation import localisation
from src.utils.graph2 import buildCells
from src.utils.addons import *


class mol(object):
    def __init__(self, loc = localisation()):
        self.list = []
        self.trans = dict()
        self.local = loc

    def get(self, n):
        return self.list[n] if type(n) is int else self.list[self.trans[n]]

    def readMol(self, link):
        with open(link) as f:
            text = f.read().split('\n')
        n = int (text[3].split()[0])
        text = list(map(lambda x: x.split()[:4], text[4:4+n]))
        atoms = list(map(lambda x: atom(x[3], x[:3], self.local), text))
        rescel = cell.cell(atoms, file=link)
        self.list.append(rescel)
        self.trans[link] = len(self.list)
        self.trans[link.split('\\')[-1]] = len(self.list)-1
        return rescel

# molecules =  mol()

if __name__ == "__main__":
    molecules = mol(localisation("", "Local/"))
    mol = molecules.readMol('..\Methylammonium.mol')
    new = dc(mol)
    print(mol)
    # buildCell(mol)
    # mol.rotate([45, 0, 0])
    # print(mol)
    # buildCell(mol)
    from src import rand

    ran = rand.rand("0", "TIME")
    mol.randRotate(ran)
    print(mol)
    buildCells([mol, new])
