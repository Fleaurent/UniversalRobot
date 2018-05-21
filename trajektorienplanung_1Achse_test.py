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

tQ =  tp.trajektorieGesamtzeit(q0, q1, vMax, aMax) 
print("tq: ",tQ)


if(tQ[0] == tQ[1]):
    print("Dreieck")
    qT, vT, t = tp.trajektorieDreieck(q0, q1, vMax, aMax, tQ[0], tQ[2])

else:
    print("Trapez")
    qT, vT, t = tp.trajektorieTrapez(q0, q1, vMax, aMax, tQ[0], tQ[1], tQ[2])
    
#qT, vT, t = tp.plotTrajektorieAchsen(q0, q1, vMax, aMax, tQ[0], tQ[1], tQ[2])

#tp.plotTrajektorie(qT, vT, t)
#filenameCSV = "csv/achse1Dreieck.csv"
#tp.writeCSV(qT, vT, t, filenameCSV)
#tp.plotCSV(filenameCSV)


"""
2. Trapez Trajektorie: deltaQ > qGrenz
"""
q0 = np.deg2rad(-90)
q1 = np.deg2rad(90)

tQ =  tp.trajektorieGesamtzeit(q0, q1, vMax, aMax) 
print("tq: ",tQ)


if(tQ[0] == tQ[1]):
    print("Dreieck")
    qT, vT, t = tp.trajektorieDreieck(q0, q1, vMax, aMax, tQ[0], tQ[2])

else:
    print("Trapez")
    qT, vT, t = tp.trajektorieTrapez(q0, q1, vMax, aMax, tQ[0], tQ[1], tQ[2])
    
#tp.plotTrajektorie(qT, vT, t)
#filenameCSV = "csv/achse2Trapez.csv"
#tp.writeCSV(qT, vT, t, filenameCSV)
#tp.plotCSV(filenameCSV)

"""
3. Trapez Trajektorie: Vorgabe Gesamtzeit Führungsachse #TODO
"""
q0 = np.deg2rad(0)
q1 = np.deg2rad(-90)

#Bsp: Vorgabe Schaltzeiten
tGes = 5

vaNeu = tp.trajektorieVANeutGes(q0, q1, vMax, aMax, tGes)

if((vaNeu[0] == 0) or (vaNeu[1] == 0)):
    print("Winkel in vorgegebener Zeit nicht erreichbar")
    
else:
    if(tQ[0] == tQ[1]):
        print("Dreieck")
        qT, vT, t = tp.trajektorieDreieck(q0, q1, vaNeu[0], vaNeu[1], vaNeu[2], tGes)
    
    else:
        print("Trapez")
        qT, vT, t = tp.trajektorieTrapez(q0, q1, vaNeu[0], vaNeu[1], vaNeu[2], vaNeu[3], tGes)

    #tp.plotTrajektorie(qT, vT, t)
    #filenameCSV = "csv/achse3vaNeu.csv"
    #tp.writeCSV(qT, vT, t, filenameCSV)
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

vaNeu = tp.trajektorieVANeu(q0, q1, vMax, aMax, tS1, tGes)

if((vaNeu[0] == 0) or (vaNeu[1] == 0)):
    print("Winkel in vorgegebener Zeit nicht erreichbar")
    
else:
    if(tQ[0] == tQ[1]):
        print("Dreieck")
        qT, vT, t = tp.trajektorieDreieck(q0, q1, vaNeu[0], vaNeu[1], tS1, tGes)
    
    else:
        print("Trapez")
        qT, vT, t = tp.trajektorieTrapez(q0, q1, vaNeu[0], vaNeu[1], tS1, tS2, tGes)

    #tp.plotTrajektorie(qT, vT, t)
    filenameCSV = "csv/achse4vaNeu.csv"
    tp.writeCSV(qT, vT, t, filenameCSV)
    #tp.plotCSV(filenameCSV)

"""
5. Trapez Trajektorie Symmetrisch: Vorgabe Gesamtzeit Führungsache (25% tGes Beschleunigen)
"""
q0 = np.deg2rad(0)
q1 = np.deg2rad(-100)

#Bsp: Vorgabe Schaltzeiten
tGes = 4

vaNeu = tp.trajektorie25aMax(q0, q1, vMax, aMax, tGes)

if((vaNeu[0] == 0) or (vaNeu[1] == 0)):
    print("Winkel in vorgegebener Zeit nicht erreichbar")
    
else:
    if(tQ[0] == tQ[1]):
        print("Dreieck")
        qT, vT, t = tp.trajektorieDreieck(q0, q1, vaNeu[0], vaNeu[1], tS1, tGes)
    
    else:
        print("Trapez")
        qT, vT, t = tp.trajektorieTrapez(q0, q1, vaNeu[0], vaNeu[1], vaNeu[2], vaNeu[3], tGes)

    #tp.plotTrajektorie(qT, vT, t)
    #filenameCSV = "csv/achse5vaNeu.csv"
    #tp.writeCSV(qT, vT, t, filenameCSV)
    #tp.plotCSV(filenameCSV)

