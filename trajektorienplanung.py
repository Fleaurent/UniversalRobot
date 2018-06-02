# -*- coding: utf-8 -*-
"""
toDO: keine Winkeländerung!

"""

import numpy as np
import math
import matplotlib.pyplot as plt
import os

"""
Teil 1:  Trajektore einzelner Achse
"""

#1. Berechnung Schaltzeitpunkte für qDiff, vMax, aMax einer Achse 
def traj_timestamps(q0, q1, vMax, aMax):    

    qDiff = abs(q1 - q0)
    
    qGrenz = (vMax * vMax) / aMax
    #print("qGrenz Rad: ", qGrenz)
    #print("qGrenz Grad: ", qGrenz * 360 / (2 * np.pi))
        
    if qDiff <= qGrenz:
        #Dreieck: tS1 = tS2, tGes
        tGes = math.sqrt((4 * qDiff) / aMax)
        tS1 = tGes/2
        tS2 = tS1
		
    else:
        #Trapez: tS1, tS2, tGes
        tGes = (vMax / aMax) + (qDiff / vMax)
        tS1 = vMax / aMax
        tS2 = tGes - tS1
    
    return [tS1, tS2, tGes]


#2. a) Berechnung vNeu, aNeu für vorgegebene Schaltzeitpunkte tS1 + tGes
def traj_getVA(q0, q1, vMax, aMax, tS1, tGes):
    qDiff = abs(q1 - q0)
        
    aNeu = qDiff / (tS1 * tGes - tS1**2)
    vNeu = aNeu * tS1
    
    if((aNeu > aMax) or (vNeu > vMax)):
        vNeu = 0
        aNeu = 0
        #handle Error
    
    return [vNeu, aNeu]

#2. b) Berechnung vNeu, aNeu und Schaltzeitpunkte für vorgegebenes tGes (falls tS1 vorgabe nicht erreichbar)
def traj_getVAtimestamps(q0, q1, vMax, aMax, tGes):
    #tGes vorgegeben: vMaxNeu
    qDiff = abs(q1 - q0)
    aNeu = aMax
        
    #NAN check!
    vNeu = (tGes - np.sqrt(tGes*tGes - 4 * qDiff/aMax))/(2/aMax)
    #alternativ
    #tS1 = (tGes * aMax - math.sqrt(tGes * tGes * aMax * aMax - 4 * aMax * qDiff))/ (2 * aMax)
    #vMaxNeu = aMax * tS1
    
    #print("vMaxNeu: ", vMaxNeu)
    if((math.isnan(vNeu)) or (vNeu > vMax)):
        vNeu = 0
        aNeu = 0
        tS1 = 0
        tS2 = 0
        tGes = 0
    else:   
        [tS1, tS2, tGes] = traj_timestamps(q0, q1, vNeu, aNeu)
        print(tS1, tS2, tGes)
        
        
    return [vNeu, aNeu, tS1, tS2, tGes]


#3. a) berechne Zeitverlauf Dreieck Trajektorie: qT, vT, aT zu sampleZeitpunkten tAB
def traj_sampleDreieck(q0, q1, vMax, aMax, tS, tGes):
    
    tDelta = 1 / 125
    qGrenz = (vMax * vMax) / aMax
    qDiff = q1 - q0
    
    if(abs(qDiff) > qGrenz):
        #kein Dreieckverlauf
        return 0
       
    tA = np.arange(0, tS + tDelta, tDelta)
    tB = np.arange(tS + tDelta, tGes + tDelta, tDelta)
    
    tAB = np.zeros([tA.size + tB.size])
    tAB[0:tA.size] = tA
    tAB[tA.size:tAB.size] = tB
    
    qT = np.zeros([tAB.size, 1])
    vT = np.zeros([tAB.size, 1])
    aT = np.zeros([tAB.size, 1])
    
    #Gelenkwinkel steigend/fallend: Vorzeichen nutzen
    if(q0 > q1):
        aMax = -aMax
    
    qTS = q0 + 0.5 * aMax * tS**2
    vTS = aMax * tS
    
    tAB[0:tA.size] = tA
    tAB[tA.size:tAB.size] = tB
    
    #qtA = 0.5 * aMax * t**2
    #qBT = qTS + vTS * (t - tS) - 0.5 * aMax * (t - tS)**2
    qT[0:tA.size,0] = q0 + 0.5 * aMax * tA**2
    qT[tA.size:tAB.size,0] = qTS + vTS * (tB - tS) - 0.5 * aMax * (tB - tS)**2
    
    
    #vtA = aMax * t
    #vBT = vTS - aMax * t + 
    vT[0:tA.size,0] = aMax * tA
    vT[tA.size:tAB.size,0] = vTS - aMax * (tB - tS) 
    
    aT[0:tA.size,0] = aMax
    aT[tA.size:tAB.size,0] = - aMax
    
    plotTrajektorie(qT, vT, aT, tAB)
    
