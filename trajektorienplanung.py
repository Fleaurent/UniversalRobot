# -*- coding: utf-8 -*-
"""
toDO: keine Winkeländerung!

"""

import numpy as np
import math
import matplotlib.pyplot as plt
import robolib3 as rl
import os

"""
Teil 1:  Trajektore einzelner Achse
"""

#1. Berechnung Schaltzeitpunkte für qDiff, vMax, aMax einer Achse 
def traj_timestamps(qStart, qTarget, vMax, aMax):    

    qDiff = abs(qTarget - qStart)
    
    qGrenz = (vMax * vMax) / aMax
    #print("qGrenz Rad: ", qGrenz)
    #print("qGrenz Grad: ", qGrenz * 360 / (2 * np.pi))
        
    if qDiff <= qGrenz:
        #Dreieck: tS1 = tS2, tGes
        tS1 =  math.sqrt(qDiff / aMax)
        tS2 = tS1
        tGes = 2 * tS1
        
        #tGes = math.sqrt((4 * qDiff) / aMax)
        #tS1 = tGes/2
        #tS2 = tS1
		
    else:
        #Trapez: tS1, tS2, tGes
        tGes = (vMax / aMax) + (qDiff / vMax)
        tS1 = vMax / aMax
        tS2 = tGes - tS1
    
    return [tS1, tS2, tGes]

def traj_Pose_timestamps(pStart, pTarget, vMax, aMax):
    
    #norm = sqrt(x^2 + y^2 + z^2)
    pDiff = math.sqrt((pStart[0] - pTarget[0])**2 + (pStart[1] - pTarget[1])**2 + (pStart[2] - pTarget[2])**2)
    pGrenz = (vMax * vMax) / aMax
    
    if pDiff <= pGrenz:
        #Dreieck: tS1 = tS2, tGes
        tGes = math.sqrt((4 * pDiff) / aMax)
        tS1 = tGes/2
        tS2 = tS1
		
    else:
        #Trapez: tS1, tS2, tGes
        tGes = (vMax / aMax) + (pDiff / vMax)
        tS1 = vMax / aMax
        tS2 = tGes - tS1
    
    return [tS1, tS2, tGes]


#2. a) Berechnung vNeu, aNeu für vorgegebene Schaltzeitpunkte tS1 + tGes
def traj_getVA(qStart, qTarget, vMax, aMax, tS1, tGes):
    qDiff = abs(qTarget - qStart)
        
    aNeu = qDiff / (tS1 * tGes - tS1**2)
    vNeu = aNeu * tS1
    
    if((aNeu > aMax) or (vNeu > vMax)):
        vNeu = 0
        aNeu = 0
        #handle Error
    
    return [vNeu, aNeu]

#2. b) Berechnung vNeu, aNeu und Schaltzeitpunkte für vorgegebenes tGes (falls tS1 vorgabe nicht erreichbar)
def traj_getVAtimestamps(qStart, qTarget, vMax, aMax, tGes):
    #tGes vorgegeben: vMaxNeu
    qDiff = abs(qTarget - qStart)
    aNeu = aMax
        
    #NAN check!
    try:
        vNeu = (tGes - np.sqrt(tGes*tGes - 4 * qDiff/aMax))/(2/aMax)
    except:
        return [0, 0, 0, 0, 0]
        
    #alternativ
    #tS1 = (tGes * aMax - math.sqrt(tGes * tGes * aMax * aMax - 4 * aMax * qDiff))/ (2 * aMax)
    #vMaxNeu = aMax * tS1
    
    #print("vMaxNeu: ", vMaxNeu)
   
    [tS1, tS2, tGes] = traj_timestamps(qStart, qTarget, vNeu, aNeu)
    #print(tS1, tS2, tGes)
        
        
    return [vNeu, aNeu, tS1, tS2, tGes]


