# Copyright 2018 Nikita Muromtsev (nikmedoed)
# Licensed under the Apache License, Version 2.0 (the «License»)

from time import time, strftime, gmtime
import re
from copy import deepcopy as dc

def getQ(distrib, pairs):
    return sum(list(map(lambda x: x*distrib.index(x), distrib))) / pairs

def getDistrib(nc, interestedAtoms, it =- 1):
    distrib = [0] * nc
    for iAtom in interestedAtoms:
        count = 0
        iAtomelem = iAtom.getelement(it)
        for i in iAtom.interestedNeighbours:
            if i.getelement(it) != iAtomelem:
                count += 1
        distrib[count] += 1
    size = len(interestedAtoms) + 1
    return list(map(lambda x: x/size, distrib))

def coolTime(s):
    r = ""
    h = s//3600
    s %= 3600
    m = s // 60
    s %= 60
    ms = s * 1000
    s //= 1
    ms %= 1000
    ms = round(ms)
    if h: r+="%4d h. " % h
    if m: r+="%3d min. " % m
    if s: r+="%3d sec. " % s
    if ms: r += "%4.0f ms." % ms
    return r

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
    start = time()

    end = time()

    print("\n".join(
        list(map(lambda x: "  %-20s = %10s" % ("кек", strftime("%d days %Hh. %Mm. %Ss.", gmtime(x[1]))),

                 [
                     ["StartTime", start],
                     ["TimeLimit", 0],
                     ["EndTime", end],
                     ["TotalSpend", end - start]
                 ]))
    ))