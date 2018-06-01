import os
from localisation import localisation

class atom(object):
    def __init__(self, name, randomp, local = localisation()):
        self.name = name
        #
        # loc = local.loc(__file__) # text for this file
        # self.generator = generator
        # self.randomp = randomp
        #ToDo сделать класс атома



        pass

    # def __str__(self):
    #     return "generator:\t" + str(self.generator) + "\nrandomp:\t" + str(self.randomp)