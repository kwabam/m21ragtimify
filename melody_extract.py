import music21 as m21
from statistics import mean
import PRS
import matplotlib.pyplot as plt
import numpy as np
import pickle
import collections
from shutil import copyfile
import os

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
    print(avgPitch)
    return avgPitch, partPitches

def skyline(score_ex):
    ## SKYLINE ALGORITHM ##
    # take the track with the highest average pitch as the melody
    melody_part = []
    highest_pitches = []
    highest_mean = 0
    for part in score_ex.parts:
        analysis_info = pitchAnalysis(part)  # returns tuple where first element is avgPitch, 2nd is partPitches
        if analysis_info[0] > highest_mean:
            highest_mean = analysis_info[0]
            highest_pitches = analysis_info[1]
            melody_part = part
    return melody_part

def find_timesig(file_name):
    score = m21.corpus.parse(file_name + ".mxl")
    print("File parsed")
    ts = score.recurse().getElementsByClass(m21.meter.TimeSignature)
    flag = 0
    for item in ts:
        print(item)
        if item.ratioString == '4/4' or item.ratioString == '2/4' or item.ratioString == '2/2':
            flag = 1

    score.show('midi')
    new_score = score.flat.getElementsNotOfClass(m21.meter.TimeSignature)
    ts = new_score.recurse().getElementsByClass(m21.meter.TimeSignature)
    print("Time signature removed")
    for item in ts:
        print(item)
    new_score.show('midi')
    print("Showing no time signature")
    ts = new_score.recurse().getElementsByClass(m21.meter.TimeSignature)
    print("Time signature removed")
    for item in ts:
        print(item)
    new_score.insert(0, m21.meter.TimeSignature('4/4'))
    new_score.show('midi')
    print("With inserted 4/4")
    ts = new_score.recurse().getElementsByClass(m21.meter.TimeSignature)
    print("Time signature removed")
    for item in ts:
        print(item)

def check_parts(file_name):
    score = m21.corpus.parse(file_name + ".mxl")
    score.show('mid')

    for part in score.parts:
        print(part.partName)
        print(part[0].bestName())
        part.flat.show('mid')


if __name__ == "__main__":
    paths = os.listdir(r'C:\Users\kw169\Desktop\SortedMidis\common')
    nc_paths = os.listdir(r'C:\Users\kw169\Desktop\SortedMidis\non-common')
    #
    # for i, file_name in enumerate(nc_paths):
    #     score = m21.corpus.parse(file_name)
    #     ts = score.recurse().getElementsByClass(m21.meter.TimeSignature)
    #     flag = 0
    #     for item in ts:
    #         print(item)
    #         if not(item.ratioString == '4/4' or item.ratioString == '2/4' or item.ratioString == '2/2'):
    #             print(file_name, i)
    # exit(1)
    print("Running!")
    os.chdir(r'C:\Users\kw169\Desktop\ograg')
    file_name = r"12th Street Blues (Heagney) (CAP A-1951-8) - unk ex Himpsl"
    file_name = input("File Name:")
    #find_timesig(file_name)
    check_parts(file_name)
    #new_score.write("midi", fp="/Users/kw169/Desktop/output/" + file_name)

    #score.show('mid')
    exit(1)
        # us = m21.environment.UserSettings()
        # us['localCorpusPath'] = r'C:\Users\kw169\Desktop\Midis'
        # print(list(us['localCorpusSettings']))
        # yes  = []
        # no = []
        # for i, filename in enumerate(os.listdir(r'C:\Users\kw169\Desktop\SortedMidis\common')):
        #     print(i)
        #     try:
        #         score_ex = m21.corpus.parse(filename)
        #         yes.append((i, filename))
        #     except:
        #         print(filename)
        #         no.append((i,filename))
        # with open('yes.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        #     pickle.dump(yes, f)
        # with open('no.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        #     pickle.dump(no, f)
        # exit(1)
    #start up sequence
    local = m21.corpus.corpora.LocalCorpus()
    paths = local.getPaths()
    alpha_level = .00005
    print(len(paths))

    # print("load errors and non_common_time, then counts frequency of each time signature")
    # with open('errors.pkl', 'rb') as f:  # Python 3: open(..., 'wb')
    #     errors = pickle.load(f)
    # with open('test.pkl', 'rb') as f:  # Python 3: open(..., 'wb')
    #     non_common_time = pickle.load(f)
    # # for i in errors:
    # #     print(i)
    # time_signatures = {}
    #
    # #count the number of times each time signature is used
    # #for item in non_common_time:
    # for i,key in non_common_time:
    #     try:
    #         time_signatures[key] += 1
    #     except:
    #         time_signatures[key] = 1
    # #print results
    # for i,key in time_signatures.items():
    #     print(i,key)
    #
    # exit(1)
    print('opens syncopation data and compares syncopation in measure x to measure x + 1')
    #
    # with open('syncopationData.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
    #     x, y = pickle.load(f)
    # print(len(x))
    # sort = sorted(x)
    # set = list(set(sort))
    # counter = collections.Counter(sort)
    # print(sorted(counter.keys()))
    # print(counter)

    # plt.scatter(x,y, alphaLevel)
    # plt.xlabel('syncopation of measure x')
    # plt.ylabel('syncopation of measure x + 1')

    #plt.savefig('graph.png')
    # exit(1)
    print("score extract")
    # filename = "Amazin' Mess, An - Radna"#input("Enter the MIDI filename: ")
    # scoreEx = m21.corpus.parse(filename)
    # print("Loading the piece before melody has been extracted... ")
    c = 0;
    non_common_time = []
    errors = []
    #TIME SIGNATURE CHECKER
    #check the time signature of each file in paths
    #c = number of 4/4 pieces
    #append non 4/4 pieces to non_common_time
    #weird time signatures that cause music21 to bug out go into errors
    path = 'C:/Users/kw169/Desktop/SortedMidis/'
    ts_common = m21.meter.TimeSignature('4/4')
    for i, file in enumerate(paths):
        score_ex = m21.converter.parse(file)
        try:
            time_signatures = score_ex.recurse().getElementsByClass(m21.meter.TimeSignature)
        except:
            print("error: finding time sig ", i)
            errors.append((i, file))
            continue
        try:
            if time_signatures[0].ratioString == '4/4':
                c += 1
                copyfile(file, path + '/common/' + str(file)[29:-4] + '.xml')
            else:
                print(str(file)[29:-4], end='\n\t')
                count = {}
                for ts in time_signatures:
                    try:
                        count[ts.ratioString] += 1
                    except:
                        count[ts.ratioString] = 1
                sig = time_signatures[0].ratioString
                for key,value in count.items():
                    if value > count[sig]:
                        sig = key
                if sig == '4/4':
                    c += 1
                    copyfile(file, path + '/common/' + str(file)[29:-4] + '.xml')
                    print('common (2nd test)')

                else:
                    copyfile(file, path + '/non-common/' + str(file)[29:-4] + '.xml')
                    ts_tuple = (file, sig)
                    print(count)
                    non_common_time.append(ts_tuple)
        except:
            print("error: ratio string/copy", i)
            errors.append((i,file))

        #print out some status messages to show how run is going
        if((i+1)%50 == 0):
            print(c, "successes out of ", (i+1))
            with open('errors.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
                pickle.dump(errors, f)
            with open('test.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
                pickle.dump(non_common_time, f)
    #print stats when everything is done
    print("Job's done!\n", c, "successes out of ", len(paths))
    with open('errors.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump(errors, f)
    with open('test.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump(non_common_time, f)
    exit(1)

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
            #use try and except block, count how many are in 4/4
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