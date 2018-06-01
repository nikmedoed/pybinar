import os
from localisation import localisation

class cell(object):
    def __init__(self, name="", local = localisation()):
        loc = local.loc(__file__) # text for this file
        self.name = name

        #ToDo сделать считыватель ячейки из файла
        pass

    def __str__(self):
        r= "input:\t" + self.name[0]
        return r

class supercell(object):
    def __init__(self, cell, xyz, local = localisation()):
        loc = local.loc(__file__) # text for this file
        self.cell = cell
        self.xyz = xyz


        # ToDo сделать размножитель ячейки
        pass

    def __str__(self):
        r = "cell:\t" + str(self.cell) + "\nxyz:\t" + str(self.xyz)
        return r
