# -*- coding: utf-8 -*-
"""
Created on Mon May 21 18:34:11 2018

@author: flore
"""

import trajektorienplanung as tp
import numpy as np

t = np.arange(0, 10, 1)
qT = np.zeros([11,6])
vT = np.zeros([11,6])

for timestamp in range(11):
    for Achse in range(6):
        qT[timestamp,Achse] = timestamp + Achse
        vT[timestamp,Achse] = timestamp + Achse

filenameCSV = "csv/exampleCsv.csv"

tp.writeCSV(qT, vT, t, filenameCSV)
tp.plotCSV(filenameCSV)