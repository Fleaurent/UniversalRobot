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
qStartA1 = 0
qTargetA1 = np.deg2rad(90)

vMaxA2 = 1.0
#aMaxA2 = 0.1    #Dreieck
aMaxA2 = 1.5    #Trapez   
qStartA2 = 0
qTargetA2 = np.deg2rad(80)

vMaxA3 = 1.5
aMaxA3 = 1.0
qStartA3 = 0
qTargetA3 = np.deg2rad(70)

vMaxA4 = 1.0
aMaxA4 = 1.0
qStartA4 = 0
qTargetA4 = np.deg2rad(60)

vMaxA5 = 1.5
aMaxA5 = 1.5
qStartA5 = 0
qTargetA5 = np.deg2rad(-50)

vMaxA6 = 1.2
aMaxA6 = 1.2
qStartA6 = np.deg2rad(0)
qTargetA6 = np.deg2rad(1)

vMax = np.array([vMaxA1,vMaxA2,vMaxA3,vMaxA4,vMaxA5,vMaxA6])
aMax = np.array([aMaxA1,aMaxA2,aMaxA3,aMaxA4,aMaxA5,aMaxA6])
qStart = np.array([qStartA1,qStartA2,qStartA3,qStartA4,qStartA5,qStartA6])
qTarget = np.array([qTargetA1,qTargetA2,qTargetA3,qTargetA4,qTargetA5,qTargetA6])

print("vMax: \t", vMax)
print("aMax: \t", aMax)
print("qStart: \t", qStart)
print("qTarget: \t", qTarget)


"""
1. Führungsachse Dreieck Trajektorie: qG < qGrenz
"""
aMax[3] = 0.1

tQFuehrung = tp.trajektorieFuehrungsachseZeit(qStart, qTarget, vMax, aMax)
print(tQFuehrung)

[vMaxNeu, aMaxNeu, tS1, tS2, tGes] = tp.trajektorieFuehrungsachseFolgen(qStart, qTarget, vMax, aMax)
print("vMaxNeu \t\t\t aMaxNeu \t\t\t tS1 \t\t\t\t tS2 \t\t\t\t tGes")
print(vMaxNeu, aMaxNeu, tS1, tS2, tGes)

[qT, vT, aT, t] = tp.plotTrajektorieAchsen(qStart, qTarget, vMaxNeu, aMaxNeu, tS1, tS2, tGes)

filenameCSV = "Achsen1Dreieck.csv"
tp.writeCSV(qT, vT, aT, t, filenameCSV)
#tp.plotCSV(filenameCSV)



"""
2. Führungsachse Trapez Trajektorie: qG > qGrenz
"""
aMax[3] = 1.0

[vMaxNeu, aMaxNeu, tS1, tS2, tGes] = tp.trajektorieFuehrungsachseFolgen(qStart, qTarget, vMax, aMax)
print(vMaxNeu, aMaxNeu, tS1, tS2, tGes)

[qT, vT, aT, t] = tp.plotTrajektorieAchsen(qStart, qTarget, vMaxNeu, aMaxNeu, tS1, tS2, tGes)
filenameCSV = "Achsen2Trapez.csv"
tp.writeCSV(qT, vT, aT, t, filenameCSV)
#tp.plotCSV(filenameCSV)

"""
3. Trajektorie 25% Trapezverlauf
"""
aMax[3] = 1.0

[vMaxNeu, aMaxNeu, tS1, tS2, tGes] = tp.trajektorieFuehrungsachse25(qStart, qTarget, vMax, aMax)
print(vMaxNeu, aMaxNeu, tS1, tS2, tGes)

[qT, vT, aT, t] = tp.plotTrajektorieAchsen(qStart, qTarget, vMaxNeu, aMaxNeu, tS1, tS2, tGes)
filenameCSV = "Achsen3Trapez25.csv"
tp.writeCSV(qT, vT, aT, t, filenameCSV)
#tp.plotCSV(filenameCSV)