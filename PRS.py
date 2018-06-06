#Implements Pressing's Cognitive Cost Model
import string

def getCost(seq, nextSeq = string.empty): #can be improved, instead of passing whole next seq, just need first beat
    if seq[1:] == '0'*len(seq)-1:  # null
        cost = 0
    elif seq == '1'*len(seq)-1:  # filled
        cost = 1
    elif seq[0] == 1 and seq[-1] == 0:  # run1
        cost = 2
    elif seq[0] == 1 and (nextSeq == string.empty or nextSeq[0] == 0):  # run2
        cost = 2
    elif seq[-1] == 1 and nextSeq != string.empty and nextSeq[0] == 1:  # upbeat
        cost = 3
    elif seq[0] == 0:  # syncopated
        cost = 5
    cost *= len(seq)
    return cost

def getSubSequenceCost(measure, divisionLevel):
    cost = 0
    if divisionLevel == 0:
        cost = getCost(measure)
    elif divisionLevel == 1:
        cost = getCost(measure[0:8], measure[8:]) + getCost(measure[8:])
    elif divisionLevel == 2:
        for i in range(4):
            if i == 3:
                cost += getCost(measure[12:])
            else:
                cost += getCost(measure[i * 4, (i+1) * 4], measure[(i+1) * 4 : (i+2) * 4])
    else:
        for i in range(8):
            if i == 7:
                cost += getCost(measure[14:])
            else:
                cost += getCost(measure[i * 2, (i + 1) * 2], measure[(i + 1) * 2: (i + 2) * 2])
    return cost

def getSyncopationLevel(measure):
    sumCosts = 0
    for l in range (0,4):
        sumCosts += getSubSequenceCost(measure, l)
    return sumCosts