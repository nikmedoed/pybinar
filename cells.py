import os
me = os.path.basename(__file__).replace(".py", "")
from localisation import localisation

# ToDo Локализация не всегда может быть для файла. сейчас нам будут генерить ошибки. Нужно что-то более сэйф

class cell(object):
    def __init__(self, name="", local = localisation()):
        loc = localisation().text[me]
        self.rawparam = {}
        #ToDo сделать считыватель ячейки из файла
        pass

class supercell(object):
    def __init__(self, cell, xyz, local = localisation()):
        loc = localisation().text[me]
        self.rawparam = {}
        # ToDo сделать размножитель ячейки
        pass
