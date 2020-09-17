# Copyright 2018 Nikita Muromtsev (nikmedoed)
# Licensed under the Apache License, Version 2.0 (the «License»)

from src.utils.parametrsPrint import printparam
from src.localisation import localisation
from src.rand import rand
import os
from math import factorial
from functools import reduce
from src.types.cell import cell
from src.types.supercell import supercell
from src.types.atom import element
from src.iterationResult import iterationResult
import src.types.molecules as molecules
import pickle
from time import time

class inData(object):
    """
    paramets reader

    initialize from input file and makes structure with raw parametrs and their interpretations
    rawparam - list
    cell - object with cell from cell file (gulp)
    supercell - reproduction of a given cell
    random - insertion position generator
    insertionRules -insertion rules
    timeLimit - time limit for experiments in seconds

    """
    # todo накрутить сообщений об ошибках

    def __init__(self, infile=""):
        self.loc = localisation.loc(__file__) # text for this file
        self.rawparam = {}
        self.time = 0
        block = ""
        if infile == "":
            print(self.loc['InError'])
            raise Exception
        if not os.path.exists(infile):
            print(self.loc['InFileFalse'])
            raise Exception

        f = open(infile, "r", encoding="utf-8")
        for i in f:
            i = i.split("//")[0].strip()
            # print("n", i, "n")
            if len(i) > 0:
                # print(len(i))
                if i[len(i)-1] == ":":
                    block = i[:len(i)-1]
                    self.rawparam[block] = []
                else:
                    self.rawparam[block].append(i)

        conditions = self.rawparam['Сonditions']
        self.random = rand(conditions[1], conditions[2])
        self.insertionRules = []
        index = 0
        for k in conditions[3:]:
            i = k.replace(">", " ").replace("(", " ").replace(")", " ").split()
            if '.mol' in i[1]:
                molecules.molecules.readMol(i[1])
                i[1]=i[1].replace(".mol", "")
            i[2] = float(i[2])
            if len(i) == 3:
                i.insert(2, 0)
            i[3] = int(i[3])
            i.append(index)
            index += 1
            self.insertionRules.append(i)

        const = self.rawparam['Сonstraints']
        self.timeLimit = int(const[0])*60 if not (":" in const[0]) else \
            sum(map(lambda x, y: int(x)*y, const[0].split(":"), [3600, 60, 1]))
        k=1
        # self.sphere2 = float(const[1])
        self.sphere1 = float(const[k])
        k+=1
        self.x2toLess = "0" == const[k]
        k+=1
        self.x2stop = float(const[k])
        self.x2stop = float(const[k])

        outp = self.rawparam["Output"]
        tmp = outp[0].split()
        self.x2fround_l = float(tmp[0])
        self.x2fround_r = float(tmp[1]) if len(tmp) > 1 else 0 if self.x2toLess else 100
        if self.x2fround_l > self.x2fround_r:
            self.x2fround_l = self.x2fround_r
            self.x2fround_r = float(tmp[0])

        self.Ntoprint = int(outp[1])
        self.pprint = printparam(outp[2:])
        self.atomsForChange = set(element(x[0]) for x in self.insertionRules) \
            .union(element(x[1]) for x in self.insertionRules)

        superDimensions = list(map(int, (conditions[0]).split()))
        chache = ".".join(infile.split(".")[:-1]) + ".pybinarchache"
        self.cell = cell(self.rawparam['Name'][0])
        print(self.loc['Readed'] + "\n")
        readed = False
        if os.path.exists(chache):
            print(self.loc['SuperFind'], "-", chache)
            try:
                with open(chache, "rb") as s:
                    cellTemp = pickle.load(s)
                    self.supercell = pickle.load(s)
                    self.supercell.cell = self.cell
                if (superDimensions == self.supercell.xyz) and (cellTemp == self.cell):
                    print(self.loc['SuperOk'], chache)
                    readed = True
            except Exception as err:
                print(self.loc['SuperNo'], chache)
                print("Information:", err)

        if not readed:
            self.supercell = supercell(self.cell, superDimensions)
            self.supercell.addNeighbours(self.sphere1, self.atomsForChange)
            with open(chache, "wb") as s:
                pickle.dump(self.cell, s)
                pickle.dump(self.supercell, s)

        # количество соседей
        self.theoretical()
        print(self.loc['Prepared'])

    def theoretical(self):
        """ рассчёт теоретической вероятности и теоретических параметров"""

        self.theoreticalProbability = {}
        self.theoreticalQ = {}
        self.theoreticalProbabilitySegments = {}
        self.proportions = {}
        self.positionsToChange = 0


        for i in self.atomsForChange:
            co = 0
            for g in self.supercell.atomsBYelements:
                if i in g:
                    co += len(self.supercell.atomsBYelements[g])
            self.proportions[i] = co
            self.positionsToChange += co

        pr = self.proportions.copy()
        for r in self.insertionRules:
            self.supercell.addAtomSort(r[1])  # добавляем сорта в словарь суперячейки
            pr[element(r[0])] -= r[3]
            pr[element(r[1])] += r[3]
        for x in pr:
            pr[x] /= self.positionsToChange
        self.theoreticalQ[-1] = 2 * reduce(lambda res, x: res * x, pr.values(), 1) / sum(pr.values()) ** 2

        # число соседей в какой-то степени логичнее считать для каждого вывода отдельно, т.к. в правиле
        # участвует один элемент, а в общем выводе все элементы, что влияет на число соседей
        # при отдельном подсчёте.
        # Но я решил, что будет правильно считать число соседей среди всех атомов,
        # участвующих во всех правилах замены, т.к. это будет в каждом отдельном правиле давать распределение
        # с учётом атомов из всех правил (т.е. сравнимые друг с другом распределения),
        # а если человек захочет получить распределение по атомам только одного
        # правила, то пусть запустит эксперимент с одним правилом.
        # Вопрос: насколько практически нужно получать результат при распределении атомов
        # только участвующих в отдельном правиле, когда делаешь эксперимент с несколькими атомами.
        # В общем для задачи главное сравнивать распределения с эталонные для одновременного применения замен
        self.supercell.neighboursGeneralCountInit(self.atomsForChange)
        prob = []
        probabilitySegments = []
        for i in range(0, self.supercell.neighboursCount + 1):
            M = factorial(self.supercell.neighboursCount) / (factorial(i) * factorial(self.supercell.neighboursCount - i))
            pro = dict(map(lambda x: (x, pr[x] ** (self.supercell.neighboursCount - i) * (1 - pr[x]) ** i * M * pr[x]), pr))
            prob.append(sum(pro.values()))
            probabilitySegments.append(pro)
        self.theoreticalProbabilitySegments[-1] = probabilitySegments
        self.theoreticalProbability[-1] = prob

        if len(self.insertionRules) > 1:
            for r in self.insertionRules:
                rule = self.insertionRules.index(r)
                prob = []
                probabilitySegments = []
                pr = {}  # специально смотрим только участников конкретного правила при подсчете всей вероятности (так было запрошено)
                a = element(r[0])
                b = element(r[1])
                pr[a] = self.proportions[a] - r[3]
                pr[b] = self.proportions[b] + r[3]
                for x in pr:
                    pr[x] /= self.positionsToChange
                for i in range(0, self.supercell.neighboursCount + 1):
                    M = factorial(self.supercell.neighboursCount) / (factorial(i) * factorial(self.supercell.neighboursCount - i))
                    pro = dict(map(lambda x: (x, pr[x] ** (self.supercell.neighboursCount - i) * (1 - pr[x]) ** i * M * pr[x]), pr))
                    prob.append(sum(pro.values()))
                    probabilitySegments.append(pro)
                self.theoreticalProbabilitySegments[rule] = probabilitySegments
                self.theoreticalProbability[rule] = prob
                self.theoreticalQ[rule] = 2 * reduce(lambda res, x: res * x, pr.values(), 1) / sum(pr.values()) ** 2

    def reset(self):
        for ruleResult in self.insertionResult:
            for atom in ruleResult:
                atom.reset()

    def iteration(self):
        start = time()

        # todo все текстовые сравнения элементов перевести на индексы, а называния элементов в словарь
        self.insertionResult = []
        for i in self.insertionRules:
            self.insertionResult.append(self.supercell.insertAtoms(self.random, i))
        res = self.supercell.getDisttribution(self.insertionRules)
        iterDistribution = res[0]
        iterQ = res[1]
        iterXI2 = {}
        iterQdiff = {}
        for i in iterDistribution:
            s = listDiff(iterDistribution[i], self.theoreticalProbability[i])
            iterXI2[i] = sum(s)
            iterQdiff[i] = iterQ[i] - self.theoreticalQ[i]
        iterTime = time() - start
        self.time += iterTime
        return iterationResult(iterDistribution, iterXI2, iterQ, iterQdiff, iterTime)

    def __repr__(self):
        return "inData class"

    def __str__(self):
        t = "\n".join([
            "\n\x1b[32mrawparam\x1b[0m",
            self.rawparam.__str__().replace("'], '", "'], \n'").replace("': ['", "':\t['"),
            "\n\x1b[32mcell\x1b[0m",
            str(self.cell),
            "\n\x1b[32msupercell\x1b[0m",
            str(self.supercell),
            "\n\x1b[32mrandom\x1b[0m",
            str(self.random),
            "\n\x1b[32mtimeLimit\x1b[0m",
            str(self.timeLimit),
            "\n\x1b[32mRules\x1b[0m",
            str(self.insertionRules),
            "\n\x1b[32mParam\x1b[0m",
            # "sphere2:\t" + str(self.sphere2),
            "sphere1:\t" + str(self.sphere1),
            "x2toLess:\t" + str(self.x2toLess),
            "x2stop:\t" + str(self.x2stop),
            "\n\x1b[32mOutparam\x1b[0m",
            "x_left_out:\t" + str(self.x2fround_l),
            "x_right_out:\t" + str(self.x2fround_r),
            "NtoPrint:\t" + str(self.Ntoprint),
            "\nPrintParam:\n" + str(self.pprint)
        ])
        return t

def listDiff(a,b):
    s = []
    for g in range(len(a)):
        s.append((a[g] - b[g]) ** 2)
    return s

if __name__ == "__main__":
    i = inData("exampleinput.txt")
    print(i)