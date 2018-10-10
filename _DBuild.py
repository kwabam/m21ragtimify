# -*- coding: utf-8 -*-
import music21 as m21
from melody_extract import convertToOnsetString
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


def main():
    v1PatternData = []
    v2PatternData = []

    # holds the number of measures that have i number of onsets
    onsetTotalV1 = []
    onsetTotalV2 = []

    for i in range(17):
        onsetTotalV1.append(0)
        v1PatternData.append({})

    for i in range(33):
        onsetTotalV2.append(0)
        v2PatternData.append({})
    # local = m21.corpus.corpora.LocalCorpus()
    # fileList = local.getPaths()
    # pieceNames = open("ragPieces.txt", "r", encoding='latin1')
    # for line in pieceNames:
    #     fileName = line.rstrip()
    #     fileList.append(fileName)
    #
    #     # pls raise error here if problem
    #
    # pieceNames.close()
    local = m21.corpus.corpora.LocalCorpus()
    paths = local.getPaths()

    print("Running!")
    for i, file in enumerate(paths):
        print(i, "i")
        score_ex = m21.converter.parse(file)
        # print("Loading "+ path)
        # convert measure into a string of onsets
        for c, measure in enumerate(score_ex.makeMeasures()):
            measure_str = convertToOnsetString(measure)
            measure_onsets = countOnsets(measure_str)
            if c > 0:
                prev_measure_str = measure_str
                two_measure_onsets = measure_onsets + countOnsets(prev_measure_str)
                onsetTotalV2[two_measure_onsets] += 1
            onsetTotalV1[measure_onsets] += 1

            # add the measure string into the v1/v2 data
            if measure_str not in v1PatternData[measure_onsets]:
                v1PatternData[measure_onsets][measure_str] = 1
            else:
                v1PatternData[measure_onsets][measure_str] += 1
            if c > 0:
                if measure_str not in v2PatternData[measure_onsets]:
                    v2PatternData[two_measure_onsets][measure_str + prev_measure_str] = 1
                else:
                    v2PatternData[two_measure_onsets][measure_str + prev_measure_str] += 1

    with open("v1Database.json", "w") as f:
        f.write(json.dumps(v1PatternData, indent=4))
    with open("v2Database.json", "w") as g:
        g.write(json.dumps(v2PatternData, indent=4))


if __name__ == "__main__":
    print("DBuild")
    main()
