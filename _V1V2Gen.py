# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 12:43:00 2018

@author: zaid
"""

import music21 as m21
import json
import os
import random
from statistics import mean

def countOnsets(measureStr):
    count = 0
    for char in measureStr:
        if char == 'I':
            count += 1
    return count

def melodyExtract(scoreEx):
    
    ## SKYLINE ALGORITHM ##
    #take the track with the highest average pitch as the melody
    
    highestPitches = []
    highestMean = 0

    for part in scoreEx.parts:
        for thing in part:
            if 'Voice' in thing.classSet:
                print(thing)
                voicePitches = []
                for item in thing:
                    print(item)
                    if 'Chord' in item.classSet:
                        chordList = []
                        for note in item:

                            voicePitches.append(note.pitch.midi)
                    elif 'Note' in item.classSet:
                        voicePitches.append(item.pitch.midi)        
                avgPitch = mean(voicePitches)
                if avgPitch > highestMean:
                    highestMean = avgPitch
                    melodyPart = thing
            
    print("this was selected", melodyPart)
    return melodyPart

# rework this method of choosing probabilistically
def selectProb(dct):
    #take the complete database
        #take this onset measures divide by
        #total number of n-onset measures
        
    #the summation style is OK to do here
    rand_val = random.random()
    total = 0
    for key, value in dct.items():
          total += value
          if rand_val <= total:
              print(key)
              return key

def main():
    v1PatternData = json.load(open("v1Database.json"))
    v2PatternData = json.load(open("v2Database.json"))
    
    onsetTotalV1 = []
    onsetTotalV2 = []
    
    for i in range(17):
        onsetTotalV1.append(0)
    
    for i in range(33):
        onsetTotalV2.append(0)
    
    position = 0
    for element in v1PatternData:
        count = 0
        for key in element:
            count+=1
            
        onsetTotalV1[position] = count
        position+=1

    position = 0
    for element in v2PatternData:
        count = 0
        for key in element:
            count+=1
            
        onsetTotalV2[position] = count
        position+=1
    
    
    
    ### PART 2
    ### apply the frequency data probabilistically
    # stores the info for how frequently a measure appears
    
    # / computing the frequencie
    # s of the data
    for i in range(17):
        for key, value in v1PatternData[i].items():
            v1PatternData[i][key] = v1PatternData[i][key]/onsetTotalV1[i]
        
    for i in range(33):
        for key, value in v2PatternData[i].items():
            v2PatternData[i][key] = v2PatternData[i][key]/onsetTotalV2[i]
        
    os.chdir('/Users/kw169/Documents/Research/2017-2018/m21proj/xm')
    fileName = input("Enter the melody filename: ")
    
    inputStream = m21.converter.parse(fileName)
    scoreMe = melodyExtract(inputStream).makeMeasures()

    outputStreamV1 = m21.stream.Stream()
    outputStreamV2 = m21.stream.Stream()
    
    outputStreamV1.timeSignature = m21.meter.TimeSignature("4/4")

    measureNum = 0
    measureStr = ""
    for measure in scoreMe:       
        print(measure)
        count+=1
        measureList = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        measure = measure.flat
        for item in measure:
            #print(note)
            if 'Note' in item.classSet or 'Chord' in item.classSet:
                print(item)
                measureList[int(item.offset*4)] = "I"
#                positionInMeasure = int(((note.getOffsetInHierarchy(scoreMe)-1)%4)*4)
#                measureList[positionInMeasure] = "I"

        if count != 1:
            prevMeasureStr = measureStr
        measureStr = "".join(measureList)

        numOnsetsCurr = countOnsets(measureStr)
        print(numOnsetsCurr)

        ragtimeMeasureToApplyV1 = selectProb(v1PatternData[numOnsetsCurr])
        if count != 1:
            ragtimeMeasureToApplyV2 = selectProb(v2PatternData[numOnsetsCurr+countOnsets(prevMeasureStr)])

        # applying the data to the measure (shifting onsets)
        #newMeasure = m21.stream.Measure()
        #newMeasure.timeSignature = m21.meter.TimeSignature("4/4")
        
        offset = 0
        for item in measure:
            #print(note)
            if 'Note' in item.classSet or 'Chord' in item.classSet:
                print("ragtiming ", item)
                print("into measure", measureNum)
                while ragtimeMeasureToApplyV1[offset] != "I":
                    offset+=1
                    if offset > len(ragtimeMeasureToApplyV1):
                        break
                if offset > len(ragtimeMeasureToApplyV1):
                    break
    #            if isinstance(note, m21.note.Note) or isinstance(note, m21.chord.Chord):
                #newMeasure.insert(offset, item)
                outputStreamV1.insert((offset/4)+(measureNum*4), item)
                print("at offset " + str((offset/4)+(measureNum*4)))
                offset+=1

#        outputStreamV1.append(newMeasure)
        measureNum+=1
        # outputStreamV2.append(newMeasure)

    outputStreamV1.write("midi", fp="/Users/kw169/Desktop/"+fileName+"Rag.midi")


if __name__ == "__main__":
    print("V1V2Gen")
    main()