import music21 as m21
import os
from melody_extract import *

def main():
    print("Hello World")
    return 0

def costly_func():
   return map(lambda x: x^2, range(10))

def syncopation():
    paths = os.listdir(r'C:\Users\kw169\Desktop\sennatest')

    c = 0
    x = []
    y = []
    for i, file in enumerate(paths):
        if i < 10:
            score_ex = m21.corpus.parse(file)
            ## SKYLINE ALGORITHM ##
            # take the track with the highest average pitch as the melody"
            highest_pitches = []
            highest_mean = 0
            count = 0
            melody_part = score_ex.parts[0]
            for part in score_ex.parts:
                analysis_info = pitchAnalysis(part)  # returns tuple where first element is avgPitch, 2nd is partPitches
                if analysis_info[0] > highest_mean:
                    highest_mean = analysis_info[0]
                    highest_pitches = analysis_info[1]
                    melody_part = part
            ## SYNCOPATION ANALYSIS ##
            # analyse the level of syncopation within each measure of the melody part#
            binary_measures = []
            syncopation_set = []
            for measure in melody_part.makeMeasures():
                # if m21.meter.bestTimeSignature(measure).ratioString == '4/4':
                # use try and except block, count how many are in 4/4
                measure_str = convertToOnsetString(measure)
                binary_measures.append(measure_str)
                syncopation_set.append(PRS.getSyncopationLevel(measure_str))
                # Graphing
                x.extend(syncopation_set[0:-1])
                y.extend(syncopation_set[1:])

if __name__ == '__main__':
    import time
    start_time = time.time()
    syncopation()
    print("--- %s seconds ---" % (time.time() - start_time))