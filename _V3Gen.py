import music21 as m21
import os
from _V1Gen import *
from RagtimeFitter import make_onset_total_str
import pickle

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

from melody_extract import skyline
from BassGenerator import generate_bassline


def rhythm_ripper(melody_part, start_measure, end_measure):
    ragtime_onsets = []
    for i,measure in melody_part.makeMeasures():
        if i >= start_measure and i < end_measure:
            onset_str = create_onset_str(measure)
            ragtime_onsets.append(onset_str)
    return ragtime_onsets


def main():
    with open('onset_totals.pkl', 'rb') as f:  # Python 3: open(..., 'wb')
        onset_totals = pickle.load(f)
    print(len(onset_totals))
    np.random.shuffle(onset_totals)
    os.chdir('/Users/kw169/Desktop/input')
    # fileName = input("Enter the melody filename: ")
    file_name = 'twinkle.mid'
    input_stream = m21.converter.parse(file_name)

    score_me = skyline(input_stream)
    classical_onset_str = make_onset_total_str(score_me)
    print(classical_onset_str)
    classical_onset_str = '4-3-4-3'

    print('==========================================================')
    song_matches = 0
    for onset_str, rag_filename in onset_totals:
        index = onset_str.find(classical_onset_str)
        if index >= 0:
            print(index)
            print(onset_str)
            print(onset_str[index:index+len(classical_onset_str)])
            print(rag_filename)
            # score = m21.corpus.parse(rag_filename)
            # score.show('mid')

            song_matches += 1
    print(song_matches)





if __name__ == '__main__':
    main()