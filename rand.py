import os
from localisation import localisation


class rand(object):
    def __init__(self, generator, randomp, local = localisation()):
        loc = local.loc(__file__) # text for this file
        self.generator =  generator
        self.randomp = randomp
        #ToDo сделать класс рандомизации


        pass

    def __str__(self):
        return "generator:\t" + str(
            "stand" if self.generator == 0 else "our" if self.generator == 1 else "special"
        ) + "\nrandomp:\t" + str(self.randomp)