#    data = np.zeros([tA.size + tB.size, 3])
#    data[0:tAB.size,0] = qT[0:tAB.size,0]
#    data[0:tAB.size,1] = vT[0:tAB.size,0]
#    data[0:tAB.size,2] = tAB[0:tAB.size,0]
    
    return [qT, vT, aT, tAB]


#3. b) berechne Zeitverlauf Trapez Trajektorie: qT, vT, aT zu sampleZeitpunkten tAC
def traj_sampleTrapez(q0, q1, vMax, aMax, tS1, tS2, tGes):
    
    tDelta = 1 / 125
    qGrenz = (vMax * vMax) / aMax
    qDiff = q1 - q0
    
   
    if(abs(qDiff) <= qGrenz):
        #kein Trapezverlauf
        return 0
            
    tA = np.arange(0, tS1 + tDelta, tDelta)
    tB = np.arange(tS1 + tDelta, tS2 + tDelta, tDelta)
    tC = np.arange(tS2 + tDelta, tGes + tDelta, tDelta)
    
    
    tAC = np.zeros([tA.size + tB.size + tC.size])
    tAC[0:tA.size] = tA
    tAC[tA.size:(tA.size + tB.size)] = tB
    tAC[(tA.size + tB.size):tAC.size] = tC
    
    qT = np.zeros([tAC.size, 1])
    vT = np.zeros([tAC.size, 1])
    aT = np.zeros([tAC.size, 1])
    
    #Gelenkwinkel steigend/fallend: Vorzeichen nutzen
    if(q0 > q1):
        aMax = -aMax
        vMax = -vMax
        
    qTS1 = q0 + 0.5 * aMax * tS1**2
    qTS2 = q1 - vMax**2 / (2 * aMax)
    
   
    #qtA = 0.5 * aMax * t**2
    #qtB = qTS1 + (t - tS1) * vMax
    #qtC = qTS2 + (vMax + (aMax * qDiff)/ vMax) * (t - tS2) - 0.5 * (t**2 - tS2**2)
    qT[0:tA.size,0] = q0 + 0.5 * aMax * tA**2
    qT[tA.size:(tA.size + tB.size),0] = qTS1 + (tB - tS1) * vMax
    qT[(tA.size + tB.size):tAC.size,0] = qTS2 + (vMax + (aMax * qDiff)/ vMax) * (tC - tS2) - 0.5 * aMax * (tC**2 - tS2**2)
    
    #vtA = aMax * t
    #vBT = vMax
    #vCT = - aMax * t + vMax + (aMax * qDiff) / vMax
    vT[0:tA.size,0] = aMax * tA
    vT[tA.size:(tA.size + tB.size),0] = vMax 
    vT[(tA.size + tB.size):tAC.size,0] = - aMax * tC + vMax + (aMax * qDiff) / vMax
    
    aT[0:tA.size,0] = aMax
    aT[tA.size:(tA.size + tB.size),0] = 0 
    aT[(tA.size + tB.size):tAC.size,0] = - aMax
       
    plotTrajektorie(qT, vT, aT, tAC)    
    
#    data = np.zeros([tA.size + tB.size + tC.size, 3])
#    data[0:tAC.size,0] = qT[0:tAC.size,0]
#    data[0:tAC.size,1] = vT[0:tAC.size,0]
#    data[0:tAC.size,2] = tAC[0:tAC.size,0]
    
    return [qT, vT, aT, tAC]


#4. Trajektorie direkt aus Vektor plotten
def plotTrajektorie(qT, vT, aT, t):
    
    plt.figure()
    plt.plot(t,qT)
    plt.grid(True)
    plt.title("Gelenkwinkel")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    
    
    plt.figure()
    plt.plot(t,vT)
    plt.grid(True)
    plt.title("Winkelgeschindigkeit")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s')
    plt.xlabel('Zeit in s')
    
    plt.figure()
    plt.plot(t,aT)
    plt.grid(True)
    plt.title("Winkelbeschleunigung")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s**2')
    plt.xlabel('Zeit in s')
    
    return 0