def traj_sample(qStart, qTarget, tS1, tS2, tGes, vMax, aMax, tDelta):
    qDiff = abs(qTarget - qStart)
    
    if(qStart > qTarget):
        aMax = - aMax
        vMax = - vMax
    
    t = np.arange(0, tGes + tDelta, tDelta)
    
    
    qT = np.zeros(t.size)
    vT = np.zeros(t.size)
    aT = np.zeros(t.size)
    
    if(tS1 == tS2):
        print("Dreieck")
        i=0
        
        #Paramter Zeitpunkt tS1
        qTS = qStart + 0.5 * aMax * tS1**2
        vTS = aMax * tS1
        #print(vTS)
        #vTS = np.sqrt(aMax * qDiff)
        #print(vTS)
        
        for ti in t:
            
            if(ti < tS1):
                #Dreieck steigend
                qT[i] = qStart + 0.5 * aMax * ti**2
                vT[i] = aMax * ti
                aT[i] = aMax
            else:
                #Dreieck fallend
                qT[i] = qTS + vTS * (ti - tS1) - 0.5 * aMax * (ti - tS1)**2
                vT[i] = vTS - aMax * (ti - tS1) 
                aT[i] = - aMax
                
            i = i+1
        
        #print(qT)
        
        """
        i = 0
        for i in range(t.size):
            vT[i] = t[i]
        print(vT)
        """
        
    else:
        print("Trapez")
        i = 0
        
        #qTS1 = qStart + 0.5 * aMax * tS1**2
        #qTS2 = qTarget - vMax**2 / (2 * aMax)
        
        qTS1 = vMax**2 / (2 * aMax)
        qTS2 = qTS1 + (tS2 - tS1) * vMax
        
        qDiff = (qTarget - qStart)
        
        for ti in t:
            
            if(ti < tS1):
                #Trapez steigend
                qT[i] = qStart + 0.5 * aMax * ti**2
                vT[i] = aMax * ti
                aT[i] = aMax
                
            elif(ti < tS2):
                #Trapez konst
                qT[i] = qTS1 + (ti - tS1) * vMax
                vT[i] = vMax
                aT[i] = 0
                
            else:
                #Trapez fallend
                qT[i] = qTS2 + (vMax + (aMax * qDiff)/ vMax) * (ti - tS2) - 0.5 * aMax * (ti**2 - tS2**2)
                vT[i] = - aMax * ti + vMax + (aMax * qDiff) / vMax
                aT[i] = - aMax
    
            i = i+1
        
        """
        i=0
        for ti in t:
            qT[i] = ti
            i = i+1
        
       # print(qT)
        
        i = 0
        for i in range(t.size):
            vT[i] = t[i]
        #print(vT)
        """
        
    return[qT, vT, aT, t]

#3. a) berechne Zeitverlauf Dreieck Trajektorie: qT, vT, aT zu sampleZeitpunkten tAB
def traj_sampleDreieck(qStart, qTarget, vMax, aMax, tS, tGes):
    
    tDelta = 1 / 125
    qGrenz = (vMax * vMax) / aMax
    qDiff = qTarget - qStart
    
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
    if(qStart > qTarget):
        aMax = -aMax
    
    qTS = qStart + 0.5 * aMax * tS**2
    vTS = aMax * tS
    
    tAB[0:tA.size] = tA
    tAB[tA.size:tAB.size] = tB
    
    #qtA = 0.5 * aMax * t**2
    #qBT = qTS + vTS * (t - tS) - 0.5 * aMax * (t - tS)**2
    qT[0:tA.size,0] = qStart + 0.5 * aMax * tA**2
    qT[tA.size:tAB.size,0] = qTS + vTS * (tB - tS) - 0.5 * aMax * (tB - tS)**2
    
    
    #vtA = aMax * t
    #vBT = vTS - aMax * t + 
    vT[0:tA.size,0] = aMax * tA
    vT[tA.size:tAB.size,0] = vTS - aMax * (tB - tS) 
    
    aT[0:tA.size,0] = aMax
    aT[tA.size:tAB.size,0] = - aMax
    
    plotTrajektorieAchsen(qT, vT, aT, tAB)
    
