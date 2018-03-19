import os
me = os.path.basename(__file__).replace(".py", "")
from localisation import localisation


class rand(object):
    def __init__(self, name="", local = localisation()):
        loc = localisation().text[me]
        self.rawparam = {}
        #ToDo сделать считыватель ячейки из файла
        pass