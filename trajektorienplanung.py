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

    qGrenz = (vMax * vMax) / aMax
    print("qGrenz Rad: ", qGrenz)
    print("qGrenz Grad: ", qGrenz * 360 / (2 * np.pi))
    qDiff = abs(q1 - q0)
    
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

def trajektorie25aMax(q0, q1, vMax, aMax, tGes):
    
    qDiff = abs(q1 - q0)
    
    tS1 = tGes / 4
    tS2 = tGes - tS1
    
    aMaxNeu = (qDiff * 16) / ( 3 * tGes**2)
    vMaxNeu = aMaxNeu * tS1 
    
    if((aMaxNeu > aMax) or (vMaxNeu > vMax)):
        return np.array([0, 0, 0, 0, 0])
    
    return np.array([vMaxNeu, aMaxNeu, tS1, tS2])

def trajektorieVANeu(q0, q1, vMax, aMax, tS1, tGes):
    #Schaltzeitpunkt tS1: aMaxNeu, vMaxNeu
    qDiff = abs(q1 - q0)
        
    aMaxNeu = qDiff / (tS1 * tGes - tS1**2)
    vMaxNeu = aMaxNeu * tS1
    
    if((aMaxNeu > aMax) or (vMaxNeu > vMax)):
        return np.array[(0, 0)]
    
    return np.array([vMaxNeu, aMaxNeu])

def trajektorieDreieck(q0, q1, vMax, aMax, tS, tGes):
    
    tDelta = 1 / 125
    qGrenz = (vMax * vMax) / aMax
    qDiff = abs(q1 - q0)
    
    if(qDiff > qGrenz):
        #kein Dreieckverlauf
        return 0
    
    tA = np.arange(0, tS + tDelta, tDelta)
    tB = np.arange(tS + tDelta, tGes + tDelta, tDelta)
    
    tAB = np.zeros([tA.size + tB.size, 1])
    tAB[0:tA.size,0] = tA
    tAB[tA.size:tAB.size,0] = tB
    
    qT = np.zeros([tAB.size, 1])
    vT = np.zeros([tAB.size, 1])
    
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
    
    plt.figure()
    plt.plot(tAB,qT)
    plt.grid(True)
    plt.title("Gelenkwinkel Dreieck")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    
    
    plt.figure()
    plt.plot(tAB,vT)
    plt.grid(True)
    plt.title("Winkelgeschindigkeit Dreieck")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s')
    plt.xlabel('Zeit in s')
    
    data = np.zeros([tA.size + tB.size, 3])
    data[0:tAB.size,0] = qT[0:tAB.size,0]
    data[0:tAB.size,1] = vT[0:tAB.size,0]
    data[0:tAB.size,2] = tAB[0:tAB.size,0]
    
    return data

def trajektorieTrapez(q0, q1, vMax, aMax, tS1, tS2, tGes):
    
    tDelta = 1 / 125
    qGrenz = (vMax * vMax) / aMax
    qDiff = abs(q1 - q0)
    
    if(qDiff <= qGrenz):
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
    
    qTS1 = 0.5 * aMax * tS1**2
    qTS2 = qDiff - vMax**2 / (2 * aMax)

   
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
       
    
    plt.figure()
    plt.plot(tAC,qT)
    plt.grid(True)
    plt.title("Gelenkwinkel Trapez")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    
    
    plt.figure()
    plt.plot(tAC,vT)
    plt.grid(True)
    plt.title("Winkelgeschindigkeit Trapez")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s')
    plt.xlabel('Zeit in s')
    
    
    data = np.zeros([tA.size + tB.size + tC.size, 3])
    data[0:tAC.size,0] = qT[0:tAC.size,0]
    data[0:tAC.size,1] = vT[0:tAC.size,0]
    data[0:tAC.size,2] = tAC[0:tAC.size,0]
    
    return data


def trajektorieQVATtoQT(q0 , q1, vMax, aMax, tS1, tS2, tGes):
    
    tDelta = 1 / 125
    
    qT = tGes / tDelta
    
    return qT

#2. Berechnung t Achse für a, tGes wenn Vorgabe Trapez
def trajektorieTrapez2(q0, q1, a, tGes):
    
    qDiff = abs(q1 - q0)
    
    #0. Bedingung für a:
    aMin = ((4 * qDiff) / (tGes * tGes))
    
    if a < aMin:
        #a zu klein um q1 bis t1 zu erreichen
        return np.array([0,0,0,0])
        
    #1. ts berechnen
    tS1 = tGes/2 - ((math.sqrt(a**2 * tGes**2 - 4*a * qDiff))/(2*a))
    tS2 = tGes - tS1
    
    #2. qs aus ts
    qS = 0.5 * a * tS1**2
    qS1 = q0 + qS
    qS2 = q1 - qS
    
    s = np.array([tS1, tS2, qS1, qS2])
    return s

def trajektorieFolgeachse(q0, q1, tS1, tS2, tGes):
    
    qDiff = q1 - q0
    
    
    #2. a Folgeachse berechnen: Dreick oder Trapez?
    if tS1 == tS2:
        #Dreieck
        a = (qDiff)/tS1**2

        qS1 = q0 + (qDiff/2)
        qS2 = qS1
        
    else:
        #Trapez
        a = qDiff/(tS1 * tGes - tS1**2)
    
        qS1 = q0 + 0.5*a*tS1**2
        qS2 = q1 - 0.5*a*tS1**2
     
    return np.array([tS1, tS2 , qS1, qS2, a]) 

"""
#Tajektorienplanung Funktionen




#5.2.2. trapez_folgeachse
def trapez_folgeachse(q0, q1, t_dom, ts1_dom, ts2_dom):
    q_ges = q1 - q0
    
    #1. Parameter dominante Achse übernehmen
    t_ges = t_dom
    ts1 = ts1_dom
    ts2 = ts2_dom
    
    #2. a Folgeachse berechnen: Dreick oder Trapez?
    if ts1 == ts2:
        #Dreieck
        a = (q_ges)/ts1**2

        qs1 = q0 + (q_ges/2)
        qs2 = qs1
        
    else:
        #Trapez
        a = q_ges/(ts1 * t_ges - ts1**2)
    
        qs1 = q0 + 0.5*a*ts1**2
        qs2 = q1 - 0.5*a*ts1**2
    
    s = np.array([ts1, ts2 , qs1, qs2, a]) 
    return s
"""