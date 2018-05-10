# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 12:03:04 2016

@author: Florens Fraidling
"""

import numpy as np
import matplotlib.pyplot as plt
import trajektorienplanung as tp
import robolib3 as rl

#Ausgabe (mit 2 Stellen + folgene 0 unterdrückt)
np.set_printoptions(precision=2, suppress=True)

#Interpolationstakt
tDelta = 1 / 125

#Trajektiorien Verlauf berechnen und Plotten

#Achse1
vMax = 1.04
aMax = 1.4
q0 = np.deg2rad(0)
#q1 = np.deg2rad(90)
q1 = np.deg2rad(44.2)

tQ =  tp.trajektorieGesamtzeit(q0, q1, vMax, aMax) 
print("tq: ",tQ)


if(tQ[0] == tQ[1]):
    #Dreieck
    print("Dreieck")
    tp.trajektorieDreieck(q0, q1, vMax, aMax, tQ[0], tQ[2])
    #qT = tp.trajektorieQVATtoQT(q0, q1, vMax, aMax, tQ[0], tQ[1], tQ[2])
    print("qT: ", qT)
else:
    #Trapez
    print("Trapez")
    qT = tp.trajektorieQVATtoQT(q0, q1, vMax, aMax, tQ[0], tQ[1], tQ[2])
    print("qT: ", qT)



q0 = np.deg2rad(0)
#q1 = np.deg2rad(90)
q1 = np.deg2rad(90)

tQ =  tp.trajektorieGesamtzeit(q0, q1, vMax, aMax) 
print("tq: ",tQ)


if(tQ[0] == tQ[1]):
    #Dreieck
    print("Dreieck")
    tp.trajektorieDreieck(q0, q1, vMax, aMax, tQ[0], tQ[2])
    #qT = tp.trajektorieQVATtoQT(q0, q1, vMax, aMax, tQ[0], tQ[1], tQ[2])
    print("qT: ", qT)
else:
    #Trapez
    print("Trapez")
    tp.trajektorieTrapez(q0, q1, vMax, aMax, tQ[0], tQ[1], tQ[2])
    #qT = tp.trajektorieQVATtoQT(q0, q1, vMax, aMax, tQ[0], tQ[1], tQ[2])
    print("qT: ", qT)



q0 = np.deg2rad(0)
#q1 = np.deg2rad(90)
q1 = np.deg2rad(90)

#Bsp: Vorgabe Schaltzeiten
tS1 = 1
tS2 = 2
tGes = 3

vaNeu = tp.trajektorieVANeu(q0, q1, vMax, aMax, tS1, tGes)

if(tQ[0] == tQ[1]):
    #Dreieck
    print("Dreieck")
    tp.trajektorieDreieck(q0, q1, vaNeu[0], vaNeu[1], tS1, tGes)
    #qT = tp.trajektorieQVATtoQT(q0, q1, vMax, aMax, tQ[0], tQ[1], tQ[2])
    
else:
    #Trapez
    print("Trapez")
    tp.trajektorieTrapez(q0, q1, vaNeu[0], vaNeu[1], tS1, tS2, tGes)
    #qT = tp.trajektorieQVATtoQT(q0, q1, vMax, aMax, tQ[0], tQ[1], tQ[2])


q0 = np.deg2rad(0)
#q1 = np.deg2rad(90)
q1 = np.deg2rad(90)

#Bsp: Vorgabe Schaltzeiten
tGes = 4

vaNeu = tp.trajektorie25aMax(q0, q1, vMax, aMax, tGes)

if(tQ[0] == tQ[1]):
    #Dreieck
    print("Dreieck")
    tp.trajektorieDreieck(q0, q1, vaNeu[0], vaNeu[1], tS1, tGes)
    #qT = tp.trajektorieQVATtoQT(q0, q1, vMax, aMax, tQ[0], tQ[1], tQ[2])
    
else:
    #Trapez
    print("Trapez")
    tp.trajektorieTrapez(q0, q1, vaNeu[0], vaNeu[1], vaNeu[2], vaNeu[3], tGes)
    #qT = tp.trajektorieQVATtoQT(q0, q1, vMax, aMax, tQ[0], tQ[1], tQ[2])


"""

