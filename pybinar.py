import sys
# import readParametrs
from localisation import localisation
import os

if __name__ == "__main__":
    try:
        input = "exampleinput.txt"
        outputfold = ""
        lang = ""
        for param in sys.argv[1:3]:
            if param[0] == "#":
                lang = param[1:]
            elif param[0] == "/":
                outputfold = param[1:]
            else:
                input = param
        if outputfold == "":
            outputfold = input + " - results"

        texts = localisation(lang).text
        me = os.path.basename(__file__).replace(".py", "")
        loc = texts[me]

        print(loc["ParamIn"] + ": \x1b[36m"+input+"\x1b[0m")
        print(loc["ResOut"] + ": \x1b[36m"+outputfold+"\x1b[0m")
        print()



    except:
        print("\x1b[35mERROR!!! Program terminated\x1b[0m")


