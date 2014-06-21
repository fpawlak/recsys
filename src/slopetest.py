# -*- coding: utf-8 -*-

import data as dt
import numpy as np
from s1 import *

data = dt.getAll()

s = SlopeOne()
s.setData(data)
s.computeDiffs()

badScores = 0
size = len(data)

for i in range(size):
    predictedValue = s.remove_and_predict(data[i, 0], data[i, 1])
    value = data[i, 2]
    if abs(value - predictedValue) >= 0.5:
        badScores += 1

quality = (size - badScores)*1.0 / size
print quality