#    data = np.zeros([tA.size + tB.size, 3])
#    data[0:tAB.size,0] = qT[0:tAB.size,0]
#    data[0:tAB.size,1] = vT[0:tAB.size,0]
#    data[0:tAB.size,2] = tAB[0:tAB.size,0]
    
    return [qT, vT, aT, tAB]


#3. b) berechne Zeitverlauf Trapez Trajektorie: qT, vT, aT zu sampleZeitpunkten tAC
def traj_sampleTrapez(qStart, qTarget, vMax, aMax, tS1, tS2, tGes):
    
    tDelta = 1 / 125
    qGrenz = (vMax * vMax) / aMax
    qDiff = qTarget - qStart
    
   
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
    if(qStart > qTarget):
        aMax = -aMax
        vMax = -vMax
        
    qTS1 = qStart + 0.5 * aMax * tS1**2
    qTS2 = qTarget - vMax**2 / (2 * aMax)
    
   
    #qtA = 0.5 * aMax * t**2
    #qtB = qTS1 + (t - tS1) * vMax
    #qtC = qTS2 + (vMax + (aMax * qDiff)/ vMax) * (t - tS2) - 0.5 * (t**2 - tS2**2)
    qT[0:tA.size,0] = qStart + 0.5 * aMax * tA**2
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
       
    plotTrajektorieAchsen(qT, vT, aT, tAC)    
    
#    data = np.zeros([tA.size + tB.size + tC.size, 3])
#    data[0:tAC.size,0] = qT[0:tAC.size,0]
#    data[0:tAC.size,1] = vT[0:tAC.size,0]
#    data[0:tAC.size,2] = tAC[0:tAC.size,0]
    
    return [qT, vT, aT, tAC]

"""
def traj_samplePoseDreieck(pStart, pTarget, vMax, aMax, tS, tGes):
    tDelta = 1 / 125
    
    pDiff = math.sqrt((pStart[0] - pTarget[0])**2 + (pStart[1] - pTarget[1])**2 + (pStart[2] - pTarget[2])**2)
    pGrenz = (vMax * vMax) / aMax
    
    tSample = np.arange(0, tGes + tDelta, tDelta)
    
    for ti in tSample:
        if(ti < TS):
            #Steigendes Dreieck
            qStart + 0.5 * aMax * tA**2
        else:
            print("test")
            #fallendes Dreieck
    
    
    
    return [xyzrxryrzT, tAB]
"""
def traj_samplePoseTrapez(qStart, qTarget, vMax, aMax, tS1, tS2, tGes):
    return [xyzrxryrzT, tAC]


#4. Trajektorie direkt aus Vektor plotten
def plotTrajektorieAchsen(qT, vT, aT, t):
    
    c = np.array(['r','g','b','c','magenta','orange'])
    lq = np.array(['q0','q1','q2','q3','q4','q5'])
    lqd = np.array(['qd0','qd1','qd2','qd3','qd4','qd5'])
    lqdd = np.array(['qdd0','qdd1','qdd2','qdd3','qdd4','qdd5'])
    
    plt.figure()
    #plt.plot(t,qT,color=c, label=l)
    try:
        for i in range(6):
            plt.plot(t,qT[:,i],color=c[i],label=lq[i])
    except:
        plt.plot(t,qT,color='r', label='q')
    plt.grid(True)
    plt.title("Gelenkwinkel")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    
    plt.figure()
    try:
        for i in range(6):
            plt.plot(t,vT[:,i],color=c[i],label=lqd[i])
    except:
        plt.plot(t,vT,color='r', label='qd')
    plt.grid(True)
    plt.title("Winkelgeschindigkeit")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    plt.figure()
    try:
        for i in range(6):
            plt.plot(t,aT[:,i],color=c[i],label=lqdd[i])
    except:
        plt.plot(t,aT,color='r', label='qdd')
    plt.grid(True)
    plt.title("Winkelbeschleunigung")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s**2')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    return 0

