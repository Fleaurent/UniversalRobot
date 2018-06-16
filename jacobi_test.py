# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 16:17:31 2018

@author: flore
"""

import jacobi as jc
import trajektorienplanung as tp
import numpy as np

#Interpolationstakt
tDelta = 1 / 125

#Parameter URSim
dhParaUR3 = np.array([(np.deg2rad(90),  0,          151.9,  0),
                      (0,               -243.65,    0,      0),                   (0,               -213.25,    0,      0),
                      (np.deg2rad(90),  0,          112.35, 0),
                      (np.deg2rad(-90), 0,          85.35,  0),
                      (0,               0,          81.9,   0)])


vMaxA1 = 0.8
aMaxA1 = 1.0
qStartA1 = np.deg2rad(0)
qTargetA1 = np.deg2rad(90)

vMaxA2 = 0.8
aMaxA2 = 1.0 
qStartA2 = np.deg2rad(0)
qTargetA2 = np.deg2rad(90)

vMaxA3 = 0.8
aMaxA3 = 1.0
qStartA3 = np.deg2rad(0)
qTargetA3 = np.deg2rad(90)

vMaxA4 = 0.8
aMaxA4 = 1.0
qStartA4 = np.deg2rad(0)
qTargetA4 = np.deg2rad(90)

vMaxA5 = 0.8
aMaxA5 = 1.0
qStartA5 = np.deg2rad(0)
qTargetA5 = np.deg2rad(90)

vMaxA6 = 0.8
aMaxA6 = 1.0
qStartA6 = np.deg2rad(0)
qTargetA6 = np.deg2rad(90)

vMax = np.array([vMaxA1,vMaxA2,vMaxA3,vMaxA4,vMaxA5,vMaxA6])
aMax = np.array([aMaxA1,aMaxA2,aMaxA3,aMaxA4,aMaxA5,aMaxA6])
qStart = np.array([qStartA1,qStartA2,qStartA3,qStartA4,qStartA5,qStartA6])
qTarget = np.array([qTargetA1,qTargetA2,qTargetA3,qTargetA4,qTargetA5,qTargetA6])




"""
Test1 Jacobimatrix für Gelenkwinkel berechnen
"""
q = np.array([np.deg2rad(0),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])

J = jc.jacobi_UR(q, dhParaUR3)
print(J)


"""
Test2: Anwendung Jakobi für Geschwindigkeit Tcp für Trajektorie
"""
#1. movej Achse1 30deg mit a,v --> movej_Dreieck
qStart = np.array([np.deg2rad(0),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])
qTarget = np.array([np.deg2rad(90),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])

[qT, vT, aT, t] = tp.traj_sampleAxes(qStart, qTarget, vMax, aMax, tDelta)
tp.plotTrajAxes(qT, vT, aT, t)

vTcpT = jc.vTcp(qT, vT, dhParaUR3)
print(vTcpT.shape)
jc.plotVTcp(vTcpT,t)

rd = np.array([0,0,10,0,0,0])
forceT = jc.force(qT, rd, dhParaUR3)
print(forceT.shape)
jc.plotForce(forceT,t)
    
singularT = jc.singular(qT, dhParaUR3)
print(singularT.shape)
jc.plotSingular(singularT,t)