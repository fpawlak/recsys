# -*- coding: utf-8 -*-

import numpy as np

def getIt(fileName):
    data = np.genfromtxt(fileName, dtype = int)
    return data[:,:3]

def toDataMatrix(dataArray):
    dataNo = len(dataArray)
    
    dataMatrix = np.zeros(shape=(getUsersNo(), getMoviesNo()))
    
    for i in range(dataNo):
        row = dataArray[i,0]-1
        col = dataArray[i,1]-1
        value = dataArray[i,2]
        dataMatrix[row, col] = value

    return dataMatrix

# cale dane
def getAll():
    return getIt('../data/u.data')


# zbior uczacy nr 1 (80%)
def getBase1():
    return getIt('../data/u1.base')
# zbior testowy nr 1 (20%)
def getTest1():
    return getIt('../data/u1.test')


# zbior uczacy nr 2(80%)
def getBase2():
    return getIt('../data/u2.base')
# zbior testowy nr 2 (20%)
def getTest2():
    return getIt('../data/u2.test')

def getUsersNo():
    return 943

def getMoviesNo():
    return 1682
    