"""
Teil 2: Führungsachse mit synchronen Folgeachsen
"""

def trajektorieFuehrungsachseZeit(q0, q1, vMax, aMax):
    
    tQFuehrung = np.array([0,0,0])
    Achse = 0
    Fuehrungsachse = 0 
    
    for Achse in range(q0.size):
        tQtemp = traj_timestamps(q0[Achse],q1[Achse],vMax[Achse],aMax[Achse])
        #print(tQtemp)
        
        if(tQtemp[2] > tQFuehrung[2]):
            tQFuehrung = tQtemp
            Fuehrungsachse = Achse + 1
    
    tS1Fuehrung = tQFuehrung[0]
    tS2Fuehrung = tQFuehrung[1]
    tGesFuehrung = tQFuehrung[2]
    
    return [tS1Fuehrung, tS2Fuehrung, tGesFuehrung, Fuehrungsachse]


def trajektorieFuehrungsachseFolgen(q0, q1, vMax, aMax):
    
    vMaxNeu =    np.zeros(q0.size)
    aMaxNeu =    np.zeros(q0.size)
    tS1     =    np.zeros(q0.size)
    tS2     =    np.zeros(q0.size)
    tGes    =    np.zeros(q0.size)
    
    #1. Parameter Führungachse == langsamste Achse
    tQFuehrung = trajektorieFuehrungsachseZeit(q0, q1, vMax, aMax)
    
    FuehrungsAchse = int(tQFuehrung[3] - 1)
    
    vMaxNeu[FuehrungsAchse] = vMax[FuehrungsAchse]
    aMaxNeu[FuehrungsAchse] = aMax[FuehrungsAchse]
    tS1[FuehrungsAchse]     = tQFuehrung[0]
    tS2[FuehrungsAchse]     = tQFuehrung[1]
    tGes[FuehrungsAchse]    = tQFuehrung[2]
    
    #2. restliche Achsen an Führungsachse anpassen
    Achse = 0
    for Achse in range(q0.size):
        
        if(Achse != FuehrungsAchse):
            
            [vMaxNeu[Achse],aMaxNeu[Achse]] = traj_getVA(q0[Achse], q1[Achse], vMax[Achse], aMax[Achse], tS1[FuehrungsAchse], tGes[FuehrungsAchse])
            
            if( (vMaxNeu[Achse] == 0) or (aMaxNeu[Achse] == 0) ):
                #Ts1 für Achse nicht umsetzbar! asynchroner Trapeztrajektorie mit tGes
                [vMaxNeu[Achse], aMaxNeu[Achse], tS1[Achse], tS2[Achse], tGes[Achse]] = traj_getVAtimestamps(q0[Achse], q1[Achse], vMax[Achse], aMax[Achse], tQFuehrung[2])
                print("vaNeu: ",vMaxNeu[Achse], aMaxNeu[Achse], tS1[Achse], tS2[Achse], tGes[Achse])
                
            else:
                #Zeitbedingung eingehalten: synchrone Trapeztrajektorie mit tS1, tS2, tGes
                tS1[Achse] = tS1[FuehrungsAchse]
                tS2[Achse] = tS2[FuehrungsAchse]
                tGes[Achse] = tGes[FuehrungsAchse]

    
    return [vMaxNeu, aMaxNeu, tS1, tS2, tGes]



