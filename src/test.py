# -*- coding: utf-8 -*-

import svd
import data as dt

data = dt.getAll()

#recs = svd.getRecommendations(dt.toDataMatrix(dataBase), level = 0.41)
#recs = np.loadtxt('txt/u1base.txt')
#recs = svd.getRecommendations(np.loadtxt('txt/u1base.txt'))


print svd.testQuality(data)
