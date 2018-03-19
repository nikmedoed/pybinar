import os
me = os.path.basename(__file__).replace(".py", "")
from localisation import localisation


class cell(object):
    def __init__(self, name="", local = localisation()):
        loc = localisation().text[me]

        #ToDo сделать считыватель ячейки из файла
        pass

class supercell(object):
    def __init__(self, cell, xyz, local = localisation()):
        loc = localisation().text[me]

        # ToDo сделать размножитель ячейки
        pass
