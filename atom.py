import os
from localisation import localisation
from position import position

class atom(object):
    def __init__(self, name, x, y = None, z = None, cell = 0, local = localisation()):
        if z:
            a = [x, y, z]
        else:
            if y: local = y
            a = x
        self.loc = local.loc(__file__)  # text for this file
        self.name = name
        self.pos = position(a)
        self.cell = cell
        pass
        # self.x, self.y, self.z = list(map(float, [x, y, z]))

    def setcell(self, n):
        self.cell = n
        return self

    def __str__(self):
        t = "  \x1b[33m%-3s\x1b[0m%s" % (self.name, self.pos)
        return t

    def __rerp__(self):
        t = "class atom:  \x1b[33m%-3s\x1b[0m%s" % (self.name, self.pos)
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

    def dist(self, other):
        if type(other) is atom: other = other.pos
        return self.pos.dist(other)

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
