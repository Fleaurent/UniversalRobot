# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 11:36:47 2018

@author: flore
"""

import numpy as np
import robolib as rl
import trajektorienplanung as tp
import jacobi as jc

#Interpolationstakt
tDelta = 1 / 125

#Parameter URSim
dhParaUR3 = np.array([(np.deg2rad(90),  0,          151.9,  0),
                      (0,               -243.65,    0,      0),
                      (0,               -213.25,    0,      0),
                      (np.deg2rad(90),  0,          112.35, 0),
                      (np.deg2rad(-90), 0,          85.35,  0),
                      (0,               0,          81.9,   0)])

#TCP Parameter in mm
vMax = 200
aMax = 1000

#Inverse Kinematik Achsenstellung
sol = 6
					  
#Achsen Parameter: alle Achsen gleiche Parameter
#vMax = 0.8
#aMax = 1.0

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
#1. movej Achse1 30deg mit a,v --> movej_Dreieck
qStart = np.array([np.deg2rad(0),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])
qTarget = np.array([np.deg2rad(30),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])

[qT, vT, aT, t] = tp.traj_sampleAxes(qStart, qTarget, vMax, aMax, tDelta)
#tp.plotTrajAxes(qT, vT, aT, t)

xyzrxryrzT = tp.traj_samplePoseFk(qT, dhParaUR3)
#tp.plotTrajPoseFk(xyzrxryrzT, t)

xyzrxryrzVT = jc.vTcp(qT, vT, dhParaUR3)
#jc.plotVTcp(xyzrxryrzVT, t)

filenameCSV = "robolib_movej_Dreieck.csv"
tp.writeCSV(qT, vT, aT, xyzrxryrzT, xyzrxryrzVT, t, filenameCSV)



#2. movej Achse1 90deg mit a,v --> movej_Trapez
qStart = np.array([np.deg2rad(0),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])
qTarget = np.array([np.deg2rad(90),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])

[qT, vT, aT, t] = tp.traj_sampleAxes(qStart, qTarget, vMax, aMax, tDelta)
#tp.plotTrajAxes(qT, vT, aT, t)

xyzrxryrzT = tp.traj_samplePoseFk(qT, dhParaUR3)
#tp.plotTrajPoseFk(xyzrxryrzT, t)

xyzrxryrzVT = jc.vTcp(qT, vT, dhParaUR3)
#jc.plotVTcp(xyzrxryrzVT, t)

filenameCSV = "robolib_movej_Trapez.csv"
tp.writeCSV(qT, vT, aT, xyzrxryrzT, xyzrxryrzVT, t, filenameCSV)



#3. movej Achse1 30deg in Zeit t --> movej_Dreieck_Zeit
tGesVorgabe = 3
qStart = np.array([np.deg2rad(0),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])
qTarget = np.array([np.deg2rad(30),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])

[qT, vT, aT, t] = tp.traj_sampleAxesTime(qStart, qTarget, vMax, aMax, tGesVorgabe, tDelta)
#tp.plotTrajAxes(qT, vT, aT, t)

xyzrxryrzT = tp.traj_samplePoseFk(qT, dhParaUR3)
#tp.plotTrajPoseFk(xyzrxryrzT, t)

xyzrxryrzVT = jc.vTcp(qT, vT, dhParaUR3)
#jc.plotVTcp(xyzrxryrzVT, t)

filenameCSV = "robolib_movej_Dreieck_Zeit.csv"
tp.writeCSV(qT, vT, aT, xyzrxryrzT, xyzrxryrzVT, t, filenameCSV)



#4. movej q1 90deg in time t --> movej_Trapez_Zeit
tGesVorgabe = 6
qStart = np.array([np.deg2rad(0),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])
qTarget = np.array([np.deg2rad(90),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])

[qT, vT, aT, t] = tp.traj_sampleAxesTime(qStart, qTarget, vMax, aMax, tGesVorgabe, tDelta)
#tp.plotTrajAxes(qT, vT, aT, t)

xyzrxryrzT = tp.traj_samplePoseFk(qT, dhParaUR3)
#tp.plotTrajPoseFk(xyzrxryrzT, t)

xyzrxryrzVT = jc.vTcp(qT, vT, dhParaUR3)
#jc.plotVTcp(xyzrxryrzVT, t)

filenameCSV = "robolib_movej_Trapez_Zeit.csv"
tp.writeCSV(qT, vT, aT, xyzrxryrzT, xyzrxryrzVT, t, filenameCSV)



#5. movej Achse1 90deg, Achse2 60deg, Achse3 30deg in time t --> movej_Synchron
a = 1.0
v = 0.8
tGesVorgabe = 6
qStart = np.array([np.deg2rad(0),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])
qTarget = np.array([np.deg2rad(90),np.deg2rad(-30),np.deg2rad(-60),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])

[qT, vT, aT, t] = tp.traj_sampleAxesTime(qStart, qTarget, vMax, aMax, tGesVorgabe, tDelta)
#tp.plotTrajAxes(qT, vT, aT, t)

xyzrxryrzT = tp.traj_samplePoseFk(qT, dhParaUR3)
#tp.plotTrajPoseFk(xyzrxryrzT, t)

xyzrxryrzVT = jc.vTcp(qT, vT, dhParaUR3)
#jc.plotVTcp(xyzrxryrzVT, t)

filenameCSV = "robolib_movej_Synchron.csv"
tp.writeCSV(qT, vT, aT, xyzrxryrzT, xyzrxryrzVT, t,  filenameCSV)

"""

#6. movel x 400 with a,v --> movel_x400
pStart = np.array([-300,-200,300,2.2214,2.2214,0])
pTarget = np.array([-300,200,300,2.2214,2.2214,0])
vMax = 200
aMax = 1000

[xyzrxryrzT, xyzrxryrzVT, xyzrxryrzAT, vTcpT, aTcpT, t] = tp.traj_samplePose(pStart, pTarget, vMax, aMax, tDelta)
tp.plotTrajPose(xyzrxryrzT, xyzrxryrzVT, xyzrxryrzAT, vTcpT, aTcpT, t)

qT = tp.traj_sampleAxesIk(xyzrxryrzT, dhParaUR3, sol)
vT = jc.vT(qT, xyzrxryrzVT, dhParaUR3)
tp.plotTrajAxesIk(qT, vT, t)

filenameCSV = "robolib_movel_x400.csv"
tp.writeCSVTcp(qT, vT, xyzrxryrzT, xyzrxryrzVT, xyzrxryrzAT, t, filenameCSV)


#7. movel x 400 mit a,v nahe Singularität: movel_x400_Singular
pStart = np.array([-150,-200,300,2.2214,2.2214,0])
pTarget = np.array([-150,200,300,2.2214,2.2214,0])
vMax = 150
aMax = 1000

[xyzrxryrzT, xyzrxryrzVT, xyzrxryrzAT, vTcpT, aTcpT, t] = tp.traj_samplePose(pStart, pTarget, vMax, aMax, tDelta)
tp.plotTrajPose(xyzrxryrzT, xyzrxryrzVT, xyzrxryrzAT,vTcpT, aTcpT, t)

qT = tp.traj_sampleAxesIk(xyzrxryrzT, dhParaUR3, sol)
vT = jc.vT(qT, xyzrxryrzVT, dhParaUR3)
tp.plotTrajAxesIk(qT, vT, t)

filenameCSV = "robolib_movel_x400_Singular.csv"
tp.writeCSVTcp(qT, vT, xyzrxryrzT, xyzrxryrzVT, xyzrxryrzAT, t, filenameCSV)

