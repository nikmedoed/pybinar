import random
from src import localisation

import os
import matplotlib.pyplot as plt
import numpy as np
import time

def save(name,  fold = '', fmt='png'):
    pwd = os.getcwd()
    if fold != "":
        if not os.path.exists(fold):
            os.mkdir(fold)
        os.chdir(fold)
    plt.savefig('{}.{}'.format(name, fmt), fmt='png')
    if os.getcwd() != pwd:
        os.chdir(pwd)

def plot(c, d, name = "", fold = '', local = localisation.localisation()):
    loc = local.loc(__file__)
    index = np.arange(13)
    bar_width = 0.35
    opacity = 0.8

    plt.grid(True, linestyle=':', fillstyle='bottom', axis='y')
    rects1 = plt.bar(index- bar_width/2, d.values(), bar_width,
                     alpha=opacity,
                     color='tab:purple',
                     label=loc['Bar1'])

    rects2 = plt.bar(index + bar_width/2, c.values(), bar_width,
                     alpha=opacity,
                     color='orange',
                     label=loc['Bar2'])

    plt.xlabel(loc['XLabel'])
    plt.ylabel(loc['YLabel'])
    plt.title(loc['Name'])
    plt.xticks(index, d.keys())
    plt.legend()

    plt.tight_layout()

    # save(name='pic_1_4_1', fmt='pdf')
    save(name=(time.strftime("%Y-%m-%d_%H-%M-%S") if name =="" else name), fold=fold, fmt='png')
    plt.show()


if __name__ == "__main__":
    local = localisation.localisation()
    d = dict.fromkeys(range(13))
    c = dict.fromkeys(range(13))
    for i in d:
        d[i] = random.random()
        c[i] = d[i] + random.random()*0.05-0.02

    plot(c, d, fold="rfolder", local=local)
