# -*- coding: utf-8 -*-

import numpy as np
import trajektorienplanung as tp
import robolib3 as rl

#Ausgabe (mit 2 Stellen + folgene 0 unterdrückt)
np.set_printoptions(precision=3, suppress=True)

#Interpolationstakt
tDelta = 1 / 125

#Trajektiorien Verlauf berechnen und Plotten

#TCP Parameter
vMax = 0.2
aMax = 1.0


"""
#6. movel x 400 with a,v --> movel_x400
pStart = np.array([0.300,-0.200,0.400,2.4186,-2.4185,2.4185])
pTarget = np.array([0.300,0.200,0.400,2.4186,-2.4185,2.4185])

[tS1, tS2, tGes] =  tp.traj_PoseTimestamps(pStart, pTarget, vMax, aMax)
print(tS1, tS2, tGes)

[xyzrxryrzT, vT, aT, t] = tp.traj_samplePose(pStart, pTarget, tS1, tS2, tGes, vMax, aMax, tDelta)
tp.plotTrajPose(xyzrxryrzT, vT, aT, t)
    
#ToDo: inverse Kinematik + plot q, save as csv + png
"""

#7. movel x 400 mit a,v nahe Singularität: movel_x400_Singular
pStart = np.array([0.200,-0.200,0.400,2.4186,-2.4185,2.4185])
pTarget = np.array([0.200,0.200,0.400,2.4186,-2.4185,2.4185])

[tS1, tS2, tGes] =  tp.traj_PoseTimestamps(pStart, pTarget, vMax, aMax)
print(tS1, tS2, tGes)

[xyzrxryrzT, vT, aT, t] = tp.traj_samplePose(pStart, pTarget, tS1, tS2, tGes, vMax, aMax, tDelta)
tp.plotTrajPose(xyzrxryrzT, vT, aT, t)
