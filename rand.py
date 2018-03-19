import os
me = os.path.basename(__file__).replace(".py", "")
from localisation import localisation


class rand(object):
    def __init__(self, generator, ranomp, local = localisation()):
        loc = localisation().text[me]

        #ToDo сделать класс рандомизации


        pass