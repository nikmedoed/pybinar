from time import time
import re

class Profiler(object):
    def __enter__(self):
        self._startTime = time()

    def __exit__(self, type, value, traceback):
        print ("Elapsed time: {:.3f} sec".format(time() - self._startTime))

def numericListFromDic(s, n, c = 31):
    s[n] += 1
    return "\x1b[%dm% 4s\x1b[%dm" % (c, s[n], 0)

def deletecolors(s):
    s = re.sub("\x1b\[\d*m", "", s)
    return s

def colorize(f, *args):
    """
    :param f: строка со вставками '@' который обозначает зоны окраски
    :param args: коды стилизации
    :return: возвращает строку со вставками стилизации
    """
    c = 0
    r = ""
    fl = False
    for i in f:
        if i == "@":
            if fl :
                fl = False
                i = "\x1b[0m"
            else:
                i = "\x1b["+ str(args[c]) +"m"
                c += 1
                fl = True
        r += i
    return r

if __name__ == "__main__":
    pass
    # with Profiler() as p:
    #     for i in range(100000000):
    #         t = "\x1b[32m% 4s\x1b[0m" % "KOKO"
    #
    # with Profiler() as p:
    #     for i in range(100000000):
    #         t= "\x1b[%dm% 4s\x1b[%dm" % (32, "KOKO", 0)
