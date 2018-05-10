# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 12:02:24 2016

@author: Florens Fraidling
"""

import numpy as np
import math
import matplotlib.pyplot as plt

#Tajektorienplanung Funktionen

#5.1.1. linear
def linear(q0, q1, t0, t1):
    
    #1. Winkelgeschwindigkeit = Winkeländerung/delta_zeit
    a1 = (q1 - q0)/(t1-t0)
    #2. Winkel zum Zeitpunkt t=0
    a0 = q0 - a1*t0
    
    a = np.array([a0, a1])
    return a
    
#5.1.2. kubisch    
def kubisch(q0, q1, t0, t1):
    M = np.array([[1,  t0, t0**2,   t0**3],
                  [1, t1, t1**2,   t1**3],
                  [0,  1,   2*t0, 3*t0**2],
                  [0,  1,  2*t1, 3*t1**2]])
    
    q = np.array([q0,q1,0,0])
    
    a = np.linalg.solve(M,q)      
    return a
    
#5.1.3. ordnung5
def ordnung5(q0, q1, v0, v1, a0, a1, t0, t1):
    M = np.array([(1, t0, t0**2,   t0**3,    t0**4,   t0**5),
                  (1, t1, t1**2,   t1**3,    t1**4,    t1**5),
                  (0,   1,  2*t0, 3*t0**2,  4*t0**3,  5*t0**4),
                  (0,   1,  2*t1, 3*t1**2,  4*t1**3,  5*t1**4),
                  (0,   0,      2,    6*t0, 12*t0**2, 20*t0**3),
                  (0,   0,      2,    6*t1, 12*t1**2, 20*t1**3)])
    
    q = np.array([q0, q1, v0, v1, a0, a1])
    
    a = np.linalg.solve(M,q)
    return a
    
#5.1.4. kubisch2
def kubisch2(q0, q1, q2, q3, t0, t1, t2):    
    #LGS aufstellen + lösen: M * a = q    
    M = np.array([(1, t0, t0**2,   t0**3, 0,  0,     0,        0),
                  (1, t1, t1**2,   t1**3, 0,  0,     0,        0),
                  (0,  0,     0,       0, 1, t1, t1**2,    t1**3),
                  (0,  0,     0,       0, 1, t2, t2**2,    t2**3),
                  (0,  1,  2*t0, 3*t0**2, 0,  0,     0,        0),
                  (0,  0,     0,       0, 0,  1,  2*t2,  3*t2**2),
                  (0,  1,  2*t1, 3*t1**2, 0, -1, -2*t1, -3*t1**2),
                  (0,  0,     2,    6*t1, 0,  0,    -2,    -6*t1)])
    
    q = np.array([q0,q1,q2,q3,0,0,0,0])
    
    a = np.linalg.solve(M,q)   
    return a

#5.1.5. trapez
def trapez(q0, q1, a, t0, t1):
    q_d = abs(q1 - q0)
    t_d = t1 - t0
    
    #0. Bedingung für a:
    a_min = ((4*q_d)/t_d**2)
    if a < a_min:
        #a zu klein um q1 bis t1 zu erreichen
        s = np.array([0,0,0,0])
        return s
        
    #1. ts berechnen
    ts = t_d/2 - ((math.sqrt(a**2 * t_d**2 - 4*a * q_d))/(2*a))
    ts1 = t0 + ts
    ts2 = t1 - ts
    
    #2. qs aus ts
    qs = 0.5*a*ts**2
    qs1 = q0 + qs
    qs2 = q1 - qs
    
    s = np.array([ts1, ts2, qs1, qs2])
    return s


#5.2.1. trajektorzeit
def trajektorzeit(v_max, a_max, q0, q1):    
    #maximaler Winkel für Dreieckverlauf
    q_max = v_max**2 / a_max
    
    #Dreick oder Trapez?
    q_d = abs(q1 - q0)
    if q_d <= q_max:
        #Dreieck
        t_ges = math.sqrt(4*q_d / a_max)
        ts1 = t_ges/2
        ts2 = t_ges/2
    else:
        #Trapez
        t_ges = (v_max / a_max) + (q_d / v_max)
        ts1 = v_max/a_max
        ts2 = t_ges - ts1
    
    tq = np.array([t_ges, ts1, ts2])
    return tq

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
