# -*- coding: utf-8 -*-

import numpy as np
import data as dt
import random

def findNumber(S, level):
#==============================================================================
#     Szuka numeru wartosci wlasnej, po przekroczeniu ktorej suma wszystkich 
#     wiekszych i rownych wartosci wlasnych przekracza ustalony poziom sumy 
#     wszystkich wartosci wlasnych. Poziom nalezy do przedzialu [0,1]).
#==============================================================================

    size = len(S) # liczba wartosci wlasnych
    
    SSum = S.sum() # suma wszystkich wartosci wlasnych
    tmpSum = 0.0
    
    for i in xrange(size):
        tmpSum += S[i]
        if tmpSum / SSum >= level: # sprawdzam czy tymczasowa suma przekracza zadany poziom
            return i
    

def getRecommendations(dataMatrix, level = 0.45):
#==============================================================================
#     Na podstawie danych i zadnego poziomu zwraca dane bez zaszumienia, ktore
#     usuwa SVD.
#==============================================================================
    
    # oblicenie srednich ocen dla kazdego filmu 
    movieMeans = dataMatrix.sum(0) # sumuje wyniki (licznik)
    amount = (dataMatrix != 0).sum(0) # zliczam wystapienia (mianownik)
    
    movieMeans[movieMeans != 0] = movieMeans[movieMeans != 0] / amount[movieMeans != 0] # srednia dla filmow, ktore mialy co najmniej jedna ocene
    movieMeans[movieMeans == 0] = np.mean(dataMatrix[dataMatrix != 0]) # srednia ze wszystkich ocen dla filmow, ktore nie mialy zadnej oceny

    # dodanie brakujacych ocen w postaci srednich
    for i in range(dt.getMoviesNo()):
        dataMatrix[:,i][(dataMatrix[:,i] == 0)] = movieMeans[i]
    
    # SVD
    U, S1, V = np.linalg.svd(dataMatrix, full_matrices=False)
    
    # wyzerowanie wartosci wlasnych mniejszych od pewnej liczby znalezionej na podstawie ustalonego poziomu
    number = findNumber(S1, level)
    S1[number:] = S1[number:] * 0
    S2 = np.diag(S1)

    # powrot do oryginalnego wymiaru
    return np.dot(U, np.dot(S2, V))


def testQuality(data, testSize = 10, level = 0.45):
#==============================================================================
#     Sprawdza jakosc wyciagajac pojedyncze elementy. Zwraca procentowa
#     trafnosc predykcji.
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
        predictData = getRecommendations(dataMatrix, level) # liczymy predykcje
        predictedValue = predictData[row, col] # pobieramy wartosc predykcji dla tej probki

        # sprawdzamy roznice
        if abs(value - predictedValue) >= 0.5:
            badScores += 1

        dataMatrix[row, col] = value # przypisujemy pierwotna wartosc
    
    quality = float(testSize - badScores) / testSize
    return quality