# Copyright 2018 Nikita Muromtsev (nikmedoed)
# Licensed under the Apache License, Version 2.0 (the «License»)

from src.localisation import localisation
from src.types.position import position
import re
from collections import defaultdict

def element(e):
    return re.sub(r'\d', '', e)

class atom(object):
    def __init__(self, name, x, y = None, z = None, cell = 0):
        if z:
            a = [x, y, z]
        else:
            if y: cell = y
            if x: a = x
            else:
                a = [0] * 3
        self.loc = localisation.loc(__file__)  # text for this file
        self.name = name
        self.initname = name
        self.pow = 0
        self.initpow = 0
        self.rule = -1
        self.element = element(self.name)
        self.pos = position(a)
        self.cell = cell
        self.neighbours = defaultdict(list)
        self.realpos = None
        self.index = -1
        pass
        # self.x, self.y, self.z = list(map(float, [x, y, z]))

    # todo индексы атомов

    def setNeighbour(self, atom):
        self.neighbours[atom.name].append(atom.index)
        #
        # n = atom.name
        # if n in self.neighbours:
        #     self.neighbours[n].append(atom.index)
        # else:
        #     self.neighbours[n]=[atom.index]

    def rotate(self, a, b=None):
        self.pos.rotate(a, b)
        return self

    def getelement(self, i=-1):
        return element(self.getname(i))

    def getname(self, i=-1):
        if self.rule == i or i == -1:
            return self.name
        else:
            return self.initname

    def reset(self):
        self.name = self.initname
        self.pow = self.initpow
        self.rule = -1

    def getpow(self, i=-1):
        if self.rule == i:
            return self.pow
        else:
            return self.initpow

    def setIndex(self,i):
        self.index = i
        return self

    def setRealPos(self, abc):
        self.realpos = self.pos * abc
        return self

    def setcell(self, n):
        self.cell = n
        return self

    def setpow(self, pow):
        self.pow = float(pow)
        self.initpow = self.pow
        return self

    def __str__(self):
        t = "  \x1b[33m%-3s\x1b[0m%s" % (self.name, self.pos)
        return t

    def __repr__(self):
        t = "class atom:  \x1b[33m%-3s\x1b[0m%s cell: %d" % (self.name, self.pos, self.cell)
        return t

    def __add__(self, other):
        if type(other) is atom: other = other.pos
        return atom(self.name, self.pos + other, self.loc)

    def __iadd__(self, other):
        if type(other) is atom: other = other.pos
        self.pos += other
        return self

    def __sub__(self, other):
        if type(other) is atom: other = other.pos
        return atom(self.name, self.pos - other, self.loc)

    def __isub__(self, other):
        if type(other) is atom: other = other.pos
        self.pos -= other
        return self

    def __mul__(self, other):
        if type(other) is atom: other = other.pos
        return atom(self.name, self.pos * other, self.loc)

    def __imul__(self, other):
        if type(other) is atom: other = other.pos
        self.pos *= other
        return self

    def __truediv__(self, other):
        if type(other) is atom: other = other.pos
        return atom(self.name, self.pos / other, self.loc)

    def __itruediv__(self, other):
        if type(other) is atom: other = other.pos
        self.pos /= other
        return self

    def __floordiv__(self, other):
        if type(other) is atom: other = other.pos
        return atom(self.name, self.pos // other, self.loc)

    def __ifloordiv__(self, other):
        if type(other) is atom: other = other.pos
        self.pos //= other
        return self

    def __bool__(self):
        return self.pos.__bool__()

    def __neg__(self):
        return self.pos.__bool__()

    def __mod__(self, other):
        if type(other) is atom: other = other.pos
        return atom(self.name, self.pos % other, self.loc)

    def __imod__(self, other):
        if type(other) is atom: other = other.pos
        self.pos %= other
        return self

    def dist(self, other, ang= None):
        if type(other) is atom: other = other.pos
        return self.pos.dist(other, ang)

    def rdist(self, other, ang=None):
        if type(other) is atom:
            other = other.realpos
        return self.realpos.dist(other, ang)

    def __abs__(self):
        return self.pos.__abs__()

    def __iter__(self):  # мог ошибиться
        return self.pos.__iter__()

    def __pow__(self, other):
        return atom(self.name, self.pos ** other, self.loc)

    def __lt__(self, other):
        if type(other) is atom: other = other.pos
        return self.pos < other

    def list(self):
        return self.pos.list()

    def __le__(self, other):
        if type(other) is atom: other = other.pos
        return self.pos <= other

    def __eq__(self, other):
        if type(other) is atom: other = other.pos
        return self.pos == other

    def __ne__(self, other):
        if type(other) is atom: other = other.pos
        return self.pos != other


    def __gt__(self, other):
        if type(other) is atom: other = other.pos
        return self.pos > other


if __name__ == "__main__":
    a = atom("Fe1", "0.00000", "0.00000", "0.00000")
    b = atom("Fe2", ["0.00000", "3.00000", "0.00000"])
    print(a)
    print(b)
    print(a + [1, 2, 3])
    print(a - [1, 2, 3])
    print(a + b)