def plotTrajektorieAchsen(q0, q1, vMax, aMax, tS1, tS2, tGes):
    
    tDelta = 1 / 125
    Achse = 0
    
    if(tS1[0] == tS2[0]):
        
        #Dreieck
        tA = np.arange(0, tS1[0] + tDelta, tDelta)
        tB = np.arange(tS1[0] + tDelta, tGes[0] + tDelta, tDelta)
        
        tAB = np.zeros([tA.size + tB.size])
        tAB[0:tA.size] = tA
        tAB[tA.size:tAB.size] = tB
        
        qT = np.zeros([tAB.size, q0.size])
        vT = np.zeros([tAB.size, q0.size])
        aT = np.zeros([tAB.size, q0.size])
        
        qTS = np.zeros(q0.size)
        vTS = np.zeros(q0.size)
        
        #berechne q(t)/v(t) für jede Achse
        for Achse in range(q0.size):
   
            #Gelenkwinkel steigend/fallend: Vorzeichen nutzen
            if(q0[Achse] > q1[Achse]):
                aMax[Achse] = -aMax[Achse]
                
            qTS[Achse] = q0[Achse] + 0.5 * aMax[Achse] * tS1[Achse]**2
            vTS[Achse] = aMax[Achse] * tS1[Achse]
            
            qT[0:tA.size,Achse] = q0[Achse] + 0.5 * aMax[Achse] * tA**2
            qT[tA.size:tAB.size,Achse] = qTS[Achse] + vTS[Achse] * (tB - tS1[Achse]) - 0.5 * aMax[Achse] * (tB - tS1[Achse])**2
            
            vT[0:tA.size,Achse] = aMax[Achse] * tA
            vT[tA.size:tAB.size,Achse] = vTS[Achse] - aMax[Achse] * (tB - tS1[Achse])
            
            aT[0:tA.size,Achse] = aMax[Achse]
            aT[tA.size:tAB.size,Achse] = - aMax[Achse]
            
        plotTrajektorie(qT, vT, aT, tAB)
        
        return [qT, vT, aT, tAB]
        
    else:
        #Trapez
        tA = np.arange(0, tS1[0] + tDelta, tDelta)
        tB = np.arange(tS1[0] + tDelta, tS2[0] + tDelta, tDelta)
        tC = np.arange(tS2[0] + tDelta, tGes[0] + tDelta, tDelta)
        
        tACsize = tA.size + tB.size + tC.size
        print("TAC size: ", tA.size, tB.size, tC.size, tACsize)
                
        tAC = np.zeros([tA.size + tB.size + tC.size])
        tAC[0:tA.size] = tA
        tAC[tA.size:(tA.size + tB.size)] = tB
        tAC[(tA.size + tB.size):tAC.size] = tC
        
        qT = np.zeros([tAC.size, q0.size])
        vT = np.zeros([tAC.size, q0.size])
        aT = np.zeros([tAC.size, q0.size])
        
        qTS1 = np.zeros(q0.size)
        qTS2 = np.zeros(q0.size)
        qDiff = np.zeros(q0.size)
        
        #berechne q,v
        for Achse in range(q0.size):
            
            #Gelenkwinkel steigend/fallend: Vorzeichen nutzen
            if(q0[Achse] > q1[Achse]):
                aMax[Achse]  = -aMax[Achse] 
                vMax[Achse]  = -vMax[Achse] 
            
            qDiff[Achse] = q1[Achse] - q0[Achse]

            qTS1[Achse] = q0[Achse] + 0.5 * aMax[Achse] * tS1[Achse]**2
            qTS2[Achse] = q1[Achse] - vMax[Achse]**2 / (2 * aMax[Achse])
            
            if(tS1[Achse] == tS1[0]):
                
                qT[0:tA.size,Achse] = q0[Achse] + 0.5 * aMax[Achse] * tA**2
                qT[tA.size:(tA.size + tB.size),Achse] = qTS1[Achse] + (tB - tS1[Achse]) * vMax[Achse]
                qT[(tA.size + tB.size):tAC.size,Achse] = qTS2[Achse] + (vMax[Achse] + (aMax[Achse] * qDiff[Achse])/ vMax[Achse]) * (tC - tS2[Achse]) - 0.5 * aMax[Achse] * (tC**2 - tS2[Achse]**2)
                
                vT[0:tA.size,Achse] = aMax[Achse] * tA
                vT[tA.size:(tA.size + tB.size),Achse] = vMax[Achse] 
                vT[(tA.size + tB.size):tAC.size,Achse] = - aMax[Achse] * tC + vMax[Achse] + (aMax[Achse] * qDiff[Achse]) / vMax[Achse]
                
                aT[0:tA.size,Achse] = aMax[Achse]
                aT[tA.size:(tA.size + tB.size),Achse] = 0
                aT[(tA.size + tB.size):tAC.size,Achse] = - aMax[Achse]
           
            else:
                tCs = 0
                print(tCs)
                
                tAs = np.arange(0, tS1[Achse] + tDelta, tDelta)
                tBs = np.arange(tS1[Achse] + tDelta, tS2[Achse] + tDelta, tDelta)
                tCs = np.arange(tS2[Achse] + tDelta, tGes[Achse], tDelta)
                
                #Problem: different sizes because of rounding
                tACssize = tAs.size + tBs.size + tCs.size
                print("TACs size: ", tAs.size, tBs.size, tCs.size, tACssize)
                
                if(tACssize < tACsize):
                    tCs = np.arange(tS2[Achse] + tDelta, tGes[Achse] + tDelta, tDelta)
                elif(tACssize > tACsize):
                    tCs = np.arange(tS2[Achse] + tDelta, tGes[Achse] - tDelta, tDelta)
                    
                qT[0:tAs.size,Achse] = q0[Achse] + 0.5 * aMax[Achse] * tAs**2
                qT[tAs.size:(tAs.size + tBs.size),Achse] = qTS1[Achse] + (tBs - tS1[Achse]) * vMax[Achse]
                qT[(tAs.size + tBs.size):tAC.size,Achse] = qTS2[Achse] + (vMax[Achse] + (aMax[Achse] * qDiff[Achse])/ vMax[Achse]) * (tCs - tS2[Achse]) - 0.5 * aMax[Achse] * (tCs**2 - tS2[Achse]**2)
                #Problem: different sizes because of rounding
                
                vT[0:tAs.size,Achse] = aMax[Achse] * tAs
                vT[tAs.size:(tAs.size + tBs.size),Achse] = vMax[Achse] 
                vT[(tAs.size + tBs.size):tAC.size,Achse] = - aMax[Achse] * tCs + vMax[Achse] + (aMax[Achse] * qDiff[Achse]) / vMax[Achse]
                
                aT[0:tAs.size,Achse] = aMax[Achse]
                aT[tAs.size:(tAs.size + tBs.size),Achse] = 0 
                aT[(tAs.size + tBs.size):tAC.size,Achse] = - aMax[Achse]
            
        plotTrajektorie(qT, vT, aT, tAC)
       
        return [qT, vT, aT, tAC]
    
    return [0, 0, 0]


