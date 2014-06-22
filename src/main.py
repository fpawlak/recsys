# -*- coding: utf-8 -*-
import test
import data as dt
import time


data = dt.getAll()

#test01 = test.svdQuality(data, 200)

t0 = time.time()
test02 = test.svdQuality02(data, testSize = 10, sampleSize = 30)
print 'Czas trwania: ',time.time() - t0

print test02