# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import trajektorienplanung as tp
import robolib3 as rl

#Ausgabe (mit 2 Stellen + folgene 0 unterdrückt)
#np.set_printoptions(precision=3, suppress=True)

#Interpolationstakt
tDelta = 1 / 125

#Trajektiorien Verlauf berechnen und Plotten

#Achsen Parameter
vMaxA1 = 1.04
aMaxA1 = 1.4
q0A1 = 0
q1A1 = np.deg2rad(90)

vMaxA2 = 1.0
#aMaxA2 = 0.1    #Dreieck
aMaxA2 = 1.5    #Trapez   
q0A2 = 0
q1A2 = np.deg2rad(80)

vMaxA3 = 1.5
aMaxA3 = 1.0
q0A3 = 0
q1A3 = np.deg2rad(70)

vMaxA4 = 1.0
aMaxA4 = 1.0
q0A4 = 0
q1A4 = np.deg2rad(60)

vMaxA5 = 1.5
aMaxA5 = 1.5
q0A5 = 0
q1A5 = np.deg2rad(-50)

vMaxA6 = 1.2
aMaxA6 = 1.2
q0A6 = np.deg2rad(0)
q1A6 = np.deg2rad(1)

vMax = np.array([vMaxA1,vMaxA2,vMaxA3,vMaxA4,vMaxA5,vMaxA6])
aMax = np.array([aMaxA1,aMaxA2,aMaxA3,aMaxA4,aMaxA5,aMaxA6])
q0 = np.array([q0A1,q0A2,q0A3,q0A4,q0A5,q0A6])
q1 = np.array([q1A1,q1A2,q1A3,q1A4,q1A5,q1A6])

print("vMax: \t", vMax)
print("aMax: \t", aMax)
print("q0: \t", q0)
print("q1: \t", q1)

"""
1. Führungsachse Dreieck Trajektorie: qG < qGrenz
"""
aMax[3] = 0.1

tQFuehrung = tp.trajektorieFuehrungsachseZeit(q0, q1, vMax, aMax)
print(tQFuehrung)

vMaxNeu, aMaxNeu, tS1, tS2, tGes = tp.trajektorieFuehrungsachseFolgen(q0, q1, vMax, aMax)
print("vMaxNeu \t\t\t aMaxNeu \t\t\t tS1 \t\t\t\t tS2 \t\t\t\t tGes")
print(vMaxNeu, aMaxNeu, tS1, tS2, tGes)

qT, vT, t = tp.plotTrajektorieAchsen(q0, q1, vMaxNeu, aMaxNeu, tS1, tS2, tGes)

filenameCSV = "csv/Achsen1Dreieck.csv"
tp.writeCSV(qT, vT, t, filenameCSV)
#tp.plotCSV(filenameCSV)

"""
2. Führungsachse Trapez Trajektorie: qG > qGrenz
"""
aMax[3] = 1.0

vMaxNeu, aMaxNeu, tS1, tS2, tGes = tp.trajektorieFuehrungsachseFolgen(q0, q1, vMax, aMax)
print(vMaxNeu, aMaxNeu, tS1, tS2, tGes)

qT, vT, t = tp.plotTrajektorieAchsen(q0, q1, vMaxNeu, aMaxNeu, tS1, tS2, tGes)
filenameCSV = "csv/Achsen2Trapez.csv"
tp.writeCSV(qT, vT, t, filenameCSV)
#tp.plotCSV(filenameCSV)

"""
3. Trajektorie 25% Trapezverlauf
"""
aMax[3] = 1.0

vMaxNeu, aMaxNeu, tS1, tS2, tGes = tp.trajektorieFuehrungsachse25(q0, q1, vMax, aMax)
print(vMaxNeu, aMaxNeu, tS1, tS2, tGes)

qT, vT, t = tp.plotTrajektorieAchsen(q0, q1, vMaxNeu, aMaxNeu, tS1, tS2, tGes)
filenameCSV = "csv/Achsen3Trapez25.csv"
tp.writeCSV(qT, vT, t, filenameCSV)
#tp.plotCSV(filenameCSV)