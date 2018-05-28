# -*- coding: utf-8 -*-

import numpy as np
import trajektorienplanung as tp
import robolib3 as rl

#Ausgabe (mit 2 Stellen + folgene 0 unterdrückt)
np.set_printoptions(precision=3, suppress=True)

#Interpolationstakt
tDelta = 1 / 125

#Trajektiorien Verlauf berechnen und Plotten

#Achse1 Parameter
vMax = 1.04
aMax = 1.4


"""
1. Dreieck Trajektorie: deltaQ < qGrenz
"""
q0 = np.deg2rad(-44.2)
q1 = np.deg2rad(0)

[tS1, tS2, tGes] =  tp.traj_timestamps(q0, q1, vMax, aMax) 
print(tS1, tS2, tGes)


if(tS1 == tS2):
    print("Dreieck")
    [qT, vT, aT, t] = tp.traj_sampleDreieck(q0, q1, vMax, aMax, tS1, tGes)

else:
    print("Trapez")
    [qT, vT, aT, t] = tp.traj_sampleTrapez(q0, q1, vMax, aMax, tS1, tS2, tGes)
    
#qT, vT, t = tp.plotTrajektorieAchsen(q0, q1, vMax, aMax, tQ[0], tQ[1], tQ[2])

#tp.plotTrajektorie(qT, vT, t)
filenameCSV = "csv/achse1Dreieck.csv"
tp.writeCSV(qT, vT, aT, t, filenameCSV)
#tp.plotCSV(filenameCSV)


"""
2. Trapez Trajektorie: deltaQ > qGrenz
"""
q0 = np.deg2rad(-90)
q1 = np.deg2rad(90)

[tS1, tS2, tGes] =  tp.traj_timestamps(q0, q1, vMax, aMax) 
print(tS1, tS2, tGes)


if(tS1 == tS2):
    print("Dreieck")
    [qT, vT, aT, t] = tp.traj_sampleDreieck(q0, q1, vMax, aMax, tS1, tGes)

else:
    print("Trapez")
    [qT, vT, aT, t] = tp.traj_sampleTrapez(q0, q1, vMax, aMax, tS1, tS2, tGes)
    
#tp.plotTrajektorie(qT, vT, aT, t)
filenameCSV = "csv/achse2Trapez.csv"
tp.writeCSV(qT, vT, aT, t, filenameCSV)
#tp.plotCSV(filenameCSV)

"""
3. Trapez Trajektorie: Vorgabe Gesamtzeit Führungsachse #TODO
"""
q0 = np.deg2rad(0)
q1 = np.deg2rad(-90)

#Bsp: Vorgabe Schaltzeiten
tGes = 5

[vNeu, aNeu, tS1, tS2, tGes] = tp.traj_getVAtimestamps(q0, q1, vMax, aMax, tGes)

if((vNeu == 0) or (aNeu == 0)):
    print("Winkel in vorgegebener Zeit nicht erreichbar")
    
else:
    
    if(tS1 == tS2):
        print("Dreieck")
        [qT, vT, aT, t] = tp.traj_sampleDreieck(q0, q1, vNeu, aNeu, tS1, tGes)
    
    else:
        print("Trapez")
        [qT, vT, aT, t] = tp.traj_sampleTrapez(q0, q1, vNeu, aNeu, tS1, tS2, tGes)

    #tp.plotTrajektorie(qT, vT, aT, t)
    filenameCSV = "csv/achse3vaNeu.csv"
    tp.writeCSV(qT, vT, aT, t, filenameCSV)
    #tp.plotCSV(filenameCSV)

"""
4. Trapez Trajektorie: Vorgabe Schaltzeiten von Führungsachse
"""
q0 = np.deg2rad(0)
q1 = np.deg2rad(-30)

#Bsp: Vorgabe Schaltzeiten
tS1 = 1
tS2 = 2
tGes = 3

[vNeu, aNeu] = tp.traj_getVA(q0, q1, vMax, aMax, tS1, tGes)

if((vNeu == 0) or (aNeu == 0)):
    print("Winkel in vorgegebener Zeit nicht erreichbar")
    
else:
    if(tS1 == tS2):
        print("Dreieck")
        [qT, vT, aT, t] = tp.traj_sampleDreieck(q0, q1, vNeu, aNeu, tS1, tGes)
    
    else:
        print("Trapez")
        [qT, vT, aT, t] = tp.traj_sampleTrapez(q0, q1, vNeu, aNeu, tS1, tS2, tGes)

    #tp.plotTrajektorie(qT, vT, aT, t)
    filenameCSV = "csv/achse4vaNeu.csv"
    tp.writeCSV(qT, vT, aT, t, filenameCSV)
    #tp.plotCSV(filenameCSV)

"""
5. Trapez Trajektorie Symmetrisch: Vorgabe Gesamtzeit Führungsache (25% tGes Beschleunigen)
"""
q0 = np.deg2rad(0)
q1 = np.deg2rad(-100)

#Bsp: Vorgabe Schaltzeiten
tGes = 4

[vMaxNeu, aMaxNeu, tS1, tS2] = tp.trajektorie25aMax(q0, q1, vMax, aMax, tGes)

if((vMaxNeu == 0) or (aMaxNeu == 0)):
    print("Winkel in vorgegebener Zeit nicht erreichbar")
    
else:
    print("Trapez25")
    [qT, vT, aT, t] = tp.traj_sampleTrapez(q0, q1, vMaxNeu, aMaxNeu, tS1, tS2, tGes)

    #tp.plotTrajektorie(qT, vT, aT, t)
    filenameCSV = "csv/achse5vaNeu.csv"
    tp.writeCSV(qT, vT, aT, t, filenameCSV)
    #tp.plotCSV(filenameCSV)

