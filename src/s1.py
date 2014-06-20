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
        self.data = data
        (self.height, _) = data.shape
        self.d = {}

        user = self.data[0, 0]
        start = 0

        for i in range(1, self.height):
            if self.data[i, 0] != user:
                end = i
                self.d[user] = self.data[start:end, 1:] 

                start = i
                user = self.data[i, 0]

        self.d[user] = self.data[start:self.height, 1:]

    def computeDiffs(self):
        for (_, ratings) in self.d.iteritems():
            (rheight, _) = ratings.shape

            for i in range(0, rheight):
                for j in range(i+1, rheight):
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

    def predict(self, user, movie):
        numerator = 0
        denominator = 0
        
        ratings = self.d[user]
        
        (rheight, _) = ratings.shape

        for i in range(0, rheight):
            from_movie = ratings[i, 0]
            rating = ratings[i, 1]

            # diff = ocena(movie) - ocena(from_movie)
            
            if movie > from_movie:
                nOU = self.noOfUsers[from_movie, movie]
                diff = -self.avgDifference[from_movie, movie]
            else:
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
        
        (rheight, _) = ratings.shape

        for i in range(0, rheight):
            if ratings[i, 0] == movie:
                movie_rating = ratings[i, 1]
                break

        for i in range(0, rheight):
            from_movie = ratings[i, 0]

            if from_movie == movie:
                pass
            
            rating = ratings[i, 1]

            # diff = ocena(movie) - ocena(from_movie)
            
            if movie > from_movie:
                nOU = self.noOfUsers[from_movie, movie]
                tD = -self.totalDifference[from_movie, movie]
            else:
                nOU = self.noOfUsers[movie, from_movie]
                tD = self.totalDifference[movie, from_movie]

            nOU -= 1
            tD -= movie_rating - rating

            diff = tD/float(noU)

            numerator += nOU * (rating + diff)
            denominator += nOU

        if denominator > 0:
            return numerator/denominator
        else:
            return 0            

    def fillMatrix(self, dataMatrix):
        (height, width) = dataMatrix.shape

        for i in range(0, height):
            for j in range(0, width):
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
            
