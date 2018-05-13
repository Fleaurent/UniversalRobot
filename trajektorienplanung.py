# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 12:02:24 2016

@author: Florens Fraidling
"""

import numpy as np
import math
import matplotlib.pyplot as plt


#1. Berechnung t Achse für vMax, aMax, qDiff
def trajektorieGesamtzeit(q0, q1, vMax, aMax):    

    qDiff = abs(q1 - q0)
    
    qGrenz = (vMax * vMax) / aMax
    #print("qGrenz Rad: ", qGrenz)
    #print("qGrenz Grad: ", qGrenz * 360 / (2 * np.pi))
        
    if qDiff <= qGrenz:
        #Dreieck
        tGes = math.sqrt((4 * qDiff) / aMax)
        tS1 = tGes/2
        tS2 = tGes/2
    else:
        #Trapez
        tGes = (vMax / aMax) + (qDiff / vMax)
        tS1 = vMax / aMax
        tS2 = tGes - tS1
     
    return np.array([tS1, tS2, tGes])



def trajektorieVANeutGes(q0, q1, vMax, aMax, tGes):
    #tGes vorgegeben: vMaxNeu
    qDiff = abs(q1 - q0)
    aMaxNeu = aMax
        
    #NAN check!
    vMaxNeu = (tGes - np.sqrt(tGes*tGes - 4 * qDiff/aMax))/(2/aMax)
    #alternativ
    #tS1 = (tGes * aMax - math.sqrt(tGes * tGes * aMax * aMax - 4 * aMax * qDiff))/ (2 * aMax)
    #vMaxNeu = aMax * tS1
    
    #print("vMaxNeu: ", vMaxNeu)
    if((math.isnan(vMaxNeu)) or (vMaxNeu > vMax)):
        vMaxNeu = 0
        aMaxNeu = 0
        tS1 = 0
        tS2 = 0
        tGes = 0
    else:   
        [tS1, tS2, tGes] = trajektorieGesamtzeit(q0, q1, vMaxNeu, aMaxNeu)
        print(tS1, tS2, tGes)
        
        
    return np.array([vMaxNeu, aMaxNeu, tS1, tS2, tGes])


def trajektorieVANeu(q0, q1, vMax, aMax, tS1, tGes):
    #Schaltzeitpunkte tS1 + tGes vorgegeben: aMaxNeu, vMaxNeu
    qDiff = abs(q1 - q0)
        
    aMaxNeu = qDiff / (tS1 * tGes - tS1**2)
    vMaxNeu = aMaxNeu * tS1
    
    if((aMaxNeu > aMax) or (vMaxNeu > vMax)):
        vMaxNeu = 0
        aMaxNeu = 0
        #handle Error
    
    return np.array([vMaxNeu, aMaxNeu])



def trajektorieDreieck(q0, q1, vMax, aMax, tS, tGes):
    
    tDelta = 1 / 125
    qGrenz = (vMax * vMax) / aMax
    qDiff = q1 - q0
    
    if(abs(qDiff) > qGrenz):
        #kein Dreieckverlauf
        return 0
       
    tA = np.arange(0, tS + tDelta, tDelta)
    tB = np.arange(tS + tDelta, tGes + tDelta, tDelta)
    
    tAB = np.zeros([tA.size + tB.size, 1])
    tAB[0:tA.size,0] = tA
    tAB[tA.size:tAB.size,0] = tB
    
    qT = np.zeros([tAB.size, 1])
    vT = np.zeros([tAB.size, 1])
    
    #Gelenkwinkel steigend/fallend: Vorzeichen nutzen
    if(q0 > q1):
        aMax = -aMax
    
    qTS = q0 + 0.5 * aMax * tS**2
    vTS = aMax * tS
    
    tAB[0:tA.size,0] = tA
    tAB[tA.size:tAB.size,0] = tB
    
    #qtA = 0.5 * aMax * t**2
    #qBT = qTS + vTS * (t - tS) - 0.5 * aMax * (t - tS)**2
    qT[0:tA.size,0] = q0 + 0.5 * aMax * tA**2
    qT[tA.size:tAB.size,0] = qTS + vTS * (tB - tS) - 0.5 * aMax * (tB - tS)**2
    
    
    #vtA = aMax * t
    #vBT = vTS - aMax * t + 
    vT[0:tA.size,0] = aMax * tA
    vT[tA.size:tAB.size,0] = vTS - aMax * (tB - tS) 
    
    plotTrajektorie(qT, vT, tAB)
    
#    data = np.zeros([tA.size + tB.size, 3])
#    data[0:tAB.size,0] = qT[0:tAB.size,0]
#    data[0:tAB.size,1] = vT[0:tAB.size,0]
#    data[0:tAB.size,2] = tAB[0:tAB.size,0]
    
    return qT, vT, tAB

def trajektorieTrapez(q0, q1, vMax, aMax, tS1, tS2, tGes):
    
    tDelta = 1 / 125
    qGrenz = (vMax * vMax) / aMax
    qDiff = q1 - q0
    
   
    if(abs(qDiff) <= qGrenz):
        #kein Trapezverlauf
        return 0
            
    tA = np.arange(0, tS1 + tDelta, tDelta)
    tB = np.arange(tS1 + tDelta, tS2 + tDelta, tDelta)
    tC = np.arange(tS2 + tDelta, tGes + tDelta, tDelta)
    
    
    tAC = np.zeros([tA.size + tB.size + tC.size, 1])
    tAC[0:tA.size,0] = tA
    tAC[tA.size:(tA.size + tB.size),0] = tB
    tAC[(tA.size + tB.size):tAC.size,0] = tC
    
    qT = np.zeros([tAC.size, 1])
    vT = np.zeros([tAC.size, 1])
    
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
       
    plotTrajektorie(qT, vT, tAC)    
    
#    data = np.zeros([tA.size + tB.size + tC.size, 3])
#    data[0:tAC.size,0] = qT[0:tAC.size,0]
#    data[0:tAC.size,1] = vT[0:tAC.size,0]
#    data[0:tAC.size,2] = tAC[0:tAC.size,0]
    
    return qT, vT, tA


def trajektorieFuehrungsachseZeit(q0, q1, vMax, aMax):
    
    tQFuehrung = np.array([0,0,0])
    Achse = 0
    Fuehrungsachse = 0 
    
    for Achse in range(q0.size):
        tQtemp = trajektorieGesamtzeit(q0[Achse],q1[Achse],vMax[Achse],aMax[Achse])
        #print(tQtemp)
        
        if(tQtemp[2] > tQFuehrung[2]):
            tQFuehrung = tQtemp
            Fuehrungsachse = Achse + 1
    
    tS1Fuehrung = tQFuehrung[0]
    tS2Fuehrung = tQFuehrung[1]
    tGesFuehrung = tQFuehrung[2]
    
    return np.array([tS1Fuehrung, tS2Fuehrung, tGesFuehrung, Fuehrungsachse])


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
            
            [vMaxNeu[Achse],aMaxNeu[Achse]] = trajektorieVANeu(q0[Achse], q1[Achse], vMax[Achse], aMax[Achse], tS1[FuehrungsAchse], tGes[FuehrungsAchse])
            
            if( (vMaxNeu[Achse] == 0) or (aMaxNeu[Achse] == 0) ):
                #Ts1 für Achse nicht umsetzbar! asynchroner Trapeztrajektorie mit tGes
                [vMaxNeu[Achse], aMaxNeu[Achse], tS1[Achse], tS2[Achse], tGes[Achse]] = trajektorieVANeutGes(q0[Achse], q1[Achse], vMax[Achse], aMax[Achse], tQFuehrung[2])
                print("vaNeu: ",vMaxNeu[Achse], aMaxNeu[Achse], tS1[Achse], tS2[Achse], tGes[Achse])
                
            else:
                #Zeitbedingung eingehalten: synchrone Trapeztrajektorie mit tS1, tS2, tGes
                tS1[Achse] = tS1[FuehrungsAchse]
                tS2[Achse] = tS2[FuehrungsAchse]
                tGes[Achse] = tGes[FuehrungsAchse]

    
    return vMaxNeu, aMaxNeu, tS1, tS2, tGes



def plotTrajektorieAchsen(q0, q1, vMax, aMax, tS1, tS2, tGes):
    
    tDelta = 1 / 125
    Achse = 0
    
    if(tS1[0] == tS2[0]):
        
        #Dreieck
        tA = np.arange(0, tS1[0] + tDelta, tDelta)
        tB = np.arange(tS1[0] + tDelta, tGes[0] + tDelta, tDelta)
        
        tAB = np.zeros([tA.size + tB.size, 1])
        tAB[0:tA.size,0] = tA
        tAB[tA.size:tAB.size,0] = tB
        
        qT = np.zeros([tAB.size, q0.size])
        vT = np.zeros([tAB.size, q0.size])
        
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
            
        plotTrajektorie(qT, vT, tAB)
        return qT, vT, tAB
        
    else:
        #Trapez
        tA = np.arange(0, tS1[0] + tDelta, tDelta)
        tB = np.arange(tS1[0] + tDelta, tS2[0] + tDelta, tDelta)
        tC = np.arange(tS2[0] + tDelta, tGes[0] + tDelta, tDelta)
        
        tACsize = tA.size + tB.size + tC.size
        print("TAC size: ", tA.size, tB.size, tC.size, tACsize)
                
        tAC = np.zeros([tA.size + tB.size + tC.size, 1])
        tAC[0:tA.size,0] = tA
        tAC[tA.size:(tA.size + tB.size),0] = tB
        tAC[(tA.size + tB.size):tAC.size,0] = tC
        
        qT = np.zeros([tAC.size, q0.size])
        vT = np.zeros([tAC.size, q0.size])
        
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
            
        plotTrajektorie(qT, vT, tAC)
        return qT, vT, tAC
    
    return 0, 0, 0

def plotTrajektorie(qT, vT, t):
    
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
    
    return 0


"""
Teil B: Trapezverlauf mit 25% tGes Beschleunigung
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
    
    return np.array([vMaxNeu, aMaxNeu, tS1, tS2])

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
    
    return vMaxNeu, aMaxNeu, tGes

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
    
    return tGesFuehrung, Fuehrungsachse


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
    
    return vMaxNeu, aMaxNeu, tS1, tS2, tGes
