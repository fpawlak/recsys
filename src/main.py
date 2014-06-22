# -*- coding: utf-8 -*-
import test
import data as dt
import time

lev = 0.47
data = dt.getAll()

#==============================================================================
#   --------------------------------------------------
#   ----------------- TESTY --------------------------
#   --------------------------------------------------
#   
#   1. s1 z wycaiganiem pojedynczym (100% danych)
#   2. svd z wyciaganiem pojedynczym (4%)
#   3. svd z wyciaganiem pojedynczym w grupach (100%)
#   4. svd + s1 z wyciaganiem pojedynczym (moze 5%?)
#   5. s1 + svd z wyciaganiem pojedynczym (moze 5%?)
#   6. test na ustalenie poziomu dla SVD
#==============================================================================

t0 = time.time()
test01 = test.slopeOneQuality(data)
print '\nCzas trwania: ', time.time() - t0
print 'Wynik: ', test01

t0 = time.time()
test02 = test.svdQualitySingle(data, testSize = 4000, level = lev) # 1000 to 1.5h
print '\nCzas trwania: ', time.time() - t0
print 'Wynik: ', test02

t0 = time.time()
test03 = test.svdQualityGroups(data, testSize = 33333, sampleSize = 30, level = lev)
print '\nCzas trwania: ', time.time() - t0
print 'Wynik: ', test03


levels6a = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
levels6b = [0.35, 0.38, 0.41, 0.44, 0.47, 0.50, 0.53]

t0 = time.time()
test06a = test.svdQualityGroupsMultiple(data, testSize = 15, sampleSize = 30, levels = levels6a)
print '\nCzas trwania: ', time.time() - t0
print 'Wynik: ', test06a
    
t0 = time.time()
test06b = test.svdQualityGroupsMultiple(data, testSize = 20, sampleSize = 30, levels = levels6b)
print '\nCzas trwania: ', time.time() - t0
print 'Wynik: ', test06b
    