#1. Auswahl der zu berechnenden Trajektorien über die status Variable
#0bX0000 linear | 0b0X000 kubisch | 0b00X00 ordnung5 | 0b0000 kubisch2 | 0b0000X trapez
status = 0b11111

#2.Eingabewerte: 
#Winkel q_1 über Zeit verändern
q_t0 = 0
q_t1 = 90
q_t2 = 45

#Zeit: t0 < t1 < t2
t0 = 1
t1 = 5
t2 = 10

#Anfangs-/Endbedingungen und Grenzen
v_t0 = 0
v_t1 = 0
a_t0 = 0
a_t1 = 0
a_max = 30
v_max = 30

#Interpolationstakt
delta = 0.01

#q_1 verläuft Trajektorie, Definition der Gelenkwinkel 2-6:
q_2 = -90
q_3 = 90
q_4 = 0
q_5 = 0
q_6 = 0


###################################
# Funktionsaufrufe und Berechnung #
###################################

#Vorberechnungen
#td0 ab 0 
td01 = np.arange(0,(t1-t0)+delta,delta)
td02 = np.arange((t1-t0),(t2-t0)+delta,delta)

#tt0 ab t0
tt01 = np.arange(t0,t1+delta,delta)
tt02 = np.arange(t1,t2+delta,delta)

td = np.zeros([td01.size + td02.size, 1])
td[0:tt01.size,0] = tt01
td[(tt01.size):(tt01.size + tt02.size),0] = tt02    

#1. Funktionsaufrufe: mit Rückgabewerten Trajektorien berechnen
#2. Verlauf plotten

