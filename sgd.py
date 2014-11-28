#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

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

def stochasticGradientDescent(trainExamples, testExamples):
    print "Starting stochastic gradient descent"
    weights = {}  # feature => weight
    numIters = 20
    def predictor(x):
        if dotProduct(weights, featureExtractor(x)) > 0:
            return 1
        return -1

    for i in range(0, numIters):
        stepSize = 0.001/(numIters**2)
        for x,y in trainExamples:
            features = featureExtractor(x)
            score = dotProduct(weights, features) * y
            if score <= 1: # gradient is -Phi(x)y, subtract gradient * stepSize
                increment(weights, y*stepSize, features)

        print weights
        print "Iteration: {}, Training data error: {}, Testing data error: {}".format(i+1, \
        evaluatePredictor(trainExamples, predictor), evaluatePredictor(testExamples, predictor))

    return weights

def getDataset(trainingFile, testingFile, solutionFile):
    # Data is a list of tuples. The first element is a dict of variable names to values,
    # the second is the IsAlert indicator
    trainingData = []
    testingData = []
    solution = []

    reader = csv.DictReader(open(trainingFile), dialect = "excel")
    testReader = csv.DictReader(open(testingFile), dialect = "excel")
    solutionReader = csv.DictReader(open(solutionFile), dialect = "excel")

    print "Reading training data"
    for row in reader:
        del row['TrialID']
        del row['ObsNum']
        if row['IsAlert'] == '1':
            isAlert = 1
        else:
            isAlert = -1
        del row['IsAlert'] # Take isAlert indicator out of the features
        trainingData.append((row, isAlert))

    print "Reading solutions"
    # Load the solution in an array, since it isn't included in the testingData file
    for row in solutionReader:
        if row['Prediction'] == '0': # Want negative, not just 0
            solution.append(-1)
        else:
            solution.append(1)

    print "Reading testing data"
    i = 0
    for row in testReader:
        del row['TrialID']
        del row['ObsNum']
        del row['IsAlert'] # Take isAlert indicator out of the features
        testingData.append((row, solution[i]))
        i += 1

    return trainingData, testingData

def main():
    trainingData, testingData = getDataset("fordTrain.csv", "fordTest.csv", "solution.csv")
    stochasticGradientDescent(trainingData, testingData)

main()
