from functools import reduce

from src import molecules as molecules
from src.localisation import localisation
from src.types.cell import cell, getDidtrib, getQ
from src.utils.addons import numericListFromDic


class supercell(object):
    def __init__(self, cell, xyz=None, local = localisation()):
        if xyz is None:
            xyz = [1, 1, 1]
        if type(cell) is supercell:
            pass
            raise NotImplementedError("Now I can't to copy, use dc() (deepcopy)")
            #todo нормальное копирование
        else:
            self.loc = local.loc(__file__) # text for this file
            self.cell = cell
            self.xyz = xyz
            self.atoms = [] # список атомов, в каждом указана связанная с ним ячейка
            self.cells = [] # позиции ячеек
            self.Cmul = reduce(lambda x, y: x*y, self.xyz)
            self.atomcountdict = dict()
            for i in cell.atomcountdict:
                self.atomcountdict[i] = self.cell.atomcountdict[i] * self.Cmul
            cellnum = 0
            self.atomcount = list(map(lambda a: [a[0], a[1] * self.Cmul], self.cell.atomcount))
            if cell.atoms == []: local.seterr(self.loc["CellNull"])

            for x in range(self.xyz[0]):
                for y in range(self.xyz[1]):
                    for z in range(self.xyz[2]):
                        temp = []
                        for i in cell.atoms:
                            temp.append((i + [x, y, z]).setcell(cellnum).setRealPos(self.cell.cell_abc))
                        self.atoms.extend(temp)
                        cellnum += 1
                        self.cells.append([x, y, z])
            self.atoms.sort(key=lambda x: x.name)
            self.interestedAtoms = self.atoms
            self.atomTEMPcount = dict.fromkeys(self.cell.elements, 0)
            self.atomsBYelements = dict.fromkeys(self.cell.elements)
            for i in self.cell.elements:
                self.atomsBYelements[i] = list(filter(lambda x: x.name == i, self.atoms))

    def addAtomSort(self, s):
        if not (s in self.atomcountdict):
            self.atomcountdict[s] = 0
            self.atomsBYelements[s]=[]

    def addNeighbours(self, sprad, atomsForChange=None):
        [x, y, z] = list(map(lambda x: x[0]*x[1], zip(self.xyz, self.cell.cell_abc)))
        corrections = []
        neiCount = -1
        for a in [-x, 0, x]:
            for b in [-y, 0, y]:
                for c in [-z, 0, z]:
                    corrections.append([a, b, c])
        if atomsForChange:
            self.interestedAtoms = list(filter(lambda x: x.element in atomsForChange, self.atoms))
        atoms = self.interestedAtoms
        for i in atoms:
            i.neighbours = list(filter(lambda x: (i!=x) and any( i.rdist(x.realpos + y, self.cell.cell_cos) <= sprad
                                                                 for y in corrections), atoms))
            if neiCount == -1:
                neiCount = len(i.neighbours)
            else:
                if neiCount != len(i.neighbours):
                    print (self.loc['Neighbours'], i)
                # Todo бросать ошибку , если число соседей не совпало
                # local.seterr(self.loc["CellNull"])
        return neiCount

    def refresh(self):
        self.cell.refresh()
        for i in cell.atomcountdict:
            self.atomcountdict[i] = self.cell.atomcountdict[i] * self.Cmul
        self.atomcount = list(map(lambda a: [a[0], a[1] * self.Cmul], self.cell.atomcount))
        self.atomsBYelements = dict.fromkeys(self.cell.elements)
        for i in self.cell.elements:
            self.atomsBYelements[i] = list(filter(lambda x: x.name == i, self.atoms))
        # self.getAtoms() #замедлит работу. надо ли? может делать именно для вывода?

    def getAtoms(self):
        self.atoms = []
        for i in self.atomcountdict:
            self.atoms.extend(self.atomsBYelements[i])
        return self.atoms

    def printatoms(self):
        r = ""
        r += "\n"+"\n".join(list(map(
            lambda x: str(x) + ("   \x1b[36mcell:\x1b[0m \x1b[31m%3d\x1b[0m %s" % (x.cell, str(self.cells[x.cell]))),
            self.atoms
        )))
        return r

    def insertAtoms(self, rand, rule):
        self.cell.elements.add(rule[1])
        t = self.atomsBYelements[rule[0]]
        l = len(t)
        res = []
        for i in range(rule[3]):
            while 1:
                r = rand.rnd(l, int)
                if t[r].name == rule[0]: break
            t[r].name = rule[1]
            t[r].pow = rule[2]
            t[r].rule = rule[4]
            res.append(t[r])
        self.atomcountdict[rule[1]] += rule[3]
        self.atomcountdict[rule[0]] -= rule[3]
        return res

    def getDisttribution(self, rules):
        # if not atomsForChange:
        #     atomsForChange = set(element(x[0]) for x in rules).union(element(x[1]) for x in rules)

        nc = len(self.interestedAtoms[0].neighbours)+1

        distrib = getDidtrib(nc, self.interestedAtoms, -1)
        distribution = {-1: distrib}
        Q = {-1: getQ(distrib, nc)}

        if len(rules) > 1:
            for r in rules:
                index = rules.index(r)
                interestedAtoms = list(filter(lambda x: x.element in r[:1], self.interestedAtoms))
                distrib = getDidtrib(nc, interestedAtoms, index)
                distribution[index] = distrib
                Q[index] = getQ(distrib, nc)
        return [distribution, Q]

    def printatomsNumeric(self):
        self.atomTEMPcount = dict.fromkeys(self.cell.elements, 0)
        r = ""
        r += "\n".join(list(map(lambda x: numericListFromDic(self.atomTEMPcount, x.name) + str(x), self.atoms)))
        return r

#todo выводить координаты с коррекцией т.е. как-то передавать в молекулу позицию

    def printatomsRulesNumeric(self, n=-1):
        self.atomTEMPcount = dict.fromkeys(self.cell.elements, 0)
        r = ""
        r += "\n".join(list(map(lambda x:
                                (molecules.molecules.get(x.getname(n)).printatomsNumeric(x.pos) if '.mol' in x.getname(n)
                                        else (numericListFromDic(self.atomTEMPcount, x.getname(n)) + str(x)))
                                 , self.atoms)))
        return r
    # todo вменяемый вывод без лишних символов, по порядку и все такое

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
    # d = supercell(s)