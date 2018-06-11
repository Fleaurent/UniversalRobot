# -*- coding: utf-8 -*-

import numpy as np
import trajektorienplanung as tp
import robolib3 as rl

#Ausgabe (mit 2 Stellen + folgene 0 unterdrückt)
np.set_printoptions(precision=3, suppress=True)

#Interpolationstakt
tDelta = 1 / 125

#Trajektiorien Verlauf berechnen und Plotten

#Parameter URSim
dhParaUR3 = np.array([(np.deg2rad(90),  0,          151.9,  0),
                      (0,               -243.65,    0,      0),
                      (0,               -213.25,    0,      0),
                      (np.deg2rad(90),  0,          112.35, 0),
                      (np.deg2rad(-90), 0,          85.35,  0),
                      (0,               0,          81.9,   0)])


#TCP Parameter
vMax = 0.2
aMax = 1.0


"""
#6. movel x 400 with a,v --> movel_x400
pStart = np.array([0.300,-0.200,0.400,2.4186,-2.4185,2.4185])
pTarget = np.array([0.300,0.200,0.400,2.4186,-2.4185,2.4185])

[xyzrxryrzT, vTcpT, aTcpT, t] = tp.traj_samplePose(pStart, pTarget, vMax, aMax, tDelta)
tp.plotTrajPose(xyzrxryrzT, vTcpT, aTcpT, t)

qT = tp.traj_sampleAxesIk(xyzrxryrzT, t, dhParaUR3)
tp.plotTrajAxesIk(xyzrxryrzT, t)


filenameCSV = "robolib_movel_x400.csv"
tp.writeCSVTcp(qT, xyzrxryrzT, vTcpT, aTcpT, t, filenameCSV)

    
#ToDo: inverse Kinematik + plot q, save as csv + png
"""

#7. movel x 400 mit a,v nahe Singularität: movel_x400_Singular
pStart = np.array([0.200,-0.200,0.400,2.4186,-2.4185,2.4185])
pTarget = np.array([0.200,0.200,0.400,2.4186,-2.4185,2.4185])

[xyzrxryrzT, vTcpT, aTcpT, t] = tp.traj_samplePose(pStart, pTarget, vMax, aMax, tDelta)
#tp.plotTrajPose(xyzrxryrzT, vTcpT, aTcpT, t)

qT = tp.traj_sampleAxesIk(xyzrxryrzT, dhParaUR3)
#tp.plotTrajAxesIk(qT, t)
print(qT.shape)

filenameCSV = "robolib_movel_x400_Singular.csv"
#tp.writeCSVTcp(qT, xyzrxryrzT, vTcpT, aTcpT, t, filenameCSV)
