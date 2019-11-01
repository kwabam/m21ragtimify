import music21 as m21
import json
import os
import random

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

from melody_extract import skyline
from BassGenerator import *


def count_onsets(measure_str):
    count = 0
    for char in measure_str:
        if char == 'I' or char == '1':
            count += 1
    return count


def select_ragtime_measure(dct):
    rand_val = random.random()
    total = 0
    for key, value in dct.items():
        total += value
        if rand_val <= total:
            return key


def create_onset_str(measure):
    measure_list = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
    for item in measure:
        if isinstance(item, m21.note.Note) or isinstance(item, m21.chord.Chord):
            measure_list[int(item.offset * 4)] = "1"
    return "".join(measure_list)


# takes an onset string and returns an array listing what beat (by 16th note division) the onsets occur on
def find_onset_int_arr(onset_str):
    i = 0
    arr = []
    for char in onset_str:
        if char == "I" or char == "1":
            arr.append(i)
        i += 1
    return arr


def find_largest_onset_gap(m1, m2):
    m1 = find_onset_int_arr(m1)
    m2 = find_onset_int_arr(m2)
    if len(m1) != len(m2):
        return "error, measures should have same number of onsets"
    high = 0
    for i in range(len(m1)):
        gap = abs(m1[i] - m2[i])
        if gap > high:
            high = gap
    return high

def get_quarter_length(measure, num):
    a = find_onset_int_arr(measure)
    if num == count_onsets(measure)-1:
        return (16 - a[num])/4
    return (a[num+1]-a[num])/4



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


def main():
    v1_pattern_data = json.load(open("v1Database.json"))

    # graph_dict_list(v1_pattern_data)
    # exit(1)
    onset_total_v1 = []

    for i in range(17):
        onset_total_v1.append(0)

    for i in range(len(v1_pattern_data)):
        onset_total_v1[i] = sum(v1_pattern_data[i].values())

    # PART 2
    # apply the frequency data probabilistically
    # stores the info for how frequently a measure appears & computing the frequencies of the data
    for i in range(len(v1_pattern_data)):
        for key, value in v1_pattern_data[i].items():
            v1_pattern_data[i][key] = v1_pattern_data[i][key] / onset_total_v1[i]

    os.chdir('/Users/kw169/Desktop/input')
    file_name = 'danceSugarPlum.xmk'
    # fileName = input("Enter the melody filename: ")

    input_stream, bassline = read_xmk(file_name)

    output_stream = m21.stream.Part()
    output_stream.timeSignature = m21.meter.TimeSignature("4/4")

    for measure_num, measure in enumerate(input_stream.makeMeasures()):
        measure = measure.flat
        #print(measure_num + 1, "===============")
        measure_str = create_onset_str(measure)
        num_onsets = count_onsets(measure_str)
        ragtime_measure = select_ragtime_measure(v1_pattern_data[num_onsets])
        onset_gap = find_largest_onset_gap(measure_str, ragtime_measure)
        while onset_gap > 3 or (measure_str == ragtime_measure and num_onsets > 0):
            print('Gap too large. Measure: ', measure_num, 'Gap: ', onset_gap)
            print('measure: ', measure_str, 'ragtime: ', ragtime_measure)
            ragtime_measure = select_ragtime_measure(v1_pattern_data[num_onsets])
            onset_gap = find_largest_onset_gap(measure_str, ragtime_measure)
        if num_onsets > 0:
            offset = 0
            num = 0
            for item in measure:
                if isinstance(item, m21.note.Note) or isinstance(item, m21.chord.Chord):
                    while offset < len(ragtime_measure) and ragtime_measure[offset] != "1":
                        offset += 1
                    d = m21.duration.Duration()
                    d.quarterLength = get_quarter_length(ragtime_measure, num)
                    item.duration = d
                    num += 1
                    output_stream.insert((offset/4) + (measure_num*4), item)
                    offset += 1

    ragtime_output = m21.stream.Score()
    ragtime_output.insert(0, output_stream)
    ragtime_output.insert(0, bassline)

    print("Showing ragtime output!")
    ragtime_output.show('midi')
    ragtime_output.write("midi", fp="/Users/kw169/Desktop/output/" + file_name + "Rag.mid")


if __name__ == "__main__":
    print("V1Gen")
    main()