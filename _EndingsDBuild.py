from melody_extract import *
import json
import os
import random
from _DBuild import countOnsets

def main():
    local = m21.corpus.corpora.LocalCorpus()
    paths = os.listdir(r'C:\Users\kw169\Desktop\SortedMidis\common')
    f = open("listed_directory.txt", "w")
    for path in paths:
        f.write(path + '\n')

    exit(1)
    v3PatternData = []
    for i in range(33):
        v3PatternData.append({})

    print("Running!")
    c = 0
    for i, file in enumerate(paths):
        try:
            if random.random() < (len(paths)):
                c += 1
                print(i, "i")
                score = m21.corpus.parse(file)
                melody_part = skyline(score)
                melody_part = melody_part.makeMeasures()
                m1 = melody_part[-2]
                m2 = melody_part[-1]

                m1 = convertToOnsetString(m1)
                m2 = convertToOnsetString(m2)

                onset_totals = countOnsets(m1) + countOnsets(m2)

                try:
                    v3PatternData[onset_totals][m1 + m2] += 1
                except:
                    v3PatternData[onset_totals][m1 + m2] = 1


        except:
            print('error', i)

    for dict in v3PatternData:
        print(dict)

    with open("v3Database.json", "w") as f:
        f.write(json.dumps(v3PatternData, indent=4))

if __name__ == '__main__':
    main()