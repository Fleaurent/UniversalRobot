# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 12:02:24 2016

@author: Florens Fraidling
"""

import numpy as np
import math
import matplotlib.pyplot as plt


#1. Berechnung t Achse für vMax, aMax, qDiff
def trajektorieQVAtoT(q0, q1, vMax, aMax, ):    

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

def trajektorieQVATtoQT(q0 , q1, vMax, aMax, tS1, tS2, tGes):
    
    tDelta = 1 / 125
    
    qT = tGes / tDelta
    
    return qT

#2. Berechnung t Achse für a, tGes wenn Vorgabe Trapez
def trajektorieTrapez(q0, q1, a, tGes):
    
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