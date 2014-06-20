# -*- coding: utf-8 -*-

import numpy as np
import data as dt

def slopeOne(dataMatrix):
    resultMatrix = dataMatrix.copy()
    
    usersNo = dt.getUsersNo()
    moviesNo = dt.getMoviesNo()

    # usersNo = 3
    # moviesNo = 3
    
    # dataMatrix = np.zeros(shape=(usersNo, moviesNo))
    # dataMatrix[0, 0] = 5
    # dataMatrix[0, 1] = 3
    # dataMatrix[0, 2] = 2
    # dataMatrix[1, 0] = 3
    # dataMatrix[1, 1] = 4
    # dataMatrix[2, 1] = 2
    # dataMatrix[2, 2] = 5    

    columns = range(0, moviesNo)

    for i in columns:
        otherColumns = filter(lambda a: a != i, columns)
        
        totalDifference = [0] * moviesNo
        avgDifference = [0] * moviesNo
        noOfUsers = [0] * moviesNo
        
        for j in otherColumns:
            for user in range(0, usersNo):
                ratingI = dataMatrix[user, i]
                ratingJ = dataMatrix[user, j]

                if ratingI > 0 and ratingJ > 0:
                    noOfUsers[j] += 1
                    totalDifference[j] += ratingI - ratingJ

            if(noOfUsers[j] > 0):
                avgDifference[j] = totalDifference[j]/float(noOfUsers[j])

        for user in range(0, usersNo):
            if(dataMatrix[user, i] == 0):
                numerator = 0
                denominator = 0
                
                for j in otherColumns:
                    ratingJ = dataMatrix[user, j]
                    if ratingJ > 0:
                        numerator += noOfUsers[j] * (ratingJ + avgDifference[j])
                        denominator += noOfUsers[j]

                if(denominator > 0):
                    resultMatrix[user, i] = numerator/denominator

    return resultMatrix

# dane = dt.getTest1()
# wynik = slopeOne(dane)
# np.savetxt('wynik.txt', wynik)
            
