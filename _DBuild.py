# -*- coding: utf-8 -*-
import music21 as m21
from melody_extract import *
import json
import os
import random


#  countOnsets count the number of note onsets in measure
def countOnsets(measureStr):
    count = 0
    for char in measureStr:
        if char == '1':
            count += 1
    return count

def V2_Build():
    v2PatternData = []
    onsetTotalV2 = []
    for i in range(33):
        onsetTotalV2.append(0)
        v2PatternData.append({})
    local = m21.corpus.corpora.LocalCorpus()
    paths = os.listdir(r'C:\Users\kw169\Desktop\SortedMidis\common')

    print("Running!")
    c = 0
    for i, file in enumerate(paths):
        try:
            if random.random() < (1000 / len(paths)):
                c += 1
                print(i, "i")
                score = m21.corpus.parse(file)
                melody_part = skyline(score)
                # print("Loading "+ path)
                # convert measure into a string of onsets
                for c, measure in enumerate(melody_part.makeMeasures()):
                    measure_str = convertToOnsetString(measure)
                    measure_onsets = countOnsets(measure_str)
                    if c > 0:
                        prev_measure_str = measure_str
                        two_measure_onsets = measure_onsets + countOnsets(prev_measure_str)
                        onsetTotalV2[two_measure_onsets] += 1
                    # add the measure string into the v2 data
                    if c > 0:
                        if measure_str not in v2PatternData[measure_onsets]:
                            v2PatternData[two_measure_onsets][measure_str + prev_measure_str] = 1
                        else:
                            v2PatternData[two_measure_onsets][measure_str + prev_measure_str] += 1
        except:
            print('error', i)

    with open("v2Database.json", "w") as g:
        g.write(json.dumps(v2PatternData, indent=4))

def main():
    v1PatternData = []

    # holds the number of measures that have i number of onsets
    onsetTotalV1 = []

    for i in range(17):
        onsetTotalV1.append(0)
        v1PatternData.append({})


    local = m21.corpus.corpora.LocalCorpus()
    paths = os.listdir(r'C:\Users\kw169\Desktop\SortedMidis\common')

    print("Running!")
    c = 0
    for i, file in enumerate(paths):
        try:
            if random.random() < (1000 / len(paths)):
                c += 1
                print(i, "i")
                score = m21.corpus.parse(file)
                melody_part = skyline(score)
                # print("Loading "+ path)
                # convert measure into a string of onsets
                for c, measure in enumerate(melody_part.makeMeasures()):
                    measure_str = convertToOnsetString(measure)
                    measure_onsets = countOnsets(measure_str)
                    if c > 0:
                        prev_measure_str = measure_str
                        two_measure_onsets = measure_onsets + countOnsets(prev_measure_str)
                        onsetTotalV2[two_measure_onsets] += 1
                    onsetTotalV1[measure_onsets] += 1

                    # add the measure string into the v1/v2 data
                    try:
                        v1PatternData[measure_onsets][measure_str] += 1
                    except:
                        v1PatternData[measure_onsets][measure_str] = 1
                    if c > 0:
                        if measure_str not in v2PatternData[measure_onsets]:
                            v2PatternData[two_measure_onsets][measure_str + prev_measure_str] = 1
                        else:
                            v2PatternData[two_measure_onsets][measure_str + prev_measure_str] += 1
        except:
            print('error', i)

    with open("v1Database.json", "w") as f:
        f.write(json.dumps(v1PatternData, indent=4))
    with open("v2Database.json", "w") as g:
        g.write(json.dumps(v2PatternData, indent=4))


if __name__ == "__main__":
    print("v2DBuild")
    V2_Build()
    print("Job's Done!")
