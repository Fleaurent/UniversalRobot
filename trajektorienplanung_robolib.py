# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 11:36:47 2018

@author: flore
"""

import numpy as np
import trajektorienplanung as tp
import robolib3 as rl

#Interpolationstakt
tDelta = 1 / 125

#Parameter URSim
dhParaUR3 = np.array([(np.deg2rad(90),  0,          151.9,  0),
                      (0,               -243.65,    0,      0),
                      (0,               -213.25,    0,      0),
                      (np.deg2rad(90),  0,          112.35, 0),
                      (np.deg2rad(-90), 0,          85.35,  0),
                      (0,               0,          81.9,   0)])

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



#1. movej Achse1 30deg mit a,v --> movej_Dreieck
qStart = np.array([np.deg2rad(0),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])
qTarget = np.array([np.deg2rad(30),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])

[qT, vT, aT, t] = tp.traj_sampleAxes(qStart, qTarget, vMax, aMax, tDelta)
tp.plotTrajAxes(qT, vT, aT, t)

xyzrxryrzT = tp.traj_samplePoseFk(qT, dhParaUR3)
tp.plotTrajPoseFk(xyzrxryrzT, t)

filenameCSV = "robolib_movej_Dreieck.csv"
tp.writeCSV(qT, vT, aT, xyzrxryrzT, t, filenameCSV)


"""
#2. movej Achse1 90deg mit a,v --> movej_Trapez
qStart = np.array([np.deg2rad(0),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])
qTarget = np.array([np.deg2rad(90),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])

[qT, vT, aT, t] = tp.traj_sampleAxes(qStart, qTarget, vMax, aMax, tDelta)
tp.plotTrajAxes(qT, vT, aT, t)

xyzrxryrzT = tp.traj_samplePoseFk(qT, dhParaUR3)
tp.plotTrajPoseFk(xyzrxryrzT, t)

filenameCSV = "robolib_movej_Trapez.csv"
tp.writeCSV(qT, vT, aT, xyzrxryrzT, t, filenameCSV)
"""

"""
#3. movej Achse1 30deg in Zeit t --> movej_Dreieck_Zeit
tGesVorgabe = 3
qStart = np.array([np.deg2rad(0),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])
qTarget = np.array([np.deg2rad(30),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])

[qT, vT, aT, t] = tp.traj_sampleAxesTime(qStart, qTarget, vMax, aMax, tGesVorgabe, tDelta)
tp.plotTrajAxes(qT, vT, aT, t)

xyzrxryrzT = tp.traj_samplePoseFk(qT, dhParaUR3)
tp.plotTrajPoseFk(xyzrxryrzT, t)

filenameCSV = "robolib_movej_Dreieck_Zeit.csv"
tp.writeCSV(qT, vT, aT, xyzrxryrzT, t, filenameCSV)
"""

"""
#4. movej q1 90deg in time t --> movej_Trapez_Zeit
tGesVorgabe = 6
qStart = np.array([np.deg2rad(0),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])
qTarget = np.array([np.deg2rad(90),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])

[qT, vT, aT, t] = tp.traj_sampleAxesTime(qStart, qTarget, vMax, aMax, tGesVorgabe, tDelta)
tp.plotTrajAxes(qT, vT, aT, t)

xyzrxryrzT = tp.traj_samplePoseFk(qT, dhParaUR3)
tp.plotTrajPoseFk(xyzrxryrzT, t)

filenameCSV = "robolib_movej_Trapez_Zeit.csv"
tp.writeCSV(qT, vT, aT, xyzrxryrzT, t, filenameCSV)
"""

"""
#5. movej Achse1 90deg, Achse2 60deg, Achse3 30deg in time t --> movej_Synchron
a = 1.0
v = 0.8
tGesVorgabe = 6
qStart = np.array([np.deg2rad(0),np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])
qTarget = np.array([np.deg2rad(90),np.deg2rad(-30),np.deg2rad(-60),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0)])

[qT, vT, aT, t] = tp.traj_sampleAxesTime(qStart, qTarget, vMax, aMax, tGesVorgabe, tDelta)
tp.plotTrajAxes(qT, vT, aT, t)

xyzrxryrzT = tp.traj_samplePoseFk(qT, dhParaUR3)
tp.plotTrajPoseFk(xyzrxryrzT, t)

filenameCSV = "robolib_movej_Synchron.csv"
tp.writeCSV(qT, vT, aT, xyzrxryrzT, t,  filenameCSV)
"""

"""
#TODO --> trajektorienplanung_Pose.py
#6. movel x 400 with a,v --> movel_x400
a = 1.0
v = 0.2

pHome = np.array([0.300,-0.200,0.400,2.4186,-2.4185,2.4185])
pTarget = np.array([0.300,0.200,0.400,2.4186,-2.4185,2.4185])

filenameCSV = "robolib_movel_x400.csv"
tp.writeCSV(qT, vT, aT, t, filenameCSV)



#7. movel x 400 mit a,v nahe Singularität: movel_x400_Singular
a = 1.0
v = 0.2

pHome = np.array([0.200,-0.200,0.400,2.4186,-2.4185,2.4185])
pTarget = np.array([0.200,0.200,0.400,2.4186,-2.4185,2.4185])

filenameCSV = "robolib_movel_x400_Singular.csv"
tp.writeCSV(qT, vT, aT, t, filenameCSV)
"""