# -*- coding: utf-8 -*-

import svd
import data as dt
import numpy as np


dataBase = dt.getBase1()
dataTest = dt.getTest1()

# recs = svd.getRecommendations(dt.toDataMatrix(dataBase))
# recs = np.loadtxt('txt/u1base.txt')
recs = svd.getRecommendations(np.loadtxt('txt/u1base.txt'))

badScores = 0

size = len(dataTest)

for i in range(size):
    predictedValue = recs[dataTest[i,0], dataTest[i,1]]
    value = dataTest[i,2]
    if abs(value - predictedValue) >= 0.5:
        badScores += 1

quality = (size - badScores)*1.0 / size
print quality
