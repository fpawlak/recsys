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
#   2. svd z wyciaganiem pojedynczym (dazy do 100%)
#   3. svd z wyciaganiem pojedynczym w grupach (dazy do 100%)
#   4. s1 + svd z wyciaganiem pojedynczym (dazy do 100%)
#   5. test na ustalenie poziomu dla SVD
#
#==============================================================================

###### TEST 1
#==============================================================================
# t0 = time.time()
# test01 = test.slopeOneQuality(data)
# print '\nCzas trwania: ', time.time() - t0
# print 'Wynik: ', test01
#==============================================================================

###### TEST 2
#==============================================================================
# t0 = time.time()
#test.svdQualitySingle(data)
# print '\nCzas trwania: ', time.time() - t0
#==============================================================================

###### TEST 3
#==============================================================================
# t0 = time.time()
# test.svdQualityGroups(data, sampleSize = 100)
# print '\nCzas trwania: ', time.time() - t0
#==============================================================================

###### TEST 4
t0 = time.time()
test.svdS1QualitySingle(data)
print '\nCzas trwania: ', time.time() - t0

###### TEST 5
#==============================================================================
# levels5a = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
# levels5b = [0.35, 0.38, 0.41, 0.44, 0.47, 0.50, 0.53]
# 
# t0 = time.time()
# test05a = test.svdQualityGroupsMultiple(data, testSize = 15, sampleSize = 30, levels = levels5a)
# print '\nCzas trwania: ', time.time() - t0
# print 'Wynik: ', test05a
#     
# t0 = time.time()
# test05b = test.svdQualityGroupsMultiple(data, testSize = 20, sampleSize = 30, levels = levels5b)
# print '\nCzas trwania: ', time.time() - t0
# print 'Wynik: ', test05b
#==============================================================================
    