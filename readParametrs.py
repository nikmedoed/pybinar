from localisation import localisation
from rand import rand
import os
import json
from math import factorial
from functools import reduce
from cells import cell, supercell
from atom import element
from copy import deepcopy
from time import time
from iterationResult import iterationResult

class printparam(object):
    """
    Class for printing parametrs from input file
    At initialisation gets 'param' - list of text data ("0" or "1") and translate it to boolean
    """
    def __init__(self, param, local=localisation()):
        loc = local.loc(__file__)  # text for this file
        [self.input,
         self.replication,
         self.cations_2sphere_cat,
         self.cations_2sphere_ani,
         self.cations_1sphere_cat,
         self.cations_1sphere_ani,
         self.min_x2,
         self.P_distrib,
         self.cations_conf,
         self.final_conf,
         self.GULP,
         self.distrib_diag
         ] = list(map(lambda x: x == "1", param))

    def __str__(self):
        t = "\n".join(
        map(lambda a,b: "\x1b[36m" + a + ":\x1b[0m\t" + str(b),
            ["input cell coordinates",
             "replication",
            "cations_2sphere_cat",
            "cations_2sphere_ani",
            "cations_1sphere_cat",
            "cations_1sphere_ani",
            "min_x2",
            "P_distrib",
            "cations_conf",
            "final_conf",
            "GULP",
            "distrib_diag"],
            [self.input,
             self.replication,
             self.cations_2sphere_cat,
             self.cations_2sphere_ani,
             self.cations_1sphere_cat,
             self.cations_1sphere_ani,
             self.min_x2,
             self.P_distrib,
             self.cations_conf,
             self.final_conf,
             self.GULP,
             self.distrib_diag
             ])
        )
        return t


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

    def __init__(self, infile="", local=localisation()):
        self.local = local
        self.loc = local.loc(__file__) # text for this file
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

        self.cell = cell(self.rawparam['Name'][0], local)
        conditions = self.rawparam['Сonditions']
        self.supercell = supercell(self.cell, list(map(int, (conditions[0]).split())), local)
        self.random = rand(conditions[1], conditions[2], local)
        self.insertionRules = []
        index = 0
        for k in conditions[3:]:
            i = k.replace(">", " ").replace("(", " ").replace(")", " ").split()
            i[2] = float(i[2])
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
        self.pprint = printparam(outp[2:], local)
        print(self.loc['Readed'])
        self.tProb = {}
        self.tQ = {}
        self.proportions = {}
        self.positionsToChange = 0

        self.atomsForChange = set(element(x[0]) for x in self.insertionRules).union(element(x[1]) for x in self.insertionRules)
        self.neigboards = self.supercell.addNeighbours(self.sphere1, self.atomsForChange) # количество соседей
        self.theoretical()
        print(self.loc['Prepared'])

    def theoretical(self):
        for i in self.atomsForChange:
            co = 0
            for g in self.supercell.atomsBYelements:
                if i in g:
                    co += len(self.supercell.atomsBYelements[g])
            self.proportions[i] = co
            self.positionsToChange += co

        prob = []
        pr = self.proportions.copy()
        for r in self.insertionRules:
            self.supercell.addAtomSort(r[1])  # добавляем сорта в словарь суперячейки
            pr[element(r[0])] -= r[3]
            pr[element(r[1])] += r[3]
        for x in pr:
            pr[x] /= self.positionsToChange
        self.tQ[-1] = 2 * reduce(lambda res, x: res * x, pr.values(), 1) / sum(pr.values()) ** 2
        for i in range(0, self.neigboards + 1):
            M = factorial(self.neigboards) / (factorial(i) * factorial(self.neigboards - i))
            pro = list(map(lambda x: pr[x] ** (self.neigboards - i) * (1 - pr[x]) ** i * M * pr[x], pr))
            prob.append(sum(pro))
        self.tProb[-1] = prob
        # todo все текстовые сравнения элементов перевести на индексы, а называния элементов в словарь
        if len(self.insertionRules) > 1:
            for r in self.insertionRules:
                rule = self.insertionRules.index(r)
                prob = []
                pr = {}  # специально смотрим только участников конкретного правила при подсчете всей вероятности (так было запрошено)
                a = element(r[0])
                b = element(r[1])
                pr[a] = self.proportions[a] - r[3]
                pr[b] = self.proportions[b] + r[3]
                for x in pr:
                    pr[x] /= self.positionsToChange
                for i in range(0, self.neigboards + 1):
                    M = factorial(self.neigboards) / (factorial(i) * factorial(self.neigboards - i))
                    pro = list(map(lambda x: pr[x] ** (self.neigboards - i) * (1 - pr[x]) ** i * M * pr[x], pr))
                    prob.append(sum(pro))  # todo возможно потребуется сохранять отдельные доли
                self.tProb[rule] = prob
                self.tQ[rule] = 2 * reduce(lambda res, x: res * x, pr.values(), 1) / sum(pr.values()) ** 2

    def reset(self):
        for ruleResult in self.insertionResult:
            for atom in ruleResult:
                atom.reset()

    def iteration(self):
        start = time()
        self.insertionResult = []
        for i in self.insertionRules:
            self.insertionResult.append(self.supercell.insertAtoms(self.random, i))
        res = self.supercell.getDisttribution(self.insertionRules)
        iterDistribution = res[0]
        iterQ = res[1]
        iterXI2 = {}
        iterQdiff = {}
        for i in iterDistribution:
            s = listDiff(iterDistribution[i], self.tProb[i])
            iterXI2[i] = sum(s)
            iterQdiff[i] = iterQ[i] - self.tQ[i]
        iterTime = time() - start
        self.time += iterTime
        return iterationResult(iterDistribution, iterXI2, iterQ, iterQdiff, iterTime, self.local)

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
    i = inData("exampleinput.txt", localisation())
    print(i)