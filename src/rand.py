# Copyright 2018 Nikita Muromtsev (nikmedoed)
# Licensed under the Apache License, Version 2.0 (the «License»)

from src.localisation import localisation
import random
from src.types import position
import time

class rand(object):
    def __init__(self, generator, randomp):
        self.loc = localisation.loc(__file__) # text for this file
        self.randomp = randomp
        if generator == '0':
            self.generator = "python standart"
            self.rand = random.Random(x=randomp)
        elif generator == '1':
            self.generator = "our"
            self.rand = random.Random(x=randomp)
            # todo реализовать свой генератор
        else:
            self.generator = "special = " + generator
            self.rand = random.Random(x=randomp)
            # ToDo сделать интерпретацию генераторов

    def rnd(self, x = 1, f = float, step=None): # в том числе дробные шаги
        if step:
            r = round(f(self.rand.random() * x) / step) * step
        else:
            r = f(self.rand.random() * x)

        return r


    def rndpos(self, *args, **fun):
        if not 'f' in fun: fun['f'] = float
        if not 'step' in fun: fun['step'] = None
        x,y,z = [1] * 3
        if len(args) == 1:
            x, y, z = [args[0]] * 3
        if len(args) == 3:
            x, y, z = args
        return position.position(self.rnd(x, **fun), self.rnd(y, **fun), self.rnd(z, **fun))

    def settime(self, t = time.time()):
        if self.randomp == "TIME":
            self.randomp = t
            self.rand.seed(t)


    def __str__(self):
        return "\n".join(list(map(lambda x, y: "%s:\t%s" % (x, y),
           ["generator",
            "randomp",
            "rand test"
            ],
          [self.generator,
           self.randomp,
           self.rnd()
           ]
        )))


# Class Random can also be subclassed if you want to use a different basic
# generator of your own devising: in that case, override the following
# methods:  random(), seed(), getstate(), and setstate().
# Optionally, implement a getrandbits() method so that randrange()
# can cover arbitrarily large ranges.

# class SystemRandom(Random):
#     """Alternate random number generator using sources provided
#     by the operating system (such as /dev/urandom on Unix or
#     CryptGenRandom on Windows).
#
#      Not available on all systems (see os.urandom() for details).
#     """
#
#     def random(self):
#         """Get the next random number in the range [0.0, 1.0)."""
#         return (int.from_bytes(_urandom(7), 'big') >> 3) * RECIP_BPF
#
#     def getrandbits(self, k):
#         """getrandbits(k) -> x.  Generates an int with k random bits."""
#         if k <= 0:
#             raise ValueError('number of bits must be greater than zero')
#         if k != int(k):
#             raise TypeError('number of bits should be an integer')
#         numbytes = (k + 7) // 8  # bits / 8 and rounded up
#         x = int.from_bytes(_urandom(numbytes), 'big')
#         return x >> (numbytes * 8 - k)  # trim excess bits
#
#     def seed(self, *args, **kwds):
#         "Stub method.  Not used for a system random number generator."
#         return None
#
#     def _notimplemented(self, *args, **kwds):
#         "Method should not be called for a system random number generator."
#         raise NotImplementedError('System entropy source does not have state.')
#
#     getstate = setstate = _notimplemented


if __name__ == "__main__":
    # a = rand(0, "TIME")
    # b = rand(0, "TIME")
    # print(a)
    #
    # b.settime(time.time())
    # print(b.rndpos(step=0.1))
    c = rand('0', "TIME")
    k = 0
    for i in range(10000):
        k += 1
        if c.rnd(10, int) == 9:
            print("OK", k)
            k = 0

