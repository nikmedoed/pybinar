import os
from localisation import localisation
from atom import atom


class cell(object):
    def __init__(self, name="", local = localisation()):
        self.loc = local.loc(__file__) # text for this file
        self.file = name
        self.filemain = ""
        self.cell_abc = []
        self.cell_ang = []
        self.atoms = []
        main = True
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
                    self.atoms.append(atom(s[0], s[1], s[2], s[3], local))

    def getatoms(self):
        r = ""
        r += "\n"+"\n".join(list(map(str, self.atoms)))
        return r

    def __str__(self):
        r = "\n".join(
            map(lambda a, b: "\x1b[36m" + a + ":\x1b[0m\t" + str(b),
            [
                "file",
                "cell_abc",
                "cell_ang",
                "atoms"
            ],
            [
                self.file,
                self.cell_abc,
                self.cell_ang,
                self.getatoms()

            ]
        ))
        return r

class supercell(object):
    def __init__(self, cell, xyz, local = localisation()):
        self.loc = local.loc(__file__) # text for this file
        self.cell = cell
        self.xyz = xyz
        self.atoms = [] # список атомов, в каждом указана связанная с ним ячейка
        self.cells = [] # позиции ячеек
        cellnum = 0
        for x in range(self.xyz[0]):
            for y in range(self.xyz[1]):
                for z in range(self.xyz[2]):
                    temp = []
                    for i in cell.atoms:
                        temp.append((i + [x, y, z]).setcell(cellnum))
                    self.atoms.extend(temp)
                    cellnum += 1
                    self.cells.append([x, y, z])



        # ToDo сделать размножитель ячейки
        pass

    def __str__(self):
        r = ""
        # r += "\x1b[36mcell:\x1b[0m\n" + str(self.cell) +
        r += "\nxyz:\t" + str(self.xyz)

        return r


if __name__ == "__main__":
    local = localisation()
    c = cell("Fe4Si4O12_P1.cif", local)
    s = supercell(c, [2, 2, 2], local)
    print(
        "\n".join([
            "\x1b[32mCell\x1b[0m",
            str(c),
            "\n\x1b[32mSupercell\x1b[0m",
            str(s)
        ])
    )
