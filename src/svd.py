# -*- coding: utf-8 -*-

import numpy as np
import data


def findNumber(S, level):
    size = len(S)
    
    SSum = S.sum()
    tmpSum = 0.0
    
    for i in xrange(size):
        tmpSum += S[i]
        if tmpSum / SSum >= level:
            return i
    return size
    
def getSVDRec(dataArray, level = 0.7):

    usersNo = len(np.unique(dataArray[:,0]))
    moviesNo = len(np.unique(dataArray[:,1]))
    dataNo = len(dataArray)
    
    dataMatrix = np.zeros(shape=(usersNo, moviesNo))

    for i in range(dataNo):
        row = dataArray[i,0]-1
        col = dataArray[i,1]-1
        value = dataArray[i,2]
        dataMatrix[row, col] = value
        
    movieMeans = dataMatrix.sum(0)/(dataMatrix != 0).sum(0)
    
    for i in range(moviesNo):
        dataMatrix[:,i][(dataMatrix[:,i] == 0)] = movieMeans[i]
    
    U, S1, V = np.linalg.svd(dataMatrix, full_matrices=False)
    
    number = findNumber(S1, level)
    S1[number:] = S1[number:] * 0
    S2 = np.diag(S1)
    
    return np.dot(U, np.dot(S2, V))


dataArray = data.getAll()
a = getSVDRec(dataArray)