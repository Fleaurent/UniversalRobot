
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 18:01:27 2017

@author: Florens Fraidling
"""
import trajektorienplanung as tp
import numpy as np
import matplotlib.pyplot as plt


# 5.3.2. Snchrone Achsen Beispiel #
#6 Achsen
achsen = 6
delta = 0.05
#1. Achse
a_max_1 = 3         #Dreieck mit 5  | Trapez mit 3
v_max_1 = 10        #Dreieck mit 20 | Trapez mit 10
q0_1 = 0
q1_1 = 90

#2. Achse
a_max_2 = 3
v_max_2 = 15
q0_2 = 10
q1_2 = 80

#3. Achse
a_max_3 = 3
v_max_3 = 20
q0_3 = 90
q1_3 = 20

#4. Achse
a_max_4 = 2
v_max_4 = 15
q0_4 = 40
q1_4 = 50

#5. Achse
a_max_5 = 5
v_max_5 = 25
q0_5 = 20
q1_5 = 60

#6. Achse
a_max_6 = 9
v_max_6 = 20
q0_6 = 60
q1_6 = 25

#Array anlegen
achsenparameter = np.array([(v_max_1,a_max_1,q0_1,q1_1),
                            (v_max_2,a_max_2,q0_2,q1_2),
                            (v_max_3,a_max_3,q0_3,q1_3),
                            (v_max_4,a_max_4,q0_4,q1_4),
                            (v_max_5,a_max_5,q0_5,q1_5),
                            (v_max_6,a_max_6,q0_6,q1_6)])
print("Achsenparameter: v_max - a_max - q0 - q1\n", achsenparameter)

#1. Trajektorzeit
t_ges = np.zeros([achsen,3])
i = 0
for ti in achsenparameter:
    t_ges[i] = tp.trajektorzeit(ti[0],ti[1],ti[2],ti[3])
    i = i+1
    
print("\nt_ges - ts1 - ts2\n",t_ges)

#dominante Achse bestimmen = größtes t_ges
dom = 0
for i in range(achsen):
    if t_ges[i,0] > t_ges[dom,0]:
        dom = i

print("Dominante Achse: ", dom+1)
t_dom = t_ges[dom,0]
ts1_dom = t_ges[dom,1]
ts2_dom = t_ges[dom,2]

#a folgeachsen bestimmen:
synchron = np.zeros([achsen,5])
i = 0
for s in achsenparameter:
    synchron[i] = tp.trapez_folgeachse(s[2],s[3],t_dom, ts1_dom, ts2_dom)
    i = i+1

print("\nsynchronisiert: ts1 - ts2 - qs1 - qs2 - a \n",synchron)

#plotten
#1. Trapez:
if ts1_dom != ts2_dom:
    print("\nTrapezverlauf:")
    #ttdom 0 bis t_dom 
    ttdom1 = np.arange(0,ts1_dom,delta)
    ttdom2 = np.arange(ts1_dom,ts2_dom,delta)
    ttdom3 = np.arange(ts2_dom, t_dom+delta,delta)

    #td0 von 0
    td01 = np.arange(0,ts1_dom,delta)
    td02 = np.arange(0,(ts2_dom - ts1_dom),delta) 
    td03 = np.arange(0,(t_dom - ts2_dom) + delta,delta)

    td = np.zeros([ttdom1.size + ttdom2.size + ttdom3.size, 1])
    td[0:ttdom1.size,0] = ttdom1
    td[(ttdom1.size):(ttdom1.size + ttdom2.size),0] = ttdom2
    td[(ttdom1.size + ttdom2.size):(ttdom1.size + ttdom2.size + ttdom3.size),0] = ttdom3

    print("sizes:",ttdom1.size,ttdom2.size, ttdom3.size,td01.size,td02.size, td03.size,td.size )
    
    #Trapez plotten
    #1. Gelenkwinkel
    qt = np.zeros([td.size , achsen])

    for i in range(achsen):
        #Parabel t0 bis ts1
        qt[0:td01.size,i] = achsenparameter[i,2] + 0.5*synchron[i,4]*td01**2
        #lin. Steigung ts1 bis ts2
        qt[(td01.size):(td01.size+td02.size),i] = (achsenparameter[i,2] + 0.5*synchron[i,4]*(ts1_dom)**2) + (synchron[i,4]*(ts1_dom))*td02       
        #Parabel ts2 bis t1
        qt[(td01.size+td02.size):(td01.size + td02.size + td03.size),i] = achsenparameter[i,3] - 0.5*synchron[i,4]*((ts2_dom - t_dom) + td03)**2

    plt.figure()
    plt.plot(td,qt)
    plt.grid(True)
    plt.title("Gelenkwinkel Trapez synchron")
    plt.ylabel('Gelenkwinkel in Grad')
    plt.xlabel('Zeit in s')
    
    #2. Winkelgeschwindigkeit
    vt = np.zeros([td.size , achsen])

    for i in range(achsen):
        #Parabel t0 bis ts1
        vt[0:td01.size,i] = synchron[i,4]*td01
        #lin. Steigung ts1 bis ts2
        vt[(td01.size):(td01.size+td02.size),i] = synchron[i,4]*(ts1_dom)      
        #Parabel ts2 bis t1
        vt[(td01.size+td02.size):(td01.size + td02.size + td03.size),i] = - synchron[i,4]*((ts2_dom - t_dom) + td03)

    plt.figure()
    plt.plot(td,vt)
    plt.grid(True)
    plt.title("Winkelgeschwindigkeit Trapez synchron")
    plt.ylabel('Winkelgeschwindigkeit in Grad/s')
    plt.xlabel('Zeit in s')
    
    #2. Winkelbeschleunigung
    at = np.zeros([td.size , achsen])

    for i in range(achsen):
        #Parabel t0 bis ts1
        at[0:td01.size,i] = synchron[i,4]
        #lin. Steigung ts1 bis ts2
        at[(td01.size):(td01.size+td02.size),i] = 0      
        #Parabel ts2 bis t1
        at[(td01.size+td02.size):(td01.size + td02.size + td03.size),i] = - synchron[i,4]

    plt.figure()
    plt.plot(td,at)
    plt.grid(True)
    plt.title("Winkelbeschleunigung Trapez synchron")
    plt.ylabel('Winkelbeschleunigung in Grad/s**2')
    plt.xlabel('Zeit in s')
    
#2. Dreieck
else:
    print("\nDreieckverlauf:")
    #tdiff t0 bis t1 
    ttdom1 = np.arange(0,ts1_dom,delta)
    ttdom2 = np.arange(ts2_dom, t_dom+delta,delta)

    #td von 0
    td01 = np.arange(0,ts1_dom,delta)
    td02 = np.arange(0,(t_dom - ts2_dom) +delta,delta)

    td = np.zeros([ttdom1.size + ttdom2.size, 1])
    td[0:ttdom1.size,0] = ttdom1
    td[(ttdom1.size):(ttdom1.size + ttdom2.size),0] = ttdom2
                  
    
    #Dreieck plotten
    #1. Gelenkwinkel
    qt = np.zeros([td.size , achsen])

    for i in range(achsen):
        #Parabel t0 bis ts1
        qt[0:td01.size,i] = achsenparameter[i,2] + 0.5*synchron[i,4]*td01**2
        #Parabel ts2 bis t1
        qt[(td01.size):(td01.size + td02.size),i] = achsenparameter[i,3] - 0.5*synchron[i,4]*((ts2_dom - t_dom) + td02)**2

    plt.figure()
    plt.plot(td,qt)
    plt.grid(True)
    plt.title("Gelenkwinkel Dreieck synchron")
    plt.ylabel('Gelenkwinkel in Grad')
    plt.xlabel('Zeit in s')
    
    #2. Winkelgeschwindigkeit
    vt = np.zeros([td.size , achsen])

    for i in range(achsen):
        #Parabel t0 bis ts1
        vt[0:td01.size,i] = synchron[i,4]*td01      
        #Parabel ts2 bis t1
        vt[(td01.size):(td01.size + td02.size),i] = - synchron[i,4]*((ts2_dom - t_dom) + td02)

    plt.figure()
    plt.plot(td,vt)
    plt.grid(True)
    plt.title("Winkelgeschwindigkeit Dreieck synchron")
    plt.ylabel('Winkelgeschwindigkeit in Grad/s')
    plt.xlabel('Zeit in s')
    
    #3. Winkelbeschleunigung
    at = np.zeros([td.size , achsen])

    for i in range(achsen):
        #Parabel t0 bis ts1
        at[0:td01.size,i] = synchron[i,4]
        #Parabel ts2 bis t1
        at[(td01.size):(td01.size + td02.size),i] = - synchron[i,4]

    plt.figure()
    plt.plot(td,at)
    plt.grid(True)
    plt.title("Winkelbeschleunigung Dreieck synchron")
    plt.ylabel('Winkelbeschleunigung in Grad/s**2')
    plt.xlabel('Zeit in s')