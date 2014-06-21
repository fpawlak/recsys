# -*- coding: utf-8 -*-

import numpy as np
import data as dt

# Wymaga, zeby dane byly posortowane (po pierwszej, a nastepnie po drugiej
# kolumnie).

class SlopeOne(object):
    def __init__(self):
        self.usersNo = dt.getUsersNo()
        self.moviesNo = dt.getMoviesNo()
        self.totalDifference = np.zeros(shape=(self.moviesNo+1, self.moviesNo+1))
        self.noOfUsers = np.zeros(shape=(self.moviesNo+1, self.moviesNo+1))
        self.avgDifference = np.zeros(shape=(self.moviesNo+1, self.moviesNo+1))        

    def setData(self, data):
        (height, _) = data.shape
        self.d = {}

        user = data[0, 0]
        start = 0

        for i in range(1, height):
            if data[i, 0] != user:
                end = i
                self.d[user] = data[start:end, 1:] 

                start = i
                user = data[i, 0]

        self.d[user] = data[start:height, 1:]

    def computeDiffs(self):
        for (_, ratings) in self.d.iteritems():
            (height, _) = ratings.shape

            for i in range(0, height):
                for j in range(i+1, height):
                    im = ratings[i, 0]
                    ir = ratings[i, 1]
                    jm = ratings[j, 0]
                    jr = ratings[j, 1]
                    self.totalDifference[im, jm] += ir - jr
                    self.noOfUsers[im, jm] += 1

        for i in range(1, self.moviesNo+1):
            # druga wspolrzedna zawsze jest wieksza
            for j in range(i+1, self.moviesNo+1):
                tD = self.totalDifference[i, j]
                nOU = self.noOfUsers[i, j]
                if nOU > 0:
                    self.avgDifference[i, j] = tD/float(nOU)

                # wypelniamy od razu pod przekatna
                self.noOfUsers[j, i] = nOU
                self.totalDifference[j, i] = -tD
                self.avgDifference[j, i] = -self.avgDifference[i, j]
            

    def predict(self, user, movie):
        numerator = 0
        denominator = 0
        
        ratings = self.d[user]
        
        (height, _) = ratings.shape

        for i in range(0, height):
            from_movie = ratings[i, 0]
            rating = ratings[i, 1]

            nOU = self.noOfUsers[movie, from_movie]
            diff = self.avgDifference[movie, from_movie]

            numerator += nOU * (rating + diff)
            denominator += nOU

        if denominator > 0:
            return numerator/denominator
        else:
            return 0

    # "Usuwa" ocene z danych i ja przewiduje.
    def remove_and_predict(self, user, movie):

        numerator = 0
        denominator = 0
        
        ratings = self.d[user]
        
        (height, _) = ratings.shape
        
        for i in range(0, height):
            if ratings[i, 0] == movie:
                movie_rating = ratings[i, 1]
                break

        for i in range(0, height):
            from_movie = ratings[i, 0]

            if from_movie == movie:
                continue
            
            rating = ratings[i, 1]

            nOU = self.noOfUsers[movie, from_movie]
            tD = self.totalDifference[movie, from_movie]

            nOU -= 1
            tD -= movie_rating - rating

            if nOU > 0:
                diff = tD/float(nOU)

            numerator += nOU * (rating + diff)
            denominator += nOU

        if denominator > 0:
            return numerator/denominator
        else:
            return 0            

    def fillMatrix(self, dataMatrix):
        for i in range(0, self.usersNo):
            for j in range(0, self.moviesNo):
                if dataMatrix[i, j] == 0:
                    dataMatrix[i, j] = self.predict(i+1, j+1)

# dane = dt.getBase1()
# s = SlopeOne()
# s.setData(dane)
# s.computeDiffs()
# print "policzylem roznice"
# dataMatrix = dt.toDataMatrix(dane)
# s.fillMatrix(dataMatrix)
# np.savetxt('wynik.txt', dataMatrix)
            
