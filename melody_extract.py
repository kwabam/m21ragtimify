import music21 as m21
from statistics import mean
import TMC

#localCorpus = m21.corpus.corpora.LocalCorpus()
#localCorpus.removePath("~/Documents/Research/2017-2018/RAGcorpus/")
#localCorpus.addPath("~/Documents/Research/2017-2018/m21proj/RAGcorpus/")
#localCorpus.directoryPaths
#localCorpus.save()
#if (localCorpus.existsInSettings):
#    print("Local corpus is good to go.\n")
#else:
#    print("Local corpus not initialized")

filename = input("Enter the MIDI filename: ")


scoreEx = m21.corpus.parse(filename)
print("Loading the piece before melody has been extracted... ")
scoreEx.show()

## SKYLINE ALGORITHM ##
#take the track with the highest average pitch as the melody"

highestPitches = []
highestMean = 0

count = 0
for part in scoreEx.parts:
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
    print(part)
    if avgPitch > highestMean:
        highestMean = avgPitch
        highestPitches = partPitches
        melodyPart = part
                
    
print("Loading the piece after the melody has been extracted")    
melodyPart.show()
print("Done!")    