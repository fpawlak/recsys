# -*- coding: utf-8 -*-

import numpy as np
import data as dt


def compFrac(self, numerator, denominator):
    try:
        result = numerator/denominator
    except:
        result = 0

    return result

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
                if nOU >= 1:
                    self.avgDifference[i, j] = tD/nOU

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

        return (numerator, denominator)

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

            if nOU >= 1:
                diff = tD/nOU
                numerator += nOU * (rating + diff)
                denominator += nOU

        return compFrac(numerator, denominator)

    # origMatrix to pierwotna macierz
    # dataMatrix to macierz po przepuszczeniu przez fillMatrix
    # zwraca liste par postaci (i, j, nowa predykcja)
    def modMatrix(self, user, movie, origMatrix, dataMatrix):
        user_index = user - 1
        movie_index = movie - 1

        rating = origMatrix[user_index, movie_index]

        predictions = []

        new_avgD = {}

        user_ratings = d[user]
        (height, _) = user_ratings.shape

        js = []

        im = movie # tak dla wygody
        
        for k in range(0, height):
            jm = user_ratings[k, 0]
            if jm == im:
                continue
            js.append(jm-1)
            tD = self.totalDifference[im, jm] - rating
            new_nOU = self.noOfUsers[im, jm] - 1
            new_avgD[jm] = compFrac(tD, new_nOU)

        # zmieniamy wiersz uzytkownika user:

        for l in range(0, self.moviesNo):
            if l == movie_index:
                numerator = 0
                denominator = 0

                for k in range(0, height):
                    from_movie = user_ratings[k, 0]
                    if from_movie == movie:
                        continue
                    from_rating = user_ratings[k, 1]

                    nOU = self.noOfUsers[movie, from_movie] - 1
                    diff = new_avgD[from_movie]

                    numerator += nOU * (from_rating + diff)
                    denominator += nOU

                prediction = compFrac(numerator, denominator)
                predictions.append(user_index, movie_index, prediction)

                
            else:
                if origMatrix[user_index, l] > 0:
                    continue

                lm = l + 1

                numerator = self.num[user_index, l]
                numerator -= self.noOfUsers[lm, im]*(rating + self.avgDifference[lm, im])
                denominator = self.den[user_index, l]
                denominator -= self.noOfUsers[lm, im]

                prediction = compFrac(numerator, denominator)
                predictions.append(user_index, l, prediction)

        # zmieniamy pozostale wiersze:

        for k in range(0, self.usersNo):
            if k == user_index:
                continue

            if origMatrix[k, movie_index] > 0:
                i_rating = origMatrix[k, movie_index]
                
                for j in js:
                    if origMatrix[k, j] > 0:
                        continue
                        
                    jm = j + 1

                    numerator = self.num[k, j]
                    numerator -= self.noOfUsers[jm, im]*(i_rating + self.avgDifference[jm, im])
                    numerator += (self.noOfUsers[jm, im]-1)*(i_rating + (-new_avgD[jm]))
                    denominator = self.den[k, j] - 1

                    prediction = compFrac(numerator, denominator)
                    predictions.append(k, j, prediction)
                        
            else:
                numerator = self.num[k, movie_index]
                denominator = self.den[k, movie_index]
                
                for j in js:
                    if origMatrix[k, j] == 0:
                        continue

                    j_rating = origMatrix[k, j]                        
                    jm = j + 1
                        
                    numerator -= self.noOfUsers[im, jm]*(j_rating + self.avgDifference[im, jm])
                    numerator += (self.noOfUsers[im, jm]-1)*(j_rating + new_avgD[jm])
                    denominator -= 1

                    
                prediction = compFrac(numerator, denominator)
                predictions.append(k, movie_index, prediction)
                
        return predictions         

    def fillMatrix(self, dataMatrix):
        self.num = np.zeros(shape=(self.usersNo, self.moviesNo))        
        self.den = np.zeros(shape=(self.usersNo, self.moviesNo))
        
        for i in range(0, self.usersNo):
            for j in range(0, self.moviesNo):
                if dataMatrix[i, j] == 0:
                    (numerator, denominator) = self.predict(i+1, j+1)

                    self.num[i, j] = numerator
                    self.den[i, j] = denominator
                    
                    dataMatrix[i, j] = compFrac(numerator, denominator)

# dane = dt.getBase1()
# s = SlopeOne()
# s.setData(dane)
# s.computeDiffs()
# print "policzylem roznice"
# dataMatrix = dt.toDataMatrix(dane)
# s.fillMatrix(dataMatrix)
# np.savetxt('wynik.txt', dataMatrix)
            
