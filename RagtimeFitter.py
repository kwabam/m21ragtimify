from _V1Gen import *
import pickle


def make_onset_total_str(part):
    onset_list = []
    for measure in part.makeMeasures():
        measure_str = create_onset_str(measure)
        measure_onsets = count_onsets(measure_str)
        if measure_onsets > 0:
            onset_list.append(measure_onsets)
    return '-'.join(str(x) for x in onset_list)


def main():
    paths = os.listdir(r'C:\Users\kw169\Desktop\SortedMidis\common')
    onset_totals = []
    for i, file in enumerate(paths):
        try:
            if random.random() < (len(paths)):
                onset_list = []
                print(i, "i")
                score = m21.corpus.parse(file)
                melody_part = skyline(score)
                print("Piece parsed into melody part")
                onset_totals.append((make_onset_total_str(melody_part), file))
                print(onset_totals[-1])

            if i % 100 == 0:
                with open('onset_totals_backup.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
                    pickle.dump(onset_totals, f)
        except:
            print('error', i)
    with open('onset_totals.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump(onset_totals, f)
    return 0


if __name__ == '__main__':
    main()