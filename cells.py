import os
from localisation import localisation

class cell(object):
    def __init__(self, name="", local = localisation()):
        loc = local.loc(__file__) # text for this file

        #ToDo сделать считыватель ячейки из файла
        pass

class supercell(object):
    def __init__(self, cell, xyz, local = localisation()):
        loc = local.loc(__file__) # text for this file

        # ToDo сделать размножитель ячейки
        pass
