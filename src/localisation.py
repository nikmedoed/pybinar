# Copyright 2018 Nikita Muromtsev (nikmedoed)
# Licensed under the Apache License, Version 2.0 (the «License»)

from pathlib import Path
import os
me = os.path.basename(__file__).replace(".py", "")
locpath = os.path.dirname(os.path.abspath(__file__)) + "/Local/"
delaultloc = "ru"

class localisationClass(object):

    def __init__(self, loc="", path=""):
        # print("locinit")
        self.loadLoc()

    def loadLoc(self, loc="", path=""):
        self.error = "?"
        local = locpath if path == "" else path
        if loc not in os.listdir(local):
            loc = delaultloc
        self.lang = loc
        f = open(local + loc, "r", encoding="utf-8")
        if not hasattr(self, 'text'): self.text = dict()
        now = ""
        # ToDo генератор локализаций по экселю
        try:
            for i in f:
                i = i.strip()
                if i != "":
                    # print(i[0:1])
                    if (i[0:2] == "--") or (i[0:2] == "=="):
                        now = i[2:]
                        if 'now' not in self.text: self.text[now] = dict()
                    else:
                        i = i.split("=")
                        # print(i[1].strip(),i[0].strip())
                        self.text[now][i[0].strip()] = i[1].strip()
        except:
            print("\x1b[31mFATAL ERROR\x1b[0m: localistion isn't loaded")
            raise Exception

    def setLoc(self, loc="", path=""):
        if loc == "":
            loc = delaultloc
        if loc != self.loc:
            self.loadLoc(loc, path)
        return self

    def seterr(self, t):
        self.error = t
        raise Exception()

    def loc(self, mod):
        me = os.path.basename(mod).replace(".py", "")
        return self.text[me] if me in self.text.keys() else []

localisation = localisationClass()

if __name__ == "__main__":
    print(localisation.loc(__file__))