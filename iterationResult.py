from src.localisation import localisation
import os
from src.addons import *

def genFileName(name):
    try:
        genFileName.a += 1
    except AttributeError:
        genFileName.a = 0
    return '/{:0>2} - {}.txt'.format(genFileName.a, name)

def getIndex():
    try:
        getIndex.a += 1
    except AttributeError:
        getIndex.a = 1
    return getIndex.a

class iterationResult(object):
    """
    """

    def __init__(self, dist, XI2, Q, Qdiff, time, local=localisation()):
        self.loc = local.loc(__file__)  # text for this file
        self.dist = dist
        self.xi2 = XI2
        self.Q = Q
        self.Qdiff = Qdiff
        self.time = time
        self.index = getIndex()


    def setloc(self, loc):
        self.loc = loc.loc(__file__)

    def __repr__(self):
        return "iteration result class"

    def makefiles(self, data, outputfold):
        print(self.loc['printIteration'], self.index)
        if not os.path.exists(outputfold):
            os.mkdir(outputfold)
        for i in self.dist:
            filename = 'iteration '
            if i == -1:
                filename += 'all rules'
            else:
                filename += 'rule {}'.format(i+1)

            with open(outputfold+genFileName(filename), "w", encoding="utf-8") as out:
                pr = out.write
                pr("%+28s = % d\n" % (self.loc['IterationNum'], self.index))
                pr("".join(list(map(lambda x: "%+28s = % .4f\n" % x, [
                    (self.loc['Time'], self.time),
                    ('χ²', self.xi2[i]),
                    ('Q', self.Q[i]),
                    ('Q - Q ' + self.loc['theoretical'], self.Qdiff[i])]))))
                pr("\n")
                pr(self.loc['Propab']+'\n')
                pr("{0[0]:^4} {0[1]:^10} {0[2]:^10} {0[3]:^10}\n".format(list(map(lambda x: self.loc[x], ['Pairs', 'Iteration', 'Theoretical', 'Difference']))))
                pr("%s\n" % "\n".join(list(map(lambda x: "{:>3}  {:< 10.4}  {:< 10.4}  {:< 10.4}".format(x[0], x[1], x[2], x[1] - x[2]),
                                               zip(range(len(self.dist[i])), self.dist[i], data.tProb[i])))))
                pr("\n\n" + self.loc["SuperCell"] + "\n\n")
                pr(deletecolors(data.supercell.printatomsRulesNumeric(i)))

#todo supedcell печатать атомы с учетом правил
#todo соседи интересных атомов





    # def __str__(self):
    #     t = "\n".join([
    #         "\n\x1b[32mrawparam\x1b[0m",
    #         self.rawparam.__str__().replace("'], '", "'], \n'").replace("': ['", "':\t['"),
    #         "\n\x1b[32mcell\x1b[0m",
    #         str(self.cell),
    #         "\n\x1b[32msupercell\x1b[0m",
    #         str(self.supercell),
    #         "\n\x1b[32mrandom\x1b[0m",
    #         str(self.random),
    #         "\n\x1b[32mtimeLimit\x1b[0m",
    #         str(self.timeLimit),
    #         "\n\x1b[32mRules\x1b[0m",
    #         str(self.insertionRules),
    #         "\n\x1b[32mParam\x1b[0m",
    #         # "sphere2:\t" + str(self.sphere2),
    #         "sphere1:\t" + str(self.sphere1),
    #         "x2toLess:\t" + str(self.x2toLess),
    #         "x2stop:\t" + str(self.x2stop),
    #         "\n\x1b[32mOutparam\x1b[0m",
    #         "x_left_out:\t" + str(self.x2fround_l),
    #         "x_right_out:\t" + str(self.x2fround_r),
    #         "NtoPrint:\t" + str(self.Ntoprint),
    #         "\nPrintParam:\n" + str(self.pprint)
    #     ])
    #     return t


if __name__ == "__main__":
    pass