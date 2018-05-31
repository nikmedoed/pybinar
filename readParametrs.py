import os
from localisation import localisation
from rand import rand
import time
import os

from cells import cell, supercell

class inData(object):
    """paramets reader"""

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
        # ToDo проверять, что файл существует

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

        # Todo Как лучше сохранить оставшиеся условия, чтобы потом было просто юзать

        const = self.rawparam['Сonstraints']
        self.timeLimit = int(const[0]) if not (":" in const[0]) else time.strptime(const[0], "%H:%M:%S")
#Todo нормально скушать время с часам больше 23



if __name__ == "__main__":

    # t = time.strptime("00:20:12", "%X") # это для экспериментов со временем
    i = inData("exampleinput.txt", localisation())
    print(i.rawparam)

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