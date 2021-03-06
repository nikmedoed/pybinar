# Copyright 2018 Nikita Muromtsev (nikmedoed)
# Licensed under the Apache License, Version 2.0 (the «License»)

import sys
from src.localisation import localisation
import os
from src.parametrs import inData
from collections import defaultdict
from src.utils.addons import *
from tqdm import tqdm

# class pybinar(object):
#     def __init__(self, time):


def checkRules(atomsCount, rules, errMes):
    c = defaultdict(lambda: 0)
    for i in rules:
        c[i[0]]+=i[3]
    for i in c:
        if atomsCount[i] < c[i]:
            print(errMes % (i, atomsCount[i]))
            return False
    return True



if __name__ == "__main__":
    """   
    in lang - code of languadge
    in outputfold - subpath for result folder
    in input - subpath to datafile
        
    """
    # try:
    input = "z_exampleinput.txt"
    outputfold = ""
    lang = ""
    for param in sys.argv[1:3]:
        if param[0] == "#":
            lang = param[1:]
        elif param[0] == "/":
            # "\\" in param or "/" in param
            outputfold = param[1:]
            # todo возможность указания полной директории для результатов
        else:
            input = param
            # todo файл с параметрами тоже брать откуда угодно, а не только из подпапки
    if outputfold == "":
        outputfold = input.split(".")[0] + " - results"

    if not os.path.exists(outputfold):
        os.mkdir(outputfold)

    localisation.setLoc(lang) # object with all text
    loc = localisation.loc(__file__) # text for this file

    print(loc["ParamIn"] + ": \x1b[36m"+input+"\x1b[0m")
    print(loc["ResOut"] + ": \x1b[36m"+outputfold+"\x1b[0m")
    print()

    # ======== read and prepare Data
    data = inData(input)
    os.chdir(outputfold)
    data.random.settime()
    outputfile = "00 - result.txt"

    # ======== Iterations

    start = time()

    # while data.time<data.timeLimit:
    #     data.iteration()


    if checkRules(data.supercell.atomcountdict, data.insertionRules, loc["RuleSizeError"]):
        x2stop = False
        iteration = 0
        timeProgress = tqdm(total=data.timeLimit, bar_format="{l_bar} {bar} | {n_fmt:.4}/{total_fmt}s [{rate_fmt}{postfix}] {elapsed}")
        #                     postfix=["Batch", dict(value=0)])

        while data.time < data.timeLimit and not x2stop:
            iteration += 1
            res = data.iteration()
            if iteration % data.Ntoprint == 0:
                res.makefiles(data, 'iteration - {:0>5}'.format(iteration))
            data.reset()
            x2stop = res.xi2[-1] <= data.x2stop if data.x2toLess else res.xi2[-1] >= data.x2stop
            if data.time > data.timeLimit:
                timeProgress.close()
            else:
                timeProgress.update(res.time)

        timeProgress.close()
        if x2stop:
            print(loc["StopByXi"], res.xi2[-1])
            res.makefiles(data, 'iteration - {:0>5}'.format(iteration))
        else:
            print(loc["StopByTime"], coolTime(data.time))

    # todo вывод данных итерации, в том числе в файлы галп, циф, диаграмма

    # todo цикл с ограничением по времени и срабатыванию на улучшения

    # todo выводи итога в зависимости от параметров

    # todo подробная диагностическая информация

    # todo аналитика, ошибки

    # todo оптимизировать рассчёт/распараллелить


    end = time()

    # graph.plot(c, d, name="как", fold="rfolder") как будет чем, дописать


    with open(outputfile, "w", encoding="utf-8") as out:
        pr = out.write
        pr("\n".join(
            list(map(lambda x: "  %-20s = %-10s" % (loc[x[0]], x[1]),
                     [
                         ["StartTime", strftime("%Y.%m.%d  %H:%M:%S", gmtime(start))],
                         ["EndTime", strftime("%Y.%m.%d  %H:%M:%S", gmtime(end))],
                         ["TimeLimit", coolTime(data.timeLimit)],
                         ["TotalSpend", coolTime(round(data.time, 4))]
                     ]))
        ))
        pr("\n")


        # Исходные данные
        pr("\n\n\n")
        pr("%s\n\n" % loc["BlockStart"].center(75, "-"))

        pr("%s: %s\n\n" % (loc["InputFile"], data.cell.file))

        pr("%-45s %s\n" % (loc["CellPar1"], data.cell.cell_abc))
        pr("%-45s %s\n\n" % (loc["CellPar2"], data.cell.cell_ang))

        pr("%s:\n %s\n" % (loc["BeforeRes"],
                           " ".join(list(map(lambda a: "%s: %s" % (str(a[0]), str(a[1])), data.cell.atomcount
                         )))))
        if data.pprint.input:
            pr("\n\n" + loc["InputCell"] + ":\n\n")
            pr(deletecolors(data.cell.printatomsNumeric())+"\n")


        # Предобработанные данные
        pr("\n\n\n")
        pr("%s\n\n" % loc["BlockMul"].center(75, "-"))

        pr("%s: %s\n" % (loc["Trans"], data.supercell.xyz))

        # Смесь атомов(без аниона) = Fe   +    Si
        # Теоретическая вероятность для каждого атома:
        # P(Fe)=   0.101562
        # P(Si)=   0.898438
        # Сумма вероятностей =   1.000000
        pr("\n%s: %d\n%s:\n %s\n"% (loc["MulCof"],
                                    data.supercell.Cmul,
                                    loc["MulRes"],
                                    " ".join(list(map(lambda a: "%s: %s" %(str(a[0]), str(a[1])),
                                                                          data.supercell.atomcount))
                                 )))
        if data.pprint.replication:
            out.write("\n\n" + loc["SuperCell"] + "\n\n")
            out.write(deletecolors(data.supercell.printatomsNumeric()))

        # Результаты смешения общие
        pr("\n\n\n")
        pr("%s\n\n" % loc["BlockGen"].center(75, "-"))

        pr("%s:\t%s\n" % (loc["Generator"], data.random.generator))
        pr("%s:\t%s\n" % (loc["GeneratorP"], data.random.randomp))
        pr("\n")
        pr("%s:\n" % (loc["Rules"]))
        pr("%s\n" % "\n".join(list(map(lambda x: " +%2d: %6s > %-6s(q = %.2f) %d" % tuple([x[4]+1, *x[:4]]), data.insertionRules))))
        pr("\n")
        pr("%15s - %s\n" % (data.sphere1, loc["Sphere1"]))
        # pr("%15s - %s\n" % (data.sphere2, loc["Sphere2"]))
        pr("%15s - %s\n" % (loc["ToLess"] if data.x2toLess else loc["ToMore"], loc["Direct"]))
        pr("%15s - %s\n" % (data.x2stop, loc["Ground"]))

        # Результаты смешения подробные
        pr("\n\n\n")
        pr("%s\n\n" % loc["BlockRes"].center(75, "-"))
        pr("%15s - %s\n" % ([data.x2fround_l, data.x2fround_r], loc["PrintGround"],))
        pr("%15s - %s\n" % (data.Ntoprint, loc["PrintIterator"]))


    # todo вывод основных данных

    # except:
    #     msg = ""
    #     try:
    #         msg = texts.error
    #         txt = loc["Msg"]
    #     except:
    #         msg = ""
    #         txt = "Msg"
    #     print("\x1b[35mERROR!!! Program terminated\x1b[0m\n\x1b[31m%s\x1b[0m: %s" % (txt, msg))



