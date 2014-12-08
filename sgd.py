#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, util, time

def dotProduct(f1, f2):
    if len(f1) > len(f2):
        return sum(float(f1.get(feature,0)) * float(val) for feature,val in f2.items())
    else:
        return sum(float(f2.get(feature,0)) * float(val) for feature,val in f1.items())

def evaluatePredictor(examples, predictor):
    error = 0
    for x, y in examples:
        if predictor(x) != y:
            error += 1
    return 1.0 * error / len(examples)

def featureExtractor(x):
    # right now only returns the observation as is,
    # should add more features later
    return x

def increment(d1, scale, d2):
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + float(v) * scale

def stochasticGradientDescent(trainExamples, testExamples, prune = False):
    print "Starting stochastic gradient descent"
    weights = {}  # feature => weight
    numIters = 5
    def predictor(x):
        if dotProduct(weights, featureExtractor(x)) > 0:
            return 1
        return -1

    for i in range(0, numIters):
        stepSize = 0.001/((i+1)**2)
        for x,y in trainExamples:
            features = featureExtractor(x)
            score = dotProduct(weights, features) * y
            if score <= 1: # gradient is -Phi(x)y, subtract gradient * stepSize
                increment(weights, y*stepSize, features)
        if prune and i > 0:
            # Eliminate the lowest weight features
            removeVars = []
            for f in weights:
                if abs(weights[f]) < 0.1:
                    removeVars.append(f)
            for f in removeVars:
                del weights[f]

        #print weights
        print "Iteration: {}, Training data error: {}, Testing data error: {}".format(i+1, \
        evaluatePredictor(trainExamples, predictor), evaluatePredictor(testExamples, predictor))

    return weights


def main():
    for timeInterval in [10,20,50,100,200]:
        print "Time interval:", timeInterval
        trainingData, testingData = util.getDataset("fordTrain.csv", "fordTest.csv", "solution.csv", True, timeInterval)
        for prune in [True, False]:
            print "Pruning:", prune
#startTime = time.clock()

#dataEndTime = time.clock()
            stochasticGradientDescent(trainingData, testingData, prune)
#endTime = time.clock()
    #print "Total time spent was ", endTime-startTime
    #print "Time spent loading data was ", dataEndTime-startTime
    #print "Time spent running SGD was ", endTime-dataEndTime


main()
