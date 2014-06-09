# -*- coding: utf-8 -*-

import numpy as np


def readIt():
    fileName = '../data/u.data'
    data = np.genfromtxt(fileName)
    return data