def plotTrajektoriePose(xyzrxryrz, t):
    
    # plot
    plt.figure()
    try:
        plt.plot(t, xyzrxryrz[:,0], color='r', label='X')
        plt.plot(t, xyzrxryrz[:,1], color='g', label='Y')
        plt.plot(t, xyzrxryrz[:,2], color='b', label='Z')
    except:
        plt.title("Pose XYZ")
        #nothing to do
    plt.grid(True)
    plt.title("Pose XYZ")
    plt.ylabel('XYZ in m')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    
    plt.figure()
    try:
        plt.plot(t, xyzrxryrz[:,3], color='c', label='rx')
        plt.plot(t, xyzrxryrz[:,4], color='magenta', label='ry')
        plt.plot(t, xyzrxryrz[:,5], color='orange', label='rz')
    except:
        plt.title("Pose rxryrz")
        #nothing to do
    plt.grid(True)
    plt.title("Pose rxryrz")
    plt.ylabel('rxryrz in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    return 0


"""
Teil 2: Führungsachse mit synchronen Folgeachsen
"""

def trajektorieFuehrungsachseZeit(qStart, qTarget, vMax, aMax):
    
    tGesFuehrung = 0
    Achse = 0
    Fuehrungsachse = 0 
    
    for Achse in range(qStart.size):
        [tS1Temp, tS2Temp, tGesTemp] = traj_timestamps(qStart[Achse],qTarget[Achse],vMax[Achse],aMax[Achse])
        #print(tQtemp)
        
        if(tGesTemp > tGesFuehrung):
            [tS1Fuehrung, tS2Fuehrung, tGesFuehrung] = [tS1Temp, tS2Temp, tGesTemp]
            Fuehrungsachse = Achse
    
    return [tS1Fuehrung, tS2Fuehrung, tGesFuehrung, Fuehrungsachse]


def trajektorieFuehrungsachseFolgen(qStart, qTarget, vMax, aMax):
    
    vMaxNeu =    np.zeros(qStart.size)
    aMaxNeu =    np.zeros(qStart.size)
    tS1     =    np.zeros(qStart.size)
    tS2     =    np.zeros(qStart.size)
    tGes    =    np.zeros(qStart.size)
    
    #1. Parameter Führungachse == langsamste Achse
    [tS1Fuehrung, tS2Fuehrung, tGesFuehrung, FuehrungsAchse] = trajektorieFuehrungsachseZeit(qStart, qTarget, vMax, aMax)
    
    #cast für Array?
    #FuehrungsAchse = int(Fuehrungsachse)
    
    vMaxNeu[FuehrungsAchse] = vMax[FuehrungsAchse]
    aMaxNeu[FuehrungsAchse] = aMax[FuehrungsAchse]
    tS1[FuehrungsAchse]     = tS1Fuehrung
    tS2[FuehrungsAchse]     = tS2Fuehrung
    tGes[FuehrungsAchse]    = tGesFuehrung
    
    #2. restliche Achsen an Führungsachse anpassen
    Achse = 0
    for Achse in range(qStart.size):
        
        if(Achse != FuehrungsAchse):
            
            [vMaxNeu[Achse],aMaxNeu[Achse]] = traj_getVA(qStart[Achse], qTarget[Achse], vMax[Achse], aMax[Achse], tS1[FuehrungsAchse], tGes[FuehrungsAchse])
            
            if( (vMaxNeu[Achse] == 0) or (aMaxNeu[Achse] == 0) ):
                #Ts1 für Achse nicht umsetzbar! asynchrone Trapeztrajektorie mit neuem tGes
                #[vMaxNeu[Achse], aMaxNeu[Achse], tS1[Achse], tS2[Achse], tGes[Achse]] = traj_getVAtimestamps(qStart[Achse], qTarget[Achse], vMax[Achse], aMax[Achse], tGesFuehrung)

                #keine Winkeländerung
                vMaxNeu[Achse] = 0
                aMaxNeu[Achse] = 0
                tS1[Achse] = tS1[FuehrungsAchse]
                tS2[Achse] = tS2[FuehrungsAchse]
                tGes[Achse] = tGes[FuehrungsAchse]
                    
                print("vaNeu: ",vMaxNeu[Achse], aMaxNeu[Achse], tS1[Achse], tS2[Achse], tGes[Achse])
                
            else:  
                #Zeitbedingung eingehalten: synchrone Trapeztrajektorie mit tS1, tS2, tGes
                tS1[Achse] = tS1[FuehrungsAchse]
                tS2[Achse] = tS2[FuehrungsAchse]
                tGes[Achse] = tGes[FuehrungsAchse]

    
    return [vMaxNeu, aMaxNeu, tS1, tS2, tGes]

def trajektorieZeitvorgabe(qStart, qTarget, vMax, aMax, tGesVorgabe):
    
    vMaxNeu =    np.zeros(qStart.size)
    aMaxNeu =    np.zeros(qStart.size)
    tS1     =    np.zeros(qStart.size)
    tS2     =    np.zeros(qStart.size)
    tGes    =    np.zeros(qStart.size)
    
    #1. Parameter Führungachse == langsamste Achse
    [tS1Fuehrung, tS2Fuehrung, tGesFuehrung, FuehrungsAchse] = trajektorieFuehrungsachseZeit(qStart, qTarget, vMax, aMax)
    
    if(tGesFuehrung > tGesVorgabe):
        #vorgegebenes tGes zu klein
        return [0, 0, 0, 0, 0]
    
    #2.Fuehrungsachse an tGes anpassen
    [vMaxNeu[FuehrungsAchse], aMaxNeu[FuehrungsAchse], tS1[FuehrungsAchse], tS2[FuehrungsAchse], tGes[FuehrungsAchse]] = traj_getVAtimestamps(qStart[FuehrungsAchse], qTarget[FuehrungsAchse], vMax[FuehrungsAchse], aMax[FuehrungsAchse], tGesVorgabe)
    
    
    #3. restliche Achsen an Führungsachse anpassen
    Achse = 0
    for Achse in range(qStart.size):
        
        if(Achse != FuehrungsAchse):
            
            [vMaxNeu[Achse],aMaxNeu[Achse]] = traj_getVA(qStart[Achse], qTarget[Achse], vMax[Achse], aMax[Achse], tS1[FuehrungsAchse], tGes[FuehrungsAchse])
            
            if( (vMaxNeu[Achse] == 0) or (aMaxNeu[Achse] == 0) ):
                #Ts1 für Achse nicht umsetzbar! asynchrone Trapeztrajektorie mit neuem tGes
                #[vMaxNeu[Achse], aMaxNeu[Achse], tS1[Achse], tS2[Achse], tGes[Achse]] = traj_getVAtimestamps(qStart[Achse], qTarget[Achse], vMax[Achse], aMax[Achse], tGesFuehrung)

                #keine Winkeländerung
                vMaxNeu[Achse] = 0
                aMaxNeu[Achse] = 0
                tS1[Achse] = tS1[FuehrungsAchse]
                tS2[Achse] = tS2[FuehrungsAchse]
                tGes[Achse] = tGes[FuehrungsAchse]
                    
                print("vaNeu: ",vMaxNeu[Achse], aMaxNeu[Achse], tS1[Achse], tS2[Achse], tGes[Achse])
                
            else:  
                #Zeitbedingung eingehalten: synchrone Trapeztrajektorie mit tS1, tS2, tGes
                tS1[Achse] = tS1[FuehrungsAchse]
                tS2[Achse] = tS2[FuehrungsAchse]
                tGes[Achse] = tGes[FuehrungsAchse]

    
    return [vMaxNeu, aMaxNeu, tS1, tS2, tGes]


def trajektorieAchsen(qStart, qTarget, vMax, aMax, tS1, tS2, tGes):
    
    tDelta = 1 / 125
    Achse = 0
    
    FuehrungAchse = np.argmax(tGes)

    
    if(tS1[FuehrungAchse] == tS2[FuehrungAchse]):
        
        #Dreieck
        tA = np.arange(0, tS1[FuehrungAchse] + tDelta, tDelta)
        tB = np.arange(tS1[FuehrungAchse] + tDelta, tGes[FuehrungAchse] + tDelta, tDelta)
        
        tAB = np.zeros([tA.size + tB.size])
        tAB[0:tA.size] = tA
        tAB[tA.size:tAB.size] = tB
        
        qT = np.zeros([tAB.size, qStart.size])
        vT = np.zeros([tAB.size, qStart.size])
        aT = np.zeros([tAB.size, qStart.size])
        
        qTS = np.zeros(qStart.size)
        vTS = np.zeros(qStart.size)
        
        #berechne q(t)/v(t) für jede Achse
        for Achse in range(qStart.size):
            
            if(aMax[Achse] == 0 or vMax[Achse] == 0):
                #keine Winkeländerung
                qT[0:tA.size,Achse] = qStart[Achse]
                qT[tA.size:tAB.size,Achse] = qStart[Achse]
                #vT, aT bleiben 0
            
            else:
                
                #Gelenkwinkel steigend/fallend: Vorzeichen nutzen
                if(qStart[Achse] > qTarget[Achse]):
                    aMax[Achse] = -aMax[Achse]
                    
                qTS[Achse] = qStart[Achse] + 0.5 * aMax[Achse] * tS1[Achse]**2
                vTS[Achse] = aMax[Achse] * tS1[Achse]
                
                qT[0:tA.size,Achse] = qStart[Achse] + 0.5 * aMax[Achse] * tA**2
                qT[tA.size:tAB.size,Achse] = qTS[Achse] + vTS[Achse] * (tB - tS1[Achse]) - 0.5 * aMax[Achse] * (tB - tS1[Achse])**2
                
                vT[0:tA.size,Achse] = aMax[Achse] * tA
                vT[tA.size:tAB.size,Achse] = vTS[Achse] - aMax[Achse] * (tB - tS1[Achse])
                
                aT[0:tA.size,Achse] = aMax[Achse]
                aT[tA.size:tAB.size,Achse] = - aMax[Achse]
            
        plotTrajektorieAchsen(qT, vT, aT, tAB)
        
        return [qT, vT, aT, tAB]
        
    else:
        #Trapez
        tA = np.arange(0, tS1[FuehrungAchse] + tDelta, tDelta)
        tB = np.arange(tS1[FuehrungAchse] + tDelta, tS2[FuehrungAchse] + tDelta, tDelta)
        tC = np.arange(tS2[FuehrungAchse] + tDelta, tGes[FuehrungAchse] + tDelta, tDelta)
        
        tACsize = tA.size + tB.size + tC.size
        #print("TAC size: ", tA.size, tB.size, tC.size, tACsize)
                
        tAC = np.zeros([tA.size + tB.size + tC.size])
        tAC[0:tA.size] = tA
        tAC[tA.size:(tA.size + tB.size)] = tB
        tAC[(tA.size + tB.size):tAC.size] = tC
        
        qT = np.zeros([tAC.size, qStart.size])
        vT = np.zeros([tAC.size, qStart.size])
        aT = np.zeros([tAC.size, qStart.size])
        
        qTS1 = np.zeros(qStart.size)
        qTS2 = np.zeros(qStart.size)
        qDiff = np.zeros(qStart.size)
        
        #berechne q,v
        for Achse in range(qStart.size):
            
            if(aMax[Achse] == 0 or vMax[Achse] == 0):
                #keine Winkeländerung
                qT[0:tA.size,Achse] = qStart[Achse]
                qT[tA.size:(tA.size + tB.size),Achse] = qStart[Achse]
                qT[(tA.size + tB.size):tAC.size,Achse] = qStart[Achse]
                #vT, aT bleiben 0
            
            else:
                    
                #Gelenkwinkel steigend/fallend: Vorzeichen nutzen
                if(qStart[Achse] > qTarget[Achse]):
                    aMax[Achse]  = -aMax[Achse] 
                    vMax[Achse]  = -vMax[Achse] 
                
                qDiff[Achse] = qTarget[Achse] - qStart[Achse]
    
                qTS1[Achse] = qStart[Achse] + 0.5 * aMax[Achse] * tS1[Achse]**2
                qTS2[Achse] = qTarget[Achse] - vMax[Achse]**2 / (2 * aMax[Achse])
                
                if(tS1[Achse] == tS1[FuehrungAchse]):
                    
                    qT[0:tA.size,Achse] = qStart[Achse] + 0.5 * aMax[Achse] * tA**2
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
                        
                    qT[0:tAs.size,Achse] = qStart[Achse] + 0.5 * aMax[Achse] * tAs**2
                    qT[tAs.size:(tAs.size + tBs.size),Achse] = qTS1[Achse] + (tBs - tS1[Achse]) * vMax[Achse]
                    qT[(tAs.size + tBs.size):tAC.size,Achse] = qTS2[Achse] + (vMax[Achse] + (aMax[Achse] * qDiff[Achse])/ vMax[Achse]) * (tCs - tS2[Achse]) - 0.5 * aMax[Achse] * (tCs**2 - tS2[Achse]**2)
                    #Problem: different sizes because of rounding
                    
                    vT[0:tAs.size,Achse] = aMax[Achse] * tAs
                    vT[tAs.size:(tAs.size + tBs.size),Achse] = vMax[Achse] 
                    vT[(tAs.size + tBs.size):tAC.size,Achse] = - aMax[Achse] * tCs + vMax[Achse] + (aMax[Achse] * qDiff[Achse]) / vMax[Achse]
                    
                    aT[0:tAs.size,Achse] = aMax[Achse]
                    aT[tAs.size:(tAs.size + tBs.size),Achse] = 0 
                    aT[(tAs.size + tBs.size):tAC.size,Achse] = - aMax[Achse]
                
        plotTrajektorieAchsen(qT, vT, aT, tAC)
       
        return [qT, vT, aT, tAC]
    
    return [0, 0, 0]

def trajektoriePose(qT, t, dhPara):
    xyzrxryrz = np.zeros((t.shape[0],6))
    T = np.zeros((4,4))
    
    print(t.shape[0])
    
    for i in range(t.shape[0]):
         T = rl.fk_ur(dhPara,qT[i,:])
         xyzrxryrz[i] = rl.T_2_rotvec(T)
        
    print(xyzrxryrz[1,:])
    plotTrajektoriePose(xyzrxryrz, t)
    
    return xyzrxryrz

"""
Teil 3: Trapezverlauf mit 25% tGes Beschleunigung
"""

def trajektorie25aMax(qStart, qTarget, vMax, aMax, tGes):
    
    qDiff = abs(qTarget - qStart)
    
    tS1 = tGes / 4
    tS2 = tGes - tS1
    
    aMaxNeu = (qDiff * 16) / ( 3 * tGes**2)
    vMaxNeu = aMaxNeu * tS1 
    
    if((aMaxNeu > aMax) or (vMaxNeu > vMax)):
        vMaxNeu = 0
        aMaxNeu = 0
    
    return [vMaxNeu, aMaxNeu, tS1, tS2]

def trajektorie25Gesamtzeit(qStart,qTarget,vMax,aMax):
    
    qDiff = abs(qTarget - qStart)
    
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

def trajektorieFuehrungsachse25Gesamtzeit(qStart,qTarget,vMax,aMax):
    
    tQFuehrung = np.array([0,0,0])
    Achse = 0
    Fuehrungsachse = 0 
    
    for Achse in range(qStart.size):
        tQtemp = trajektorie25Gesamtzeit(qStart[Achse],qTarget[Achse],vMax[Achse],aMax[Achse])
        #print(tQtemp)
        
        if(tQtemp[2] > tQFuehrung[2]):
            tQFuehrung = tQtemp
            Fuehrungsachse = Achse + 1
    
    tGesFuehrung = tQFuehrung[2]
    
    return [tGesFuehrung, Fuehrungsachse]


def trajektorieFuehrungsachse25(qStart, qTarget, vMax, aMax):
   
    vMaxNeu =    np.zeros(qStart.size)
    aMaxNeu =    np.zeros(qStart.size)
    tS1     =    np.zeros(qStart.size)
    tS2     =    np.zeros(qStart.size)
    tGes    =    np.zeros(qStart.size)
    
    #1. Parameter Führungachse == langsamste Achse
    tQFuehrung = trajektorieFuehrungsachse25Gesamtzeit(qStart, qTarget, vMax, aMax)
    
    tGesFuehrung = tQFuehrung[0]
    
    #2. Achsen an tGes Fuehrungsachse anpassen
    Achse = 0
    for Achse in range(qStart.size):
        vMaxNeu[Achse], aMaxNeu[Achse], tS1[Achse], tS2[Achse] = trajektorie25aMax(qStart[Achse],qTarget[Achse],vMax[Achse],aMax[Achse], tGesFuehrung)
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
    try:
        plt.plot(r.timestamp, r.target_q_0, color='r', label='q0')
        plt.plot(r.timestamp, r.target_q_1, color='g', label='q1')
        plt.plot(r.timestamp, r.target_q_2, color='b', label='q2')
        plt.plot(r.timestamp, r.target_q_3, color='c', label='q3')
        plt.plot(r.timestamp, r.target_q_4, color='magenta', label='q4')
        plt.plot(r.timestamp, r.target_q_5, color='orange', label='q5')
    except:
        plt.title("Gelenkwinkel")
        #nothing to do
    plt.grid(True)
    plt.title("Gelenkwinkel")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_q.png')
    
    
    plt.figure()
    try:
        plt.plot(r.timestamp, r.target_qd_0, color='r', label='qd0')
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
    try:
        plt.plot(r.timestamp, r.target_qdd_0, color='r', label='qdd0')
        plt.plot(r.timestamp, r.target_qdd_1, color='g', label='qdd1')
        plt.plot(r.timestamp, r.target_qdd_2, color='b', label='qdd2')
        plt.plot(r.timestamp, r.target_qdd_3, color='c', label='qdd3')
        plt.plot(r.timestamp, r.target_qdd_4, color='magenta', label='qdd4')
        plt.plot(r.timestamp, r.target_qdd_5, color='orange', label='qdd5')
    except:
        plt.title("Winkelbeschleunigung")
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
def writeCSV(qT, vT, aT, xyzrxryrz, t, filenameCSV):
    #"exampleCsv.csv" # directory relative to script
    
    csv = open('csv/' + filenameCSV, "w")  #open File in write mode
    
    axNum = qT.shape[1]
    
    #print("CSV: ",qT.shape)
    if(axNum == 1):
        csv.write("timestamp target_q_0 target_qd_0 target_qdd_0\n")
    elif(axNum == 6):
        csv.write("timestamp target_q_0 target_q_1 target_q_2 target_q_3 target_q_4 target_q_5 target_qd_0 target_qd_1 target_qd_2 target_qd_3 target_qd_4 target_qd_5 target_qdd_0 target_qdd_1 target_qdd_2 target_qdd_3 target_qdd_4 target_qdd_5 actual_TCP_pose_0 actual_TCP_pose_1 actual_TCP_pose_2 actual_TCP_pose_3 actual_TCP_pose_4 actual_TCP_pose_5\n")
    else:
        return 1

    
    for timestamp in range(t.size):
        
        #1. timestamp
        time = np.float32(t[timestamp])
        csv.write(str(time) + " ")
        
        #2. q_X
        for axis in range(axNum):
            csv.write(str(qT[timestamp,axis]) + " ")
        
        #3. qd_X
        for axis in range(axNum):
            csv.write(str(vT[timestamp,axis]) + " ")
            
        #4. qdd_X
        for axis in range(axNum):
            csv.write(str(aT[timestamp,axis]) + " ")
        
        #5- actual_TCP_pose_X
        for para in range(6):
            csv.write(str(xyzrxryrz[timestamp,para]) + " ")
            
        csv.write("\n")
        
    return 0