#5.1.5. trapez
if(status & 0b00001):
    t_q = tp.trapez(q_t0, q_t1,a_max,t0, t1)
    if(t_q[0] == t_q[1] == t_q[2] == t_q[3] == 0):
        print("Trapez: a_max zu klein um q_t1 bis t1 zu erreichen!\n")
    else:
        print("Trapez: Übergang Parabel zu Gerade ts12/qs12:\n",t_q, "\n")
    
        ts1 = t_q[0]
        ts2 = t_q[1]
        qs1 = t_q[2]
        qs2 = t_q[3]    
    
        th = (t0 + t1)/2
        qh = (q_t0 + q_t1)/2
        
        #Vorberechnung Zeitabschnitte
        #ttd0: delta/abstand der Zeitpunkte ab 0 (für Berechnungen t_trapez_delta0)
        ttd01 = np.arange(0,ts1 - t0,delta)
        ttd02 = np.arange(0,(ts2 - ts1),delta) 
        ttd03 = np.arange(0,(t1 - ts2) +delta,delta)
        ttd0ges = np.arange(t0,t1 + delta, delta)
        
        #ttt0: Zeitpunkte ab t0 durchgehend (t_trapez_t0)
        ttt01 = np.arange(t0,ts1,delta)
        ttt02 = np.arange(ts1,ts2,delta) 
        ttt03 = np.arange(ts2,t1 +delta,delta)
        ttt0ges = np.arange(t0,t1 + delta, delta)
        
        #ttd:  Zeitinterpolationstakt - Werte für y-Achse eingetragen (t_trapez_delta)
        ttd = np.zeros([ttd01.size + ttd02.size + ttd03.size, 1])
        ttd[0:ttt01.size,0] = ttt01
        ttd[(ttt01.size):(ttt01.size + ttt02.size),0] = ttt02
        ttd[(ttt01.size + ttt02.size):(ttt01.size + ttt02.size + ttt03.size),0] = ttt03
                
        #trapez plotten
        #1. Gelenkwinkel
        q5 = np.zeros([ttd.size , 6])
        #3.1: Parabel t0 bis ts1
        q5[0:ttt01.size,0] = q_t0 + 0.5*a_max*ttd01**2
        #3.2: lin. Steigung ts1 bis ts2
        q5[(ttt01.size):(ttt01.size+ttt02.size),0] = (q_t0 + 0.5*a_max*(ts1 - t0)**2) + (a_max*(ts1 - t0))*ttd02       
        #3.3 abnehmende parabel ts2 bis t1
        q5[(ttt01.size+ttt02.size):(ttt01.size + ttt02.size + ttt03.size),0] = q_t1 - 0.5*a_max*((ts2 - t1) + ttd03)**2
    
        q5[:,1] = q_2
        q5[:,2] = q_3
        q5[:,3] = q_4
        q5[:,4] = q_5
        q5[:,5] = q_6

        plt.figure()
        plt.plot(ttd,q5)
        plt.grid(True)
        plt.title("Gelenkwinkel trapez")
        plt.ylabel('Gelenkwinkel in Grad')
        plt.xlabel('Zeit in s')
    
        #xyz KUKA KR30HA
        q_k = np.zeros([1 , 6])
        T = np.zeros([td.size])
        i = 0
        xyzrpy = 0
        xyzrpy_trap = np.zeros([ttd.size , 6])
        for q_k in q5 :       
            T = robo.fk_k(q_k)
            xyzrpy_trap[i,:] = robo.T_2_xyzrpy(T)
            i = i+1
      
        plt.figure()
        for i, color in enumerate(['red', 'green', 'blue', 'cyan', 'pink','yellow']):
            plt.plot(ttd,xyzrpy_trap[:,i], color = color)
        plt.grid(True)
        plt.title("Koordinaten KUKA KR30HA trapez")
        plt.ylabel('xyz in mm     rpy in Grad')
        plt.xlabel('Zeit ins s')
    
        #2. Winkelgeschwindigkeit
        v5 = np.zeros([ttd.size, 6])
        #3.1: Parabel t0 bis ts1 = lineare Geschwindigkeits zunahme 
        v5[0:ttt01.size,0] = a_max*ttd01
        #3.2: lin. Steigung ts1 bis ts2 = konst. Geschwindigkeit
        v5[(ttt01.size):(ttt01.size+ttt02.size),0] = a_max*(ts1 - t0)       
        #3.3 abnehmende parabel ts2 bis t1 = lineare Geschwindigkeits abnahme 
        v5[(ttt01.size+ttt02.size):(ttt01.size + ttt02.size + ttt03.size),0] = -a_max*((ts2 - t1) + ttd03)
        v5[:,1] = 0
        v5[:,2] = 0
        v5[:,3] = 0
        v5[:,4] = 0
        v5[:,5] = 0
    
        plt.figure()
        plt.plot(ttd,v5)
        plt.grid(True)
        plt.title("Winkelgeschwindigkeit trapez")
        plt.ylabel('Winkelgeschwindigkeit in Grad/s')
        plt.xlabel('Zeit in s')
        
        #3. Winkelbeschleunigung
        a5 = np.zeros([ttd.size, 6])
        #3.1: Parabel t0 bis ts1 = konst. Beschleunigung
        a5[0:ttt01.size,0] = a_max
        #3.2: lin. Steigung ts1 bis ts2 = Beschleunigng 0
        a5[(ttt01.size):(ttt01.size+ttt02.size),0] = 0       
        #3.3 abnehmende parabel ts2 bis t1 0 = - konst. Beschleunigung
        a5[(ttt01.size+ttt02.size):(ttt01.size + ttt02.size + ttt03.size),0] = - a_max
        a5[:,1] = 0
        a5[:,2] = 0
        a5[:,3] = 0
        a5[:,4] = 0
        a5[:,5] = 0
    
        plt.figure()
        plt.plot(ttd,a5)
        plt.grid(True)
        plt.title("Winkelbeschleunigung trapez")
        plt.ylabel('Winkelbeschleunigung in Grad/s**2')
        plt.xlabel('Zeit in s')

"""
        
