# Copyright 2018 Nikita Muromtsev (nikmedoed)
# Licensed under the Apache License, Version 2.0 (the «License»)

from src.localisation import localisation
from src.types.atom import atom
from src.utils.addons import *
from src import rand
import math

class cell(object):
    def __init__(self,
                 name,
                 local = localisation(),
                 file="NoneFile",
                 cell_abc=[1, 1, 1],
                 cell_ang=[90, 90, 90]
                 ):
        if type(name) is cell:
            self.loc = name.loc
            self.file = name.file
            self.filemain = name.filemain
            self.cell_abc = name.cell_abc # ab gamma, ac betta, cb alpha
            self.cell_ang = name.cell_ang
            self.cell_cos = list(map(lambda x: math.cos(x*math.pi/180), self.cell_ang))
            self.elements = dc(name.elements)
            self.atomcountdict = name.atomcount
            self.atoms = dc(name.atoms)
            self.atomsBYelements = dc(name.atomsBYelements)
        elif type(name) is list:
            self.file = file
            self.cell_abc = cell_abc
            self.cell_ang = cell_ang
            self.cell_cos = []
            self.elements = set()
            self.atoms = name
            self.loc = local.loc(__file__)
            self.filemain = ""
            self.cell_cos = list(map(lambda x: math.cos(x*math.pi/180), self.cell_ang))
            self.atomcountdict = dict()
            for i in name:
                if not (i.name in self.elements):
                    self.elements.add(i.name)
                    self.atomcountdict[i.name] = 0
                self.atomcountdict[i.name] += 1
            self.atomsBYelements = dict.fromkeys(self.elements)
            for i in self.elements:
                self.atomsBYelements[i] = list(filter(lambda x: x.name == i, self.atoms))
        else:
            self.loc = local.loc(__file__) # text for this file
            self.file = name
            self.filemain = ""
            self.cell_abc = []
            self.cell_ang = []
            self.cell_cos = []
            self.atoms = []
            main = True
            self.elements = set()
            self.atomcountdict = dict()
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
                        if len(s) > 0: # проверить безопасность на примере кати 55к
                            if not (s[0] in self.elements):
                                self.elements.add(s[0])
                                self.atomcountdict[s[0]] = 0
                        self.atomcountdict[s[0]] += 1
                        self.atoms.append(atom(s[0], s[1], s[2], s[3], local).setpow(s[4]))
            self.atomcount = list(self.atomcountdict.items())
            self.atomcount.sort(key=lambda x: x[0])
            self.atoms.sort(key=lambda x: x.name)
            self.atomsBYelements = dict.fromkeys(self.elements)
            for i in self.elements:
                self.atomsBYelements[i] = list(filter(lambda x: x.name == i, self.atoms))

    def refresh(self):
        self.atomcount = list(self.atomcountdict.items())
        self.atomcount.sort(key=lambda x: x[0])

    def getAtoms(self):
        self.atoms = []
        for i in self.atomcount:
            self.atoms.extend(self.atomsBYelements[i[0]])
        return self.atoms

    def printatoms(self):
        r = ""
        r += "\n"+"\n".join(list(map(str, self.atoms)))
        return r

#Todo номера при молекулах должны быть общими, а не начинаться заново

    def printatomsNumeric(self, trans=None):
        self.atomTEMPcount = dict.fromkeys(self.elements, 0)
        r = ""
        r += "\n".join(list(map(lambda x: numericListFromDic(self.atomTEMPcount, x.name) +
                                          (str(x + trans)if trans else str(x)), self.atoms)))
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

    def rotate(self, angles=[0, 0, 0]):
        # Дано углы a,b,c
        abc = list(map(lambda x: x*math.pi/180, angles))
        cos = list(map(math.cos, abc))
        sin = list(map(math.sin, abc))
        for i in self.atoms:
            i.rotate(cos, sin)
        return self

    def randRotate(self, rand):
        self.rotate([rand.rnd(360), rand.rnd(360), rand.rnd(360)])


def getQ(distrib, pairs):
    return sum(list(map(lambda x: x*distrib.index(x), distrib))) / pairs

def getDidtrib(nc, interestedAtoms, it =- 1):
    distrib = [0] * nc
    for iAtom in interestedAtoms:
        count = 0
        for i in iAtom.neighbours:
            if i.getelement(it) != iAtom.getelement(it):
                count += 1
        distrib[count] += 1
    return list(map(lambda x: x/(len(interestedAtoms)+1), distrib))

if __name__ == "__main__":
    local = localisation()
    c = cell("Fe4Si4O12_P1.cif", local)

    # d.file = "dfdfdf"
    # print(c.file)
    # for i in s.atomsBYelements['Fe1']:
    #     print(i)
    # print(d)
    # print(s.printatomsNumeric())
    sc = dc(s)
    r = ['Fe1', 'Sas', 1.5, 10]
    ran = rand.rand("0", "TIME", local)
    z = sc.inserAtoms(ran, r)
    ran.settime()
    sc.refresh()
    g = sc.getAtoms()
    # d = dict.fromkeys(range(8), 0)
    # for i in range(10000):
    #     z = sc.inserAtoms(ran, r)
    #     for k in z:
    #         d[k.cell] += 1
    # print(d)

    # print("\n".join(list(map(lambda x: repr(x), z))))


    print(sc)
