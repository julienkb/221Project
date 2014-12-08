#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

def getDataset(trainingFile, testingFile, solutionFile, useExtraFeatures, intervalLength = 50):
    reader = csv.DictReader(open(trainingFile), dialect = "excel")
    testReader = csv.DictReader(open(testingFile), dialect = "excel")
    solutionReader = csv.DictReader(open(solutionFile), dialect = "excel")

    atts = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11' ]
    normalFeatures = ['P7', 'V1', 'V6', 'V10', 'V11','E1', 'E7', 'E8', 'E9'] #Enter wanted attributes here
    rangeFeatures = ['E2', 'E5', 'E7', 'E8', 'V3']
    minFeatures = ['V10', 'E6', 'E9']
    maxFeatures = ['E1', 'E2', 'E3', 'E8', 'E9', 'V6', 'V8']
    usedFeatures = list(set(normalFeatures) | set(rangeFeatures) | set(minFeatures) | set(maxFeatures))
    delAtts = list(set(atts) - set(usedFeatures))

    train, test = getNormalFeatures(reader, testReader, solutionReader, usedFeatures, delAtts)
    if useExtraFeatures:
        trainingData = getExtraFeatures(train, intervalLength, rangeFeatures, minFeatures, maxFeatures, normalFeatures)
        testingData = getExtraFeatures(test, intervalLength, rangeFeatures, minFeatures, maxFeatures, normalFeatures)
        return trainingData, testingData
    return train, test

def getSolution(solutionReader):
    solution = []
    print "Reading solutions"
    # Load the solution in an array, since it isn't included in the testingData file
    for row in solutionReader:
        if row['Prediction'] == '0': # Want negative, not just 0
            solution.append(-1)
        else:
            solution.append(1)
    return solution

def getNormalFeatures(reader, testReader, solutionReader, useAtts, delAtts):
    # Data is a list of tuples. The first element is a dict of variable names to values,
    # the second is the IsAlert indicator
    trainingData = []
    testingData = []

    print "Reading training data"
    for row in reader:
        del row['TrialID']
        del row['ObsNum']
        for attribute in delAtts:
            del row[attribute]

        if row['IsAlert'] == '1':
            isAlert = 1
        else:
            isAlert = -1
        del row['IsAlert'] # Take isAlert indicator out of the features
        trainingData.append((row, isAlert))

    solution = getSolution(solutionReader)

    print "Reading testing data"
    i = 0
    for row in testReader:
        del row['TrialID']
        del row['ObsNum']
        for attribute in delAtts:
            del row[attribute]

        del row['IsAlert'] # Take isAlert indicator out of the features
        testingData.append((row, solution[i]))
        i += 1

    return trainingData, testingData

def getExtraFeatures(oldData, intervalLength, rangeFeatures, minFeatures, maxFeatures, normalFeatures):
    # invervalLength is the number of timesteps in the range
    # Return new data set, values are the averages or range of each feature over that time range
    print "Calculating average and range features over intervals"
    newData = []

    timestepsPerDriver = 1210 # Constant from the data
    numMixed, numAlert, numDrowsy = 0, 0, 0
    for driver in xrange(0, len(oldData)/timestepsPerDriver):
        for interval in xrange(0, timestepsPerDriver/intervalLength):
            startIndex = driver*timestepsPerDriver + interval*intervalLength
            endIndex = startIndex + intervalLength

            intervalData = {}
            for f in normalFeatures:
                intervalData[f] = getIntervalAvg(oldData, f, startIndex, endIndex)

            for f in rangeFeatures:
                intervalData['R' + f] = getIntervalRange(oldData, f, startIndex, endIndex)

            for f in minFeatures:
                intervalData['Min'+f] = getIntervalMin(oldData, f, startIndex, endIndex)

            for f in maxFeatures:
                intervalData['Max'+f] = getIntervalMax(oldData, f, startIndex, endIndex)

            alert = getIntervalAvgAlert(oldData, startIndex, endIndex)
            if alert == 0:
                numMixed = numMixed + 1
            elif alert == 1:
                numAlert = numAlert + 1
                newData.append((intervalData, alert))
            else:
                numDrowsy = numDrowsy + 1
                newData.append((intervalData, alert))
    print numMixed, numAlert, numDrowsy
    return newData

def getIntervalAvgAlert(data, startIndex, endIndex):
    sum = 0.0
    for i in range(startIndex, endIndex):
        sum = sum + data[i][1]
    avgAlertness = float(sum)/(endIndex-startIndex)
    if avgAlertness >= 0.5:
        return 1
    elif avgAlertness <= -0.5:
        return -1
    else:
        return 0

def getIntervalAvg(data, feature, startIndex, endIndex):
    sum = 0.0
    for i in range(startIndex, endIndex):
        sum = sum + float(data[i][0][feature])
    return sum/(endIndex - startIndex)

def getIntervalRange(data, feature, startIndex, endIndex):
    vals = []
    for i in range(startIndex, endIndex):
        vals.append(float(data[i][0][feature]))
    return max(vals) - min(vals)

def getIntervalMax(data, feature, startIndex, endIndex):
    vals = []
    for i in range(startIndex, endIndex):
        vals.append(float(data[i][0][feature]))
    return max(vals)

def getIntervalMin(data, feature, startIndex, endIndex):
    vals = []
    for i in range(startIndex, endIndex):
        vals.append(float(data[i][0][feature]))
    return min(vals)
