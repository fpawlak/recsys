# -*- coding: utf-8 -*-

import svd
import s1
import random
import data as dt
import numpy as np


def svdS1QualitySingle(data, testSize = 10, level = 0.47):
#==============================================================================
# Sprawdza jakosc SVD wyciagajac pojedyncze elementy.
# Zwraca procentowa trafnosc predykcji.
#==============================================================================

    f = open('svdS1QualitySingle.txt', 'a')
    
    s = s1.SlopeOne()
    s.setData(data)
    s.computeDiffs()
    origMatrix = dt.toDataMatrix(data)
    s.origMatrix = origMatrix
    s.num = np.loadtxt('num.txt')
    s.den = np.loadtxt('den.txt')
    s.dataMatrix = np.loadtxt('macierz-wypelniona.txt')
    
    size = len(data)
    testData = range(0, size)
    random.shuffle(testData)
    
    badScores = 0 # ustawiamy licznik zlej predykcji na zero

    for i in range(size):
        # pobieramy dane o badanej probce
        row = data[testData[i], 0]
        col = data[testData[i], 1]
        value = data[testData[i], 2]
        
        predictData = svd.getRecommendations(s.modMatrix(row, col), level) # liczymy predykcje
        predictedValue = predictData[row-1, col-1] # pobieramy wartosc predykcji dla tej probki

        # sprawdzamy roznice
        
        if abs(value - predictedValue) >= 0.5:
            badScores += 1

        if i % testSize == 0:
            quality = float((i+1) - badScores) / (i+1)
            f.write(str(quality) + '\n')
            f.flush()



def svdQualitySingle(data, testSize = 10, level = 0.47):
#==============================================================================
# Sprawdza jakosc SVD wyciagajac pojedyncze elementy.
# Zwraca procentowa trafnosc predykcji.
#==============================================================================
    f = open('svdQualitySingle.txt', 'a')
    
    size = len(data)
    dataMatrix = dt.toDataMatrix(data)
    testData = range(0, size)
    random.shuffle(testData)
    
    badScores = 0 # ustawiamy licznik zlej predykcji na zero
    
    for i in range(size):
        
        # pobieramy dane o badanej probce
        row = data[testData[i], 0] - 1
        col = data[testData[i], 1] - 1
        value = data[testData[i], 2]
        
        dataMatrix[row, col] = 0 # ustawiamy probke na zero (tak jakby pierowtnie nie bylo tam wyniku)
        predictData = svd.getRecommendations(dataMatrix, level) # liczymy predykcje
        predictedValue = predictData[row, col] # pobieramy wartosc predykcji dla tej probki

        # sprawdzamy roznice
        if abs(value - predictedValue) >= 0.5:
            badScores += 1

        dataMatrix[row, col] = value # przypisujemy pierwotna wartosc

        if i % testSize == 0:
            quality = float((i+1) - badScores) / (i+1)
            f.write(str(quality) + '\n')
            f.flush()


def svdQualityGroups(data, testSize = 10, sampleSize = 25, level = 0.47):
#==============================================================================
#     Sprawdza jakosc SVD wyciagajac pojedyncze elementy (grupami).
#     Zwraca procentowa trafnosc predykcji.
#
#     testSize - liczba probek
#     sampleSize - liczba elementow w probce (tyle elementow jest zerowanych
#                  na raz)
#==============================================================================
    f = open('svdQualityGroups.txt', 'a')
    size = len(data) # wielkosc danych (tutaj: 100k)
    
    if size % sampleSize != 0:
        print 'Parametr sampleSize nie dzieli rowno danych!'
    else:
        
        dataMatrix = dt.toDataMatrix(data)
        testData = range(size)
        random.shuffle(testData)
        testData = np.reshape(testData, [size/sampleSize, sampleSize]) # zmieniamy ich ksztalt tak by byl to array wielkosci testSize x sampleSize
        
        badScores = 0 # ustawiamy licznik zlej predykcji na zero
        
        forSize = size / sampleSize
        for i in range(forSize):
            
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
                
            if i % testSize == 0:
                quality = float(sampleSize * (i+1) - badScores) / ((i+1) * sampleSize)
                f.write(str(quality) + '\n')
                f.flush()
                

def slopeOneQuality(data):
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



def svdQualityGroupsMultiple(data, testSize = 10, sampleSize = 6, levels = [0.38, 0.41, 0.44, 0.47, 0.50, 0.53]):
#==============================================================================
#     Sprawdza jakosc SVD wyciagajac pojedyncze elementy (grupami).
#     Zwraca procentowa trafnosc predykcji.
#     Dla roznych leveli.
#     
#
#     testSize - liczba probek
#     sampleSize - liczba elementow w probce (tyle elementow jest zerowanych
#                  na raz)
#     levels = rozne levele do sprawdzenia, ktory jest najlepszy
#==============================================================================

    overallSize = testSize * sampleSize
    size = len(data) # wielkosc danych (tutaj: 100k)
    
    # sprawdzenie czy liczba sprawdzanych elementow jest niewieksza od liczby elementow
    if overallSize > size:
        print 'Za duza probka! ', testSize, ' * ', sampleSize, ' = ', overallSize, ' > ', size 
        return 0
    else:
        dataMatrix = dt.toDataMatrix(data)
        testData = random.sample(xrange(size), overallSize) # losujemy overallSize probek, ktore poddamy ocenie
        testData = np.reshape(testData, [testSize, sampleSize]) # zmieniamy ich ksztalt tak by byl to array wielkosci testSize x sampleSize
        

        for k in range(len(levels)):
            level = levels[k]
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
            print 'Level = ',level,', jakosc: ',quality
        return quality
        
