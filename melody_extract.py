import music21 as m21
from statistics import mean
import PRS
import matplotlib.pyplot as plt
import numpy as np
import pickle
import collections

#localCorpus = m21.corpus.corpora.LocalCorpus()
#localCorpus.removePath("~/Documents/Research/2017-2018/RAGcorpus/")
#localCorpus.addPath("~/Documents/Research/2017-2018/m21proj/RAGcorpus/")
#localCorpus.directoryPaths
#localCorpus.save()
#if (localCorpus.existsInSettings):
#    print("Local corpus is good to go.\n")
#else:
#    print("Local corpus not initialized")

def convertToOnsetString(measure):
    measure_as_onset_list = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
    for item in measure.flat:
        if isinstance(item, m21.note.Note) or isinstance(item, m21.chord.Chord):
            index = round((item.offset) * 4)
            if index > 15:
                index = 15
            measure_as_onset_list[index] = '1'
    return "".join(measure_as_onset_list)

def pitchAnalysis(part):
    partPitches = []
    for item in part.flat:
        if not isinstance(item, m21.note.Rest):
            if isinstance(item, m21.note.Note):
                partPitches.append(item.pitch.frequency)
            elif isinstance(item, m21.chord.Chord):
                chordList = []
                for note in item:
                    chordList.append(note.pitch.frequency)
                partPitches.append(mean(chordList))
    avgPitch = mean(partPitches)
    return avgPitch, partPitches

if __name__ == "__main__":
    local = m21.corpus.corpora.LocalCorpus()
    paths = local.getPaths()
    alpha_level = .00005
    # with open('syncopationData.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
    #     x, y = pickle.load(f)
    # print(len(x))
    # sort = sorted(x)
    # set = list(set(sort))
    # counter = collections.Counter(sort)
    # print(sorted(counter.keys()))
    # print(counter)
    #
    # plt.scatter(x,y, alphaLevel)
    # plt.xlabel('syncopation of measure x')
    # plt.ylabel('syncopation of measure x + 1')
    #
    # plt.savefig('graph.png')
    # exit(1)

    # filename = "Amazin' Mess, An - Radna"#input("Enter the MIDI filename: ")
    # scoreEx = m21.corpus.parse(filename)
    # print("Loading the piece before melody has been extracted... ")
    x = []
    y = []

    for i, file in enumerate(paths):
        score_ex = m21.converter.parse(file)
        ## SKYLINE ALGORITHM ##
        #take the track with the highest average pitch as the melody"
        highest_pitches = []
        highest_mean = 0
        count = 0
        melody_part = score_ex.parts[0]
        for part in score_ex.parts:
            analysis_info = pitchAnalysis(part) #returns tuple where first element is avgPitch, 2nd is partPitches
            if analysis_info[0] > highest_mean:
                highest_mean = analysis_info[0]
                highest_pitches = analysis_info[1]
                melody_part = part
        ## SYNCOPATION ANALYSIS ##
        #analyse the level of syncopation within each measure of the melody part#
        binary_measures = []
        syncopation_set = []
        for measure in melody_part.makeMeasures():
            #if m21.meter.bestTimeSignature(measure).ratioString == '4/4':
                measure_str = convertToOnsetString(measure)
                binary_measures.append(measure_str)
                syncopation_set.append(PRS.getSyncopationLevel(measure_str))
                #Graphing
                x.extend(syncopation_set[0:-1])
                y.extend(syncopation_set[1:])
        print(i, "i")
        if i%50 == 0: #every 50 pieces, copy data down
            with open('syncopationDataRounded.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
                pickle.dump([x, y], f)

    plt.scatter(x, y, alpha_level)
    plt.xlabel('syncopation of measure x')
    plt.ylabel('syncopation of measure x + 1')
    plt.show()

    with open('test.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([x,y], f)