"""
Teil 3: Trapezverlauf mit 25% tGes Beschleunigung
"""

def trajektorie25aMax(q0, q1, vMax, aMax, tGes):
    
    qDiff = abs(q1 - q0)
    
    tS1 = tGes / 4
    tS2 = tGes - tS1
    
    aMaxNeu = (qDiff * 16) / ( 3 * tGes**2)
    vMaxNeu = aMaxNeu * tS1 
    
    if((aMaxNeu > aMax) or (vMaxNeu > vMax)):
        vMaxNeu = 0
        aMaxNeu = 0
    
    return [vMaxNeu, aMaxNeu, tS1, tS2]

def trajektorie25Gesamtzeit(q0,q1,vMax,aMax):
    
    qDiff = abs(q1 - q0)
    
    #1. Versuch 25% aMax
    tGes = math.sqrt((qDiff * 16) / (3 * aMax))
    aMaxNeu = aMax
    vMaxNeu = 0.25 * tGes * aMax
        
    #2. Versuch aMaxNeu < aMax --> tGesNeu > tGes
    if(vMaxNeu > vMax):
        tGes = (qDiff * 16) / (12 * vMax)
        aMaxNeu = (qDiff * 16) / (tGes* tGes * 3)
        vMaxNeu = vMax
    
    return [vMaxNeu, aMaxNeu, tGes]

def trajektorieFuehrungsachse25Gesamtzeit(q0,q1,vMax,aMax):
    
    tQFuehrung = np.array([0,0,0])
    Achse = 0
    Fuehrungsachse = 0 
    
    for Achse in range(q0.size):
        tQtemp = trajektorie25Gesamtzeit(q0[Achse],q1[Achse],vMax[Achse],aMax[Achse])
        #print(tQtemp)
        
        if(tQtemp[2] > tQFuehrung[2]):
            tQFuehrung = tQtemp
            Fuehrungsachse = Achse + 1
    
    tGesFuehrung = tQFuehrung[2]
    
    return [tGesFuehrung, Fuehrungsachse]


