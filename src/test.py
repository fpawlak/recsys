# -*- coding: utf-8 -*-

import svd
import s1
import random
import data as dt
import numpy as np


def svdQuality(data, testSize = 10, sampleSize = 6, level = 0.45):
#==============================================================================
#     Sprawdza jakosc SVD wyciagajac pojedyncze elementy (grupami).
#     Zwraca procentowa trafnosc predykcji.
#
#     testSize - liczba probek
#     sampleSize - liczba elementow w probce (tyle elementow jest zerowanych
#                  na raz)
#==============================================================================

    overallSize = testSize * sampleSize
    size = len(data) # wielkosc danych (tutaj: 100k)
    
    # sprawdzenie czy liczba sprawdzanych elementow jest niewieksza od liczby elementow
    if overallSize > size:
        print 'Za duza probka! ', testSize, ' * ', sampleSize, ' = ', overallSize, ' > ', size 
        return 0
    else:
        dataMatrix = dt.toDataMatrix(data)
        testData = random.sample(xrange(1, size), overallSize) # losujemy overallSize probek, ktore poddamy ocenie
        testData = np.reshape(testData, [testSize, sampleSize]) # zmieniamy ich ksztalt tak by byl to array wielkosci testSize x sampleSize
        
        badScores = 0 # ustawiamy licznik zlej predykcji na zero
        
        for i in range(testSize):
            
            # ustawiamy wsyzstkie probki w grupie na 0 (zero)
            for j in range(sampleSize):
                row =   data[testData[i][j], 0] - 1
                col =   data[testData[i][j], 1] - 1
                dataMatrix[row, col] = 0
                
            predictData = svd.getRecommendations(dataMatrix, level) # liczymy predykcje
            
            # porownujemy wyniki
            for j in range(sampleSize):
                row =   data[testData[i][j], 0] - 1
                col =   data[testData[i][j], 1] - 1
                value = data[testData[i][j], 2]
                predictedValue = predictData[row, col]
                if abs(value - predictedValue) >= 0.5:
                    badScores += 1
                    
                dataMatrix[row, col] = value # ustawiamy na oryginalna wartosc
        
        quality = float(overallSize - badScores) / overallSize
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



