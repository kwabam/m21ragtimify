import music21 as m21
import json
import os
import random

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

from melody_extract import skyline
from BassGenerator import *
from _V1Gen import *


def graph_dict_list(dict_list):
    x = []
    y = []
    for d in dict_list:
        for key, item in d.items():
            x.append(key)
            y.append(item)

    print(x)
    print(y)

    z = [c for _, c in sorted(zip(y, x))]
    y = sorted(y)

    print(z)
    print(y)

    x = z[-20:]
    y = y[-20:]

    y.reverse()
    x.reverse()

    height = y
    bars = x
    y_pos = np.arange(len(bars))

    # Create horizontal bars
    plt.barh(y_pos, height)

    # Create names on the y-axis
    plt.yticks(y_pos, bars)

    # Show graphic
    plt.savefig("v1_onset_data.png", bbox_inches='tight')
    plt.show()

def graph_freq(data, name):
    c = 0
    a = []
    for dict in data:
        for key,value in dict.items():
            c += value
        a.append(c)
        c = 0
    print(a)

    objects = []
    for i in range(17):
        objects.append(i)
    y_pos = np.arange(len(objects))
    performance = a

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Freq')
    plt.title(name + " Onset Frequency")

    plt.savefig(name + '_freq.png')

def main():
    v1_data = json.load(open("v1Database.json"))
    endings_data = json.load(open("v3Database.json"))
    endings_1 = []
    endings_2 = []
    for i in range(17):
        endings_1.append({})
        endings_2.append({})
    for dict in endings_data:
        for key, value in dict.items():
            penult_measure = key[:16]
            ult_measure = key[16:]
            pen_count = count_onsets(penult_measure)
            ult_count = count_onsets(ult_measure)
            try:
                endings_1[pen_count][penult_measure] += 1
            except:
                endings_1[pen_count][penult_measure] = 1
            try:
                endings_2[ult_count][ult_measure] += 1
            except:
                endings_2[ult_count][ult_measure] = 1

    graph_freq(v1_data, 'V1 Database')
    #graph_dict_list(endings_1)
    #graph_dict_list(endings_2)
    return 0


if __name__ == '__main__':
    main()