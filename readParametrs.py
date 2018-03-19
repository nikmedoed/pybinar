import os
me = os.path.basename(__file__).replace(".py", "")
from localisation import localisation
from rand import rand

from cells import cell, supercell

class inData(object):
    """paramets reader"""

    def __init__(self, infile="", local = localisation()):
        loc = localisation().text[me]
        self.rawparam = {}
        block = ""
        if infile == "":
            print(loc['InError'])
            raise Exception
        # ToDo проверять, что файл существует

        f = open(infile, "r", encoding="utf-8")
        for i in f:
            i = i.split("//")[0].strip()
            # print("n", i, "n")
            if len(i) > 0:
                # print(len(i))
                if i[len(i)-1] == ":":
                    block = i[:len(i)]
                    self.rawparam[block] = []
                else:
                    self.rawparam[block].append(i)

        self.cell = cell(self.rawparam['Name'], local)
        conditions = self.rawparam['Сonditions']
        self.supercell = supercell(cell, list(map(int,(conditions[0]).split())), local)
        self.random = rand(int(conditions[1]),conditions[2])

        # Todo Как лучше сохранить оставшиесч условия, чтобы потом было просто юзать




if __name__ == "__main__":
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