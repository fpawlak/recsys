# -*- coding: utf-8 -*-

import svd
import s1
import random
import data as dt


def svdQuality01(data, testSize = 10, level = 0.45):
#==============================================================================
#     Sprawdza jakosc SVD wyciagajac pojedyncze elementy. 
#     Zwraca procentowa trafnosc predykcji.
#==============================================================================
    size = len(data)
    dataMatrix = dt.toDataMatrix(data)
    testData = random.sample(xrange(1, size), testSize) # losujemy testSize probek, ktore poddamy ocenie
    
    badScores = 0 # ustawiamy licznik zlej predykcji na zero
    
    for i in range(len(testData)):
        
        # pobieramy dane o badanej probce
        row =   data[testData[i], 0] - 1
        col =   data[testData[i], 1] - 1
        value = data[testData[i], 2]
        
        dataMatrix[row, col] = 0 # ustawiamy probke na zero (tak jakby pierowtnie nie bylo tam wyniku)
        predictData = svd.getRecommendations(dataMatrix, level) # liczymy predykcje
        predictedValue = predictData[row, col] # pobieramy wartosc predykcji dla tej probki

        # sprawdzamy roznice
        if abs(value - predictedValue) >= 0.5:
            badScores += 1

        dataMatrix[row, col] = value # przypisujemy pierwotna wartosc
    
    quality = float(testSize - badScores) / testSize
    return quality

  


def slopeOneQuality(data, testSize):
#==============================================================================
#     Sprawdza jakosc SlopeOne wyciagajac pojedyncze elementy. 
#     Zwraca procentowa trafnosc predykcji.
#==============================================================================
    s = s1.SlopeOne()
    s.setData(data)
    s.computeDiffs()

    badScores = 0
    size = len(data)

    for i in range(size):
        predictedValue = s.remove_and_predict(data[i, 0], data[i, 1])
        value = data[i, 2]
        if abs(value - predictedValue) >= 0.5:
            badScores += 1

    quality = float(size - badScores) / size
    return quality



