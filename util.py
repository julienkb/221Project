#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv


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
