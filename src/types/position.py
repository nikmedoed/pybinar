from math import sqrt
import math


class position (object):
    def __init__(self, x, y = None, z = None):
        if type(x) is list:
            self.x, self.y, self.z = list(map(float, x))
        elif type(x) is position:
            self.x, self.y, self.z = x.x, x.y, x.z
        else:
            # self.loc = local.loc(__file__) # text for this file
            self.x, self.y, self.z = list(map(float, [x, y, z]))

    def rotate(self, a, b=None):
        if b:
            cos = a
            sin = b
        else:
            abc = map(lambda x: x * math.pi / 180, a)
            cos = list(map(math.cos, abc))
            sin = list(map(math.sin, abc))
        a1, b1, c1 = cos
        a2, b2, c2 = sin
        x, y, z = self.x, self.y, self.z
        self.x, self.y, self.z = [
             c2 * (a1 * y + a2 * z) + c1 * (b1 * x - b2 * (-a2 * y + a1 * z)),
             c1 * (a1 * y + a2 * z) - c2 * (b1 * x - b2 * (-a2 * y + a1 * z)),
             b2 * x + b1 * (-a2 * y + a1 * z)
        ]
        return self

    def __add__(self, other):
        if type(other) is list:
            r = position(self.x+other[0], self.y+other[1], self.z+other[2])
        else:
            r = position(self.x+other.x, self.y+other.y, self.z+other.z)
        return r

    def __iadd__(self, other):
        if type(other) is list:
            self.x += other[0]
            self.y += other[1]
            self.z += other[2]
        else:
            self.x += other.x
            self.y += other.y
            self.z += other.z
        return self

    def __sub__(self, other):
        if type(other) is list:
            r = position(self.x-other[0], self.y-other[1], self.z-other[2])
        else:
            r = position(self.x-other.x, self.y-other.y, self.z-other.z)
        return r

    def __isub__(self, other):
        if type(other) is list:
            self.x -= other[0]
            self.y -= other[1]
            self.z -= other[2]
        else:
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        return self

    def __bool__(self):
        return self.x != 0 or self.y != 0 or self.z != 0

    def __neg__(self):
        return position(-self.x, -self.y, -self.z)

    def __mul__(self, other):
        if type(other) is list:
            r = position(self.x*other[0], self.y*other[1], self.z*other[2])
        else:
            r = position(self.x*other.x, self.y*other.y, self.z*other.z)
        return r

    def __imul__(self, other):
        if type(other) is list:
            self.x *= other[0]
            self.y *= other[1]
            self.z *= other[2]
        else:
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        return self

    # todo если потребуется, то сделать векторное произведение и скалярное, потмоу что просто домножение координа это такое себе

    def __truediv__(self, other):
        if type(other) is list:
            r = position(self.x / other[0], self.y / other[1], self.z / other[2])
        else:
            r = position(self.x / other.x, self.y / other.y, self.z / other.z)
        return r

    def __itruediv__(self, other):
        if type(other) is list:
            self.x /= other[0]
            self.y /= other[1]
            self.z /= other[2]
        else:
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        return self

    def __floordiv__(self, other):
        if type(other) is list:
            r = position(self.x // other[0], self.y // other[1], self.z // other[2])
        else:
            r = position(self.x // other.x, self.y // other.y, self.z // other.z)
        return r

    def __ifloordiv__(self, other):
        if type(other) is list:
            self.x //= other[0]
            self.y //= other[1]
            self.z //= other[2]
        else:
            self.x //= other.x
            self.y //= other.y
            self.z //= other.z
        return self

    def __mod__(self, other):
        if type(other) is list:
            r = position(self.x % other[0], self.y % other[1], self.z % other[2])
        else:
            r = position(self.x % other.x, self.y % other.y, self.z % other.z)
        return r

    def __imod__(self, other):
        if type(other) is list:
            self.x %= other[0]
            self.y %= other[1]
            self.z %= other[2]
        else:
            self.x %= other.x
            self.y %= other.y
            self.z %= other.z
        return self

    def dist(self, other, ang=None):
        # if type(other) is list:
        #     r = sqrt((self.x - other[0])**2 + (self.y - other[1])**2 + (self.z - other[2])**2)
        # else:
        r = sum((self-other)**2)
        if ang:
            r += 2*sum([self.y*self.x*ang[0], self.x*self.z*ang[1],  self.z*self.y*ang[2]])
        return sqrt(r)

    def __pow__(self, other):
        # __pow__(self, other[, modulo]) - возведениестепень(x ** y, pow(x, y[, modulo]))
        return position(self.x**other, self.y**other, self.z**other)

    def __abs__(self):
        return sqrt(sum(self**2))

    def __iter__(self):
        return (x for x in [self.x, self.y, self.z])

# __ipow__(self, other[, modulo]) - **=.

    def __lt__(self, other):
        if type(other) is list:
            r = abs(self) < abs(position(other))
        else:
            r = abs(self) < abs(other)
        return r
        #- x < y вызывает x.__lt__(y).

    def list(self):
        return [self.x, self.y, self.z]

    def __le__(self, other):
        if type(other) is list:
            r = abs(self) <= abs(position(other))
        else:
            r = abs(self) <= abs(other)
        return r
        # - x ≤ y вызывает x.__le__(y).

    def __eq__(self, other):
        if type(other) is list:
            r = self.list() == position(other).list()
        else:
            r = self.list() == other.list()
        return r

    def __ne__(self, other):
        if type(other) is list:
            r = self.list() != position(other).list()
        else:
            r = self.list() != other.list()
        return r
        # - x != y вызывает x.__ne__(y)

    def __gt__(self, other):
        if type(other) is list:
            r = abs(self) > abs(position(other))
        else:
            r = abs(self) > abs(other)
        return r
        # - x > y вызывает x.__gt__(y).

    def __ge__(self, other):
        if type(other) is list:
            r = abs(self) >= abs(position(other))
        else:
            r = abs(self) >= abs(other)
        return r
        # - x ≥ y вызывает x.__ge__(y).

    def __str__(self):
        # t ="% 17.10f% 17.10f% 17.10f" % (self.x, self.y, self.z)
        # t = "%17s %17s %17s" % (tuple(map(lambda x: "% 7d.%-10s" % (x // 1, str(x % 1)[3:] if len(str(x % 1)[3:]) > 0 else "0") ,[self.x, self.y, self.z])))
        t = "%15s %15s %15s" % (tuple(map(lambda x: "% 5s.%-10s" % tuple(str(round(x,10)).split(".")), [self.x, self.y, self.z])))
        # t = t.replace("00", "  ")
        return t

    def __repr__(self):
        t = "Position(coordinates): %-12.5f%-12.5f%-12.5f" % (self.x, self.y, self.z)
        return t


if __name__ == "__main__":
    a = position("1.00000", "0.00000", "0.00000")
    b = position(3, 3, 3)
    print(a)
    print (a+[1,2,3])
    print(a+b)
    print (a<b)
    print (a<[1,2,3])

