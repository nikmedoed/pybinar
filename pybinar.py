import sys
# import readParametrs
from localisation import localisation
import os
from readParametrs import inData
from functools import reduce
from time import strftime, gmtime, sleep

from addons import *
# class pybinar(object):
#     def __init__(self, time, local = localisation()):



if __name__ == "__main__":
    """   
    in lang - code of languadge
    in outputfold - subpath for result folder
    in input - subpath to datafile
        
    """
    # try:


    input = "exampleinput.txt"
    outputfold = ""
    lang = ""
    for param in sys.argv[1:3]:
        if param[0] == "#":
            lang = param[1:]
        elif param[0] == "/":
            outputfold = param[1:]
            # todo возможность указания полной директории для результатов
        else:
            input = param
            # todo файл с параметрами тоже брать откуда угодно, а не только из подпапки
    if outputfold == "":
        outputfold = input.split(".")[0] + " - results"

    texts = localisation(lang) # object with all text
    loc = texts.loc(__file__) # text for this file

    print(loc["ParamIn"] + ": \x1b[36m"+input+"\x1b[0m")
    print(loc["ResOut"] + ": \x1b[36m"+outputfold+"\x1b[0m")
    print()

    try:
        os.stat(outputfold)
    except:
        os.mkdir(outputfold)

    outputfile = outputfold + "/00 - result.txt"

    data = inData(input, texts)
    start = time()

    sleep(2)
    # todo рассчёт вероятности
    # todo рассчёт хи^2
    # todo вбросы атомов
    # todo график хи^2
    # todo логика эксперимента исходя из входных условий

    end = time()

    # todo вывод данных

    with open(outputfile, "w", encoding="utf-8") as out:
        out.write("\n".join(
            list(map(lambda x: "  %-20s = %-10s" % (loc[x[0]], x[1]),
                     [
                         ["StartTime", strftime("%Y.%m.%d  %H:%M:%S", gmtime(start))],
                         ["EndTime", strftime("%Y.%m.%d  %H:%M:%S", gmtime(end))],
                         ["TimeLimit", coolTime(data.timeLimit)],
                         ["TotalSpend", coolTime(round(end - start, 4))]
                     ]))
        ))
        inputatomsnumeric = data.cell.printatomsNumeric()
        if data.pprint.input:
            out.write("\n\n\n" + loc["InputCell"] + ":\n\n")
            out.write(deletecolors(inputatomsnumeric))

        out.write("\n\n\n%s: %s\n" % (loc["Trans"], data.supercell.xyz))
        out.write("%-45s %s\n" % (loc["CellPar1"], data.cell.cell_abc))
        out.write("%-45s %s\n" % (loc["CellPar2"], data.cell.cell_ang))

        # Смесь атомов(без аниона) = Fe   +    Si
        # Теоретическая вероятность для каждого атома:
        # P(Fe)=   0.101562
        # P(Si)=   0.898438
        # Сумма вероятностей =   1.000000

        if data.pprint.replication:
            m = reduce(lambda x, y: x*y, data.supercell.xyz)
            # out.write("\n\n\n\n\x1b[35m%s\x1b[0m: %d\t\x1b[35m%s\x1b[0m: %s"
            out.write("\n%s: %d\n%s:\n %s"
                      % (loc["MulCof"],
                         data.supercell.Cmul,
                        loc["MulRes"],
                         " ".join(list(map(
                             lambda a: "%s: %s" %
                                       (
                                 str(a[0]),
                                 str(a[1])
                                       ),
                             data.supercell.atomcount
                        ))
                         )))
            out.write("\n\n" + loc["SuperCell"] + "\n\n")
            #
            out.write(deletecolors(data.supercell.printatomsNumeric()))


    # except:
    #     msg = ""
    #     try:
    #         msg = texts.error
    #         txt = loc["Msg"]
    #     except:
    #         msg = ""
    #         txt = "Msg"
    #     print("\x1b[35mERROR!!! Program terminated\x1b[0m\n\x1b[31m%s\x1b[0m: %s" % (txt, msg))



