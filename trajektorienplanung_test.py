# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 12:03:04 2016

@author: Florens Fraidling
"""


import trajektorienplanung as tp
import numpy as np
import matplotlib.pyplot as plt
import robo

#Ausgabe (mit 2 Stellen + folgene 0 unterdrückt)
np.set_printoptions(precision=2, suppress=True)


#Trajektiorien Verlauf berechnen und Plotten

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

#5.1.1. linear
if(status & 0b10000):
    a_lin = tp.linear(q_t0, q_t1, t0, t1)
    print("linear: q(t) = a0 + a1*t\na_lin:",a_lin, "\n")
    
    #linear plotten
    #Gelenkwinkel
    q1 = np.zeros([tt01.size , 6])
    q1[:,0] = a_lin[0] + a_lin[1]*tt01
    q1[:,1] = q_2 
    q1[:,2] = q_3
    q1[:,3] = q_4
    q1[:,4] = q_5
    q1[:,5] = q_6
    
    plt.figure()
    plt.plot(tt01,q1)
    plt.grid(True)
    plt.title("Gelenkwinkel linear")
    plt.ylabel('Gelenkwinkel in Grad')
    plt.xlabel('Zeit in s')
    
    #xyz Koordinaten KUKA KR30HA 
    q_k = np.zeros([1 , 6])
    T = np.zeros([tt01.size])
    i = 0
    xyzrpy = 0
    xyzrpy_lin = np.zeros([tt01.size , 6])
    for q_k in q1 :       
        T = robo.fk_k(q_k)
        xyzrpy_lin[i,:] = robo.T_2_xyzrpy(T)
        i = i+1
    
    plt.figure()
    for i, color in enumerate(['red', 'green', 'blue', 'cyan', 'pink','yellow']):
        plt.plot(tt01,xyzrpy_lin[:,i], color = color)
    plt.grid(True)
    plt.title("Koordinaten KUKA KR30HA linear")
    plt.ylabel('xyz in mm     rpy in grad')
    plt.xlabel('Zeit in s')

#5.1.2. kubisch
if(status & 0b01000):
    a_kub = tp.kubisch(q_t0, q_t1, t0, t1)
    print("kubisch: q(t) = a0 + a1*t + a2*t**2 + a3*t**3 \n a_kub:\n", a_kub, "\n")
    
    #kubisch plotten
    #1.Winkel
    q2 = np.zeros([tt01.size , 6])
    q2[:,0] = a_kub[0] + a_kub[1]*(tt01) + a_kub[2]*(tt01)**2 + a_kub[3]*(tt01)**3
    q2[:,1] = q_2 
    q2[:,2] = q_3
    q2[:,3] = q_4
    q2[:,4] = q_5
    q2[:,5] = q_6
    
    plt.figure()
    plt.plot(tt01,q2)
    plt.grid(True)
    plt.title("Gelenkwinkel kubisch")
    plt.ylabel('Gelenkwinkel')
    plt.xlabel('Time')
    
    #xyz Koordinaten KUKA KR30HA
    q_k = np.zeros([1 , 6])
    T = np.zeros([tt01.size])
    i = 0
    xyzrpy = 0
    xyzrpy_kub = np.zeros([tt01.size , 6])
    for q_k in q2 :       
        T = robo.fk_k(q_k)
        xyzrpy_kub[i,:] = robo.T_2_xyzrpy(T)
        i = i+1
       
    plt.figure()
    for i, color in enumerate(['red', 'green', 'blue', 'cyan', 'pink','yellow']):
        plt.plot(tt01,xyzrpy_kub[:,i], color = color)
    plt.grid(True)
    plt.title("Koordinaten KUKA KR30HA kubisch")
    plt.ylabel('xyz in mm     rpy in Grad')
    plt.xlabel('Zeit in s')
    
    #2. Winkelgeschwindigkeit
    v2 = np.zeros([tt01.size , 6])
    v2[:,0] = a_kub[1] + 2*a_kub[2]*(tt01) + 3*a_kub[3]*(tt01)**2
    v2[:,1] = 0 
    v2[:,2] = 0
    v2[:,3] = 0
    v2[:,4] = 0
    v2[:,5] = 0
    
    plt.figure()
    plt.plot(tt01,v2)
    plt.grid(True)
    plt.title("Winkelgeschwindigkeit kubisch")
    plt.ylabel('Winkelgeschwindigkeit in Grad/s')
    plt.xlabel('Zeit in s')
    
    #2. Winkelbeschleunigung
    a2 = np.zeros([tt01.size , 6])
    a2[:,0] = 2*a_kub[2] + 6*a_kub[3]*(tt01)
    a2[:,1] = 0 
    a2[:,2] = 0
    a2[:,3] = 0
    a2[:,4] = 0
    a2[:,5] = 0
    
    plt.figure()
    plt.plot(tt01,a2)
    plt.grid(True)
    plt.title("Winkelbeschleunigung kubisch")
    plt.ylabel('Winkelbeschleunigung in Grad/s**2')
    plt.xlabel('Zeit in s')

#5.1.3. ordnung5
if(status & 0b00100):
    a_ordnung5 = tp.ordnung5(q_t0, q_t1, v_t0, v_t1, a_t0, a_t1, t0, t1)
    print("Ordnung5: q(t) = a0 + a1*t + ... + a5*t**5\n a_ordung5:\n", a_ordnung5, "\n")
    
    #ordnung5 plotten
    #1. Gelenkwinkel
    q3 = np.zeros([tt01.size , 6])
    q3[:,0] = a_ordnung5[0] + a_ordnung5[1]*tt01 + a_ordnung5[2]*tt01**2 + a_ordnung5[3]*tt01**3 + a_ordnung5[4]*tt01**4 + a_ordnung5[5]*tt01**5 
    q3[:,1] = q_2 
    q3[:,2] = q_3
    q3[:,3] = q_4
    q3[:,4] = q_5
    q3[:,5] = q_6

    plt.figure()
    plt.plot(tt01,q3)
    plt.grid(True)
    plt.title("Gelenkwinkel ordnung5")
    plt.ylabel('Gelenkwinkel in Grad')
    plt.xlabel('Zeit in s')
    
    #xyz KUKA KR30HA
    q_k = np.zeros([1 , 6])
    T = np.zeros([tt01.size])
    i = 0
    xyzrpy = 0
    xyzrpy_ord5 = np.zeros([tt01.size , 6])
    for q_k in q3:       
        T = robo.fk_k(q_k)
        xyzrpy_ord5[i,:] = robo.T_2_xyzrpy(T)
        i = i+1
           
    plt.figure()
    for j, color in enumerate(['red', 'green', 'blue', 'cyan', 'pink','yellow']):
        plt.plot(tt01,xyzrpy_ord5[:,j], color = color)
    plt.grid(True)
    plt.title("Koordinaten KUKA KR30HA ordnung5")
    plt.ylabel('xyz in mm     rpy in Grad')
    plt.xlabel('Zeit in s')
    
    #2. Winkelgeschwindigkeit
    v3 = np.zeros([tt01.size , 6])
    v3[:,0] = a_ordnung5[1] + 2*a_ordnung5[2]*tt01 + 3*a_ordnung5[3]*tt01**2 + 4*a_ordnung5[4]*tt01**3 + 5*a_ordnung5[5]*tt01**4 
    v3[:,1] = 0 
    v3[:,2] = 0
    v3[:,3] = 0
    v3[:,4] = 0
    v3[:,5] = 0

    plt.figure()
    plt.plot(tt01,v3)
    plt.grid(True)
    plt.title("Winkelgeschwindigkeit ordnung5")
    plt.ylabel('Winkelgeschwindigkeit in Grad/s')
    plt.xlabel('Zeit in s')
    
    #3. Winkelbeschleunigung
    a3 = np.zeros([tt01.size , 6])
    a3[:,0] = 2*a_ordnung5[2] + 6*a_ordnung5[3]*tt01 + 12*a_ordnung5[4]*tt01**2 + 20*a_ordnung5[5]*tt01**3 
    a3[:,1] = 0 
    a3[:,2] = 0
    a3[:,3] = 0
    a3[:,4] = 0
    a3[:,5] = 0

    plt.figure()
    plt.plot(tt01,a3)
    plt.grid(True)
    plt.title("Winkelbeschleunigung ordnung5")
    plt.ylabel('Winkelbeschleunigung in Grad/s**2')
    plt.xlabel('Zeit in s')

#5.1.4. kubisch2
if(status & 0b00010):
    a_kub2 = tp.kubisch2(q_t0, q_t1, q_t1, q_t2, t0, t1, t2)
    print("doppelt kubisch: A(t = [t0, t1]), B(t = [t1, t2])\nq_A(t) = a0 + a1*t + a2*t**2 + a3*t**3\nq_B(t) = a4 + a5*t + a6*t**2 + a7*t**3\n a_kub2:\n", a_kub2, "\n") 
  
    #kubisch2 plotten
    #1. Gelenkwinkel
    q4 = np.zeros([tt01.size + tt02.size, 6])
    q4[0:tt01.size,0] = a_kub2[0] + a_kub2[1]*tt01 + a_kub2[2]*tt01**2 + a_kub2[3]*tt01**3
    q4[(tt01.size):(tt01.size + tt02.size),0] = a_kub2[4] + a_kub2[5]*tt02 + a_kub2[6]*tt02**2 + a_kub2[7]*tt02**3
    q4[:,1] = q_2
    q4[:,2] = q_3
    q4[:,3] = q_4
    q4[:,4] = q_5
    q4[:,5] = q_6

    plt.figure()
    plt.plot(td,q4)
    plt.grid(True)
    plt.title("Gelenkwinkel kubisch2")
    plt.ylabel('Gelenkwinkel in Grad')
    plt.xlabel('Zeit in s')
    
    #xyz KUKA KR30HA
    q_k = np.zeros([1 , 6])
    T = np.zeros([td.size])
    i = 0
    xyzrpy = 0
    xyzrpy_kub2 = np.zeros([td.size , 6])
    for q_k in q4 :       
        T = robo.fk_k(q_k)
        xyzrpy_kub2[i,:] = robo.T_2_xyzrpy(T)
        i = i+1
      
    plt.figure()
    for i, color in enumerate(['red', 'green', 'blue', 'cyan', 'pink','yellow']):
        plt.plot(td,xyzrpy_kub2[:,i], color = color)
    plt.grid(True)
    plt.title("Koordinaten KUKA KR30HA kubisch2")
    plt.ylabel('xyz in mm     rpy in Grad')
    plt.xlabel('Zeit in s')
    
    #2. Winkelgeschwindigkeit
    v4 = np.zeros([tt01.size + tt02.size, 6])
    v4[0:tt01.size,0] = a_kub2[1] + 2*a_kub2[2]*tt01 + 3*a_kub2[3]*tt01**2
    v4[(tt01.size):(tt01.size + tt02.size),0] = a_kub2[5] + 2*a_kub2[6]*tt02 + 3*a_kub2[7]*tt02**2
    v4[:,1] = 0
    v4[:,2] = 0
    v4[:,3] = 0
    v4[:,4] = 0
    v4[:,5] = 0

    plt.figure()
    plt.plot(td,v4)
    plt.grid(True)
    plt.title("Winkelgeschwindigkeit kubisch2")
    plt.ylabel('Winkelgeschwindigkeit in Grad/s')
    plt.xlabel('Zeit in s')
    
    #3. Winkelbeschleunigung
    a4 = np.zeros([tt01.size + tt02.size, 6])
    a4[0:tt01.size,0] = 2*a_kub2[2] + 6*a_kub2[3]*tt01
    a4[(tt01.size):(tt01.size + tt02.size),0] = 2*a_kub2[6] + 6*a_kub2[7]*tt02
    a4[:,1] = 0
    a4[:,2] = 0
    a4[:,3] = 0
    a4[:,4] = 0
    a4[:,5] = 0

    plt.figure()
    plt.plot(td,a4)
    plt.grid(True)
    plt.title("Winkelbeschleunigung kubisch2")
    plt.ylabel('Winkelbeschleunigung in Grad/s**2')
    plt.xlabel('Zeit in s')

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

        
        
