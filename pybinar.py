import sys
# import readParametrs
from localisation import localisation
import os

if __name__ == "__main__":
    """   
    in lang - code of languadge
    in outputfold - subpath for result folder
    in input - subpath to datafile
        
    """
    try:
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
            outputfold = input + " - results"

        texts = localisation(lang) # object with all text
        loc = texts.loc(__file__) # text for this file

        print(loc["ParamIn"] + ": \x1b[36m"+input+"\x1b[0m")
        print(loc["ResOut"] + ": \x1b[36m"+outputfold+"\x1b[0m")
        print()

    # todo чтение параметров
    # todo размножение ячейки
    # todo рассчёт вероятности
    # todo рассчёт хи^2
    # todo вбросы атомов
    # todo график хи^2
    # todo логика эксперимента исходя их входных условий
    # todo вывод данных

    except:
        print("\x1b[35mERROR!!! Program terminated\x1b[0m")



