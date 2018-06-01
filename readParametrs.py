from localisation import localisation
from rand import rand
import time
import os
import json

from cells import cell, supercell

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

    def __init__(self, infile="", local = localisation()):
        loc = local.loc(__file__) # text for this file
        self.rawparam = {}
        block = ""
        if infile == "":
            print(loc['InError'])
            raise Exception
        if not os.path.exists(infile):
            print(loc['InFileFalse'])
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

        self.cell = cell(self.rawparam['Name'], local)
        conditions = self.rawparam['Сonditions']
        self.supercell = supercell(cell, list(map(int,(conditions[0]).split())), local)
        self.random = rand(int(conditions[1]), conditions[2], local)
        self.insertionRules = []
        for k in conditions[3:]:
            i = k.replace(">", " ").split()
            i[2] = int(i[2])
            self.insertionRules.append(i)

        const = self.rawparam['Сonstraints']
        self.timeLimit = int(const[0])*60 if not (":" in const[0]) else \
            sum(map(lambda x, y: int(x)*y, const[0].split(":"), [360, 60, 1]))

        self.sphere2 = float(const[1])
        self.sphere1 = float(const[2])
        self.x2toLess =  "0" == const[3]
        self.x2stop = float(const[4])


        #Todo параметры остановки эксперимента

        #Todo параметры вывода

    def __repr__(self):
        return "inData class"

    def __str__(self):
        t = "\n".join([
            "\nrawparam",
            self.rawparam.__str__().replace("'], '", "'], \n'").replace("': ['", "':\t['"),
            "\ncell",
            str(self.cell),
            "\nsupercell",
            str(self.supercell),
            "\nrandom",
            str(self.random),
            "\ntimeLimit",
            str(self.timeLimit),
            "\nRules",
            str(self.insertionRules),
            "\nParam",
            "sphere2:\t" + str(self.sphere2),
            "sphere1:\t" + str(self.sphere1),
            "x2toLess:\t" + str(self.x2toLess),
            "x2stop:\t" + str(self.x2stop),

        ])

        return t



if __name__ == "__main__":
    i = inData("exampleinput.txt", localisation())
    print(i)

    # t = time("30:20:12") # это для экспериментов со временем %H:%M:%S

    # print (t)

# if block == "Name":
#     pass
# elif block == "Сonditions":
#     pass
# elif block == "Сonstraints":
#     pass
# elif block == "Output":
#     pass
# else:
#     print(loc["Unexpected"])