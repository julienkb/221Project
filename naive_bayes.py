#!/usr/bin/env python
# -*- coding: utf-8 -*-
import util
import math, time

def getVariance(average, values):
    return sum((average - val) ** 2 for val in values) / len(values)

def getNaiveBayes(trainingData):
    # mean and variance of each feature, divided by alert/not alert
    alertDist = {}
    drowsyDist = {}

    # iterate over each feature
    for f in trainingData[0][0]:
        print "Calculating distribution for feature", f
        alertVals = []
        drowsyVals = []
        # iterate over dataset
        for i in range(0, len(trainingData)):
            x, y = trainingData[i]
            if y == 1: # Alert
                alertVals.append(float(x[f]))
            if y == -1: # Not Alert
                drowsyVals.append(float(x[f]))

        alertMean  = sum(alertVals)/len(alertVals)
        drowsyMean = sum(drowsyVals)/len(drowsyVals)
        alertVar   = getVariance(alertMean, alertVals)
        drowsyVar  = getVariance(drowsyMean, drowsyVals)

        alertDist[f]  = (alertMean, alertVar)
        drowsyDist[f] = (drowsyMean, drowsyVar)
    print alertDist, drowsyDist
    return alertDist, drowsyDist

def getNormalProb(dist, val): # Get the normal probability using the dist (mean, variance)
    mean, var = dist
    if var == 0.0: # strange edge case
        return 1.0
    return (1.0/math.sqrt(2.0*math.pi*var))*math.exp(-((mean-val)**2)/(2.0*var))

def predictor(evidence, alertDist, drowsyDist):
    alertProb, drowsyProb = 1.0, 1.0
    for f, val in evidence.iteritems():
        alertProb  = alertProb * getNormalProb(alertDist[f], float(val))
        drowsyProb = drowsyProb * getNormalProb(drowsyDist[f], float(val))

    if alertProb > drowsyProb:
        return 1
    else:
        return -1

def evaluateNaiveBayes(trainingData, testingData, alertDist, drowsyDist):
    error = 0
    for x, y in trainingData:
        if predictor(x, alertDist, drowsyDist) != y:
            error += 1
    print "Training data error is {}".format(1.0 * error / len(trainingData))

    error = 0
    for x, y in testingData:
        if predictor(x, alertDist, drowsyDist) != y:
            error += 1
    print "Testing data error is {}".format(1.0 * error / len(testingData))

def getGreatestDifferences(alertDist, drowsyDist):
    for f in alertDist:
        diff = alertDist[f][0] - drowsyDist[f][0]
        std = math.sqrt(alertDist[f][1] + drowsyDist[f][1])
        if std == 0:
            print 0
        else:
            print f, diff/std

def main():
    startTime = time.clock()
    trainingData, testingData = util.getDataset("fordTrain.csv", "fordTest.csv", "solution.csv", True)
    dataEndTime = time.clock()
    alertDist, drowsyDist = getNaiveBayes(trainingData)
    evaluateNaiveBayes(trainingData, testingData, alertDist, drowsyDist)
    getGreatestDifferences(alertDist, drowsyDist)
    endTime = time.clock()
    print "Total time was ", endTime-startTime
    print "Time to read data was ", dataEndTime-startTime
    print "Time to learn and test Naive Bayes was ", endTime-dataEndTime

main()
