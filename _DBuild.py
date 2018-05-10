# -*- coding: utf-8 -*-
import music21 as m21
import json
import os
import random

#countOnsets – count the number of note onsets in measure (marked w/ "I")
def countOnsets(measureStr):
    count = 0
    for char in measureStr:
        if char == 'I':
            count += 1
    return count

def main():
    #holds 
    v1PatternData = []
    v2PatternData = []
    
    #holds the number of measures that have i number of onsets
    onsetTotalV1 = []
    onsetTotalV2 = []
    
    for i in range(17):
        onsetTotalV1.append(0)
        v1PatternData.append({})  
    
    for i in range(33):
        onsetTotalV2.append(0)
        v2PatternData.append({})
    
    pieceNames = open("ragPieces.txt", "r", encoding='latin1')
    fileList = []
    
    
    for line in pieceNames:
        fileName = line.rstrip()
        fileList.append(fileName) 
        
        # pls raise error here if problem        
    
    pieceNames.close()
    
    for i in range(len(fileList)):
        
        if i > 79:
            break

        scoreEx = m21.corpus.parse(fileList[i])
        print("Loading "+ fileList[i]) 

        scoreMe = scoreEx[0].makeMeasures()
        
        i+=1
        count = 0
        prevMeasureStr = ""
        measureStr = ""
        
        # convert measure into a string of onsets
        for measure in scoreMe:            
            count+=1
            measureList = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
            measure = measure.flat
            noteCount = 0
            for note in measure:
                noteCount+=1
                measureList[int(note.offset*4)] = "I"
                #measureList[int(note.offset*4)]
                #if isinstance(note, m21.note.Note) or isinstance(note, m21.chord.Chord):
#                    measureList[int(note.offset*4)] = "I"
#                    positionInMeasure = int(((note.getOffsetInHierarchy(scoreMe)-1)%4)*4)
#                    measureList[positionInMeasure] = "I"
            measureStr = "".join(measureList)
#            if noteCount < 1:
#                print("check out this piece, look @ measure ", count)
            
            # update the total number of measures with that many onsets
            if count != 1:
                prevMeasureStr = measureStr
                onsetTotalV2[countOnsets(measureStr+prevMeasureStr)] += 1
            onsetTotalV1[countOnsets(measureStr)] += 1

            # add the measure string into the v1/v2 data
            if measureStr not in v1PatternData[countOnsets(measureStr)]:
                v1PatternData[countOnsets(measureStr)][measureStr] = 1
            else:
                v1PatternData[countOnsets(measureStr)][measureStr] += 1
            if count != 1:  
                if measureStr not in v2PatternData[countOnsets(measureStr)]:
                    v2PatternData[countOnsets(measureStr+prevMeasureStr)][measureStr+prevMeasureStr] = 1
                else:
                    v2PatternData[countOnsets(measureStr+prevMeasureStr)][measureStr+prevMeasureStr] += 1
                    
                    #funfile.close()
    
    with open("v1Database.json","w") as f:
        f.write(json.dumps(v1PatternData, indent =4))
    with open("v2Database.json","w") as g:
        g.write(json.dumps(v2PatternData, indent = 4))
       
    
main()