def trajektorieFuehrungsachse25(q0, q1, vMax, aMax):
   
    vMaxNeu =    np.zeros(q0.size)
    aMaxNeu =    np.zeros(q0.size)
    tS1     =    np.zeros(q0.size)
    tS2     =    np.zeros(q0.size)
    tGes    =    np.zeros(q0.size)
    
    #1. Parameter Führungachse == langsamste Achse
    tQFuehrung = trajektorieFuehrungsachse25Gesamtzeit(q0, q1, vMax, aMax)
    
    tGesFuehrung = tQFuehrung[0]
    
    #2. Achsen an tGes Fuehrungsachse anpassen
    Achse = 0
    for Achse in range(q0.size):
        vMaxNeu[Achse], aMaxNeu[Achse], tS1[Achse], tS2[Achse] = trajektorie25aMax(q0[Achse],q1[Achse],vMax[Achse],aMax[Achse], tGesFuehrung)
        tGes[Achse] = tGesFuehrung
        
        if((vMaxNeu[Achse] == 0) or (aMaxNeu[Achse] == 0)):
            #todo: Fehlerbehandlung: extra Verlauf berechnen
            print("Fehler: 25% nicht möglich für Achse: ", Achse)
    
    return [vMaxNeu, aMaxNeu, tS1, tS2, tGes]



"""
CSV Files
"""
#plotCSV: python2.7
import csv_reader
#target
def plotCSV(filenameCSV):
    
    filename = os.path.splitext(filenameCSV)[0]
    
    with open(('csv/' + filenameCSV)) as csvfile:
        r = csv_reader.CSVReader(csvfile)

    # plot
    plt.figure()
    plt.plot(r.timestamp, r.target_q_0, color='r', label='q0')
    try:
        plt.plot(r.timestamp, r.target_q_1, color='g', label='q1')
        plt.plot(r.timestamp, r.target_q_2, color='b', label='q2')
        plt.plot(r.timestamp, r.target_q_3, color='c', label='q3')
        plt.plot(r.timestamp, r.target_q_4, color='magenta', label='q4')
        plt.plot(r.timestamp, r.target_q_5, color='orange', label='q5')
    except:
        plt.title("Winkelgeschindigkeit")
        #nothing to do
    plt.grid(True)
    plt.title("Gelenkwinkel")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_q.png')
    
    
    plt.figure()
    plt.plot(r.timestamp, r.target_qd_0, color='r', label='qd0')
    try:
        plt.plot(r.timestamp, r.target_qd_1, color='g', label='qd1')
        plt.plot(r.timestamp, r.target_qd_2, color='b', label='qd2')
        plt.plot(r.timestamp, r.target_qd_3, color='c', label='qd3')
        plt.plot(r.timestamp, r.target_qd_4, color='magenta', label='qd4')
        plt.plot(r.timestamp, r.target_qd_5, color='orange', label='qd5')
    except:
        #nothing to do
        plt.title("Winkelgeschindigkeit")
    plt.grid(True)
    plt.title("Winkelgeschindigkeit")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_qd.png')
    
    
    plt.figure()
    plt.plot(r.timestamp, r.target_qdd_0, color='r', label='qdd0')
    try:
        plt.plot(r.timestamp, r.target_qdd_1, color='g', label='qdd1')
        plt.plot(r.timestamp, r.target_qdd_2, color='b', label='qdd2')
        plt.plot(r.timestamp, r.target_qdd_3, color='c', label='qdd3')
        plt.plot(r.timestamp, r.target_qdd_4, color='magenta', label='qdd4')
        plt.plot(r.timestamp, r.target_qdd_5, color='orange', label='qdd5')
    except:
        plt.title("Winkelgeschindigkeit")
        #nothing todo
    plt.grid(True)
    plt.title("Winkelbeschleunigung")
    plt.ylabel('Winkelbeschleunigung in Rad / s**2')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_qdd.png')
    
    return 0

