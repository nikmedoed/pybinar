from localisation import localisation
from rand import rand
import time
import os
import json

from cells import cell, supercell
from atom import element

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
        self.loc = local.loc(__file__) # text for this file
        self.rawparam = {}
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
        for k in conditions[3:]:
            i = k.replace(">", " ").replace("(", " ").replace(")", " ").split()
            i[2] = float(i[2])
            i[3] = int(i[3])
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

        self.atomsForChange = set(element(x[0]) for x in self.insertionRules).union(element(x[1]) for x in self.insertionRules)
        self.neigboards = self.supercell.addNeighbours(self.sphere1, self.atomsForChange)

        outp = self.rawparam["Output"]
        tmp = outp[0].split()
        self.x2fround_l = float(tmp[0])
        self.x2fround_r = float(tmp[1]) if len(tmp) > 1 else 0 if self.x2toLess else 100
        if self.x2fround_l > self.x2fround_r:
            self.x2fround_l = self.x2fround_r
            self.x2fround_r = float(tmp[0])

        self.Ntoprint = int(outp[1])
        self.pprint = printparam(outp[2:], local)

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


if __name__ == "__main__":
    i = inData("exampleinput.txt", localisation())
    print(i)