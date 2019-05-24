import os
me = os.path.basename(__file__).replace(".py", "")

delaultloc = "ru"

class localisation(object):

    def __init__(self, loc = ""):
        self.error = "?"
        if loc == "":
            loc = delaultloc
        f = open("src/Local/"+loc, "r", encoding="utf-8")
        self.text = dict()
        now = ""
        # ToDo проверять список доступных локализаций и переключать на стандартную
        # ToDo генератор локализаций по экселю
        try:
            for i in f:
                i = i.strip()
                if i != "":
                    # print(i[0:1])
                    if (i[0:2] == "--") or (i[0:2] == "=="):
                        now = i[2:]
                        self.text[now] = dict()
                    else:
                        i = i.split("=")
                        # print(i[1].strip(),i[0].strip())
                        self.text[now][i[0].strip()] = i[1].strip()
        except:
            print("\x1b[31mFATAL ERROR\x1b[0m: localistion isn't loaded")
            raise Exception


    def seterr(self, t):
        self.error = t
        raise Exception()


    def loc(self, mod):
        me = os.path.basename(mod).replace(".py", "")
        return self.text[me] if me in self.text.keys() else []


if __name__ == "__main__":
    a = localisation()
    print(a.text)