"""
#actual
def plotCSV(filenameCSV):
    filename = os.path.splitext(filenameCSV)[0]

    with open(('csv/' + filenameCSV)) as csvfile:
        r = csv_reader.CSVReader(csvfile)

    # plot
    plt.figure()
    plt.plot(r.timestamp, r.actual_q_0, color='r', label='q0')
    try:
        plt.plot(r.timestamp, r.actual_q_1, color='g', label='q1')
        plt.plot(r.timestamp, r.actual_q_2, color='b', label='q2')
        plt.plot(r.timestamp, r.actual_q_3, color='c', label='q3')
        plt.plot(r.timestamp, r.actual_q_4, color='magenta', label='q4')
        plt.plot(r.timestamp, r.actual_q_5, color='orange', label='q5')
    except:
        plt.title("Winkelgeschindigkeit")
        #nothing to do
    plt.grid(True)
    plt.title("Gelenkwinkel")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_q.png')
    
    
    plt.figure()
    plt.plot(r.timestamp, r.actual_qd_0, color='r', label='qd0')
    try:
        plt.plot(r.timestamp, r.actual_qd_1, color='g', label='qd1')
        plt.plot(r.timestamp, r.actual_qd_2, color='b', label='qd2')
        plt.plot(r.timestamp, r.actual_qd_3, color='c', label='qd3')
        plt.plot(r.timestamp, r.actual_qd_4, color='magenta', label='qd4')
        plt.plot(r.timestamp, r.actual_qd_5, color='orange', label='qd5')
    except:
        #nothing to do
        plt.title("Winkelgeschindigkeit")
    plt.grid(True)
    plt.title("Winkelgeschindigkeit")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_qd.png')
    
    
    plt.figure()
    plt.plot(r.timestamp, r.actual_qdd_0, color='r', label='qdd0')
    try:
        plt.plot(r.timestamp, r.actual_qdd_1, color='g', label='qdd1')
        plt.plot(r.timestamp, r.actual_qdd_2, color='b', label='qdd2')
        plt.plot(r.timestamp, r.actual_qdd_3, color='c', label='qdd3')
        plt.plot(r.timestamp, r.actual_qdd_4, color='magenta', label='qdd4')
        plt.plot(r.timestamp, r.actual_qdd_5, color='orange', label='qdd5')
    except:
        plt.title("Winkelgeschindigkeit")
        #nothing todo
    plt.grid(True)
    plt.title("Winkelbeschleunigung")
    plt.ylabel('Winkelbeschleunigung in Rad / s**2')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_qdd.png')
    
    return 0
"""

#plotPoseCSV: python2.7
def plotPoseCSV(filenameCSV):
    
    filename = os.path.splitext(filenameCSV)[0]
    
    with open(('csv/' + filenameCSV)) as csvfile:
        r = csv_reader.CSVReader(csvfile)

    # plot
    plt.figure()
    try:
        plt.plot(r.timestamp, r.actual_TCP_pose_0, color='r', label='X')
        plt.plot(r.timestamp, r.actual_TCP_pose_1, color='g', label='Y')
        plt.plot(r.timestamp, r.actual_TCP_pose_2, color='b', label='Z')
    except:
        plt.title("Pose XYZ")
        #nothing to do
    plt.grid(True)
    plt.title("Pose XYZ")
    plt.ylabel('XYZ in m')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_XYZ.png')
    
    
    
    plt.figure()
    try:
        plt.plot(r.timestamp, r.actual_TCP_pose_3, color='c', label='rx')
        plt.plot(r.timestamp, r.actual_TCP_pose_4, color='magenta', label='ry')
        plt.plot(r.timestamp, r.actual_TCP_pose_5, color='orange', label='rz')
    except:
        plt.title("Pose rxryrz")
        #nothing to do
    plt.grid(True)
    plt.title("Pose rxryrz")
    plt.ylabel('rxryrz in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_rxryrz.png')
    
    return 0

#nur Python 3.6: größe np.array Problem in 2.7
def writeCSV(qT, vT, aT, t, filenameCSV):
    #"exampleCsv.csv" # directory relative to script
    
    csv = open('csv/' + filenameCSV, "w")  #open File in write mode
    
    axNum = qT.shape[1]
    
    #print("CSV: ",qT.shape)
    if(axNum == 1):
        csv.write("timestamp target_q_0 target_qd_0 target_qdd_0\n")
    elif(axNum == 6):
        csv.write("timestamp target_q_0 target_q_1 target_q_2 target_q_3 target_q_4 target_q_5 target_qd_0 target_qd_1 target_qd_2 target_qd_3 target_qd_4 target_qd_5 target_qdd_0 target_qdd_1 target_qdd_2 target_qdd_3 target_qdd_4 target_qdd_5\n")
    else:
        return 1

    
    for timestamp in range(t.size):
        
        #1. timestamp
        time = np.float32(t[timestamp])
        csv.write(str(time) + " ")
        
        #2. q_x
        for axis in range(axNum):
            csv.write(str(qT[timestamp,axis]) + " ")
        
        #3. qd_x
        for axis in range(axNum):
            csv.write(str(vT[timestamp,axis]) + " ")
            
        #4. qdd_x
        for axis in range(axNum):
            csv.write(str(aT[timestamp,axis]) + " ")
            
        csv.write("\n")
        
    return 0
