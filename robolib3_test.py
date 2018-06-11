# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 18:21:09 2018

@author: flore
"""

import numpy as np
import robolib3 as rl

np.set_printoptions(precision=3,suppress=True)


#0.Testparameter
xyzrpyTest = np.array([10, 20, 30, np.deg2rad(45),np.deg2rad(45),np.deg2rad(45)])
rotvecHomeSim = np.array([295.15, -112.35, 480.90, 2.4184, -2.4184, 2.4184])
xyzrpyHomeSim = np.array([295.15, -112.35, 480.90, -1.571, 0, -1.571])
rotvecHomeRobo = np.array([295.40, -110.40, 445.05, -1.209, 1.209, -1.209])
xyzrpyHomeRobo = np.array([295.40, -110.40, 445.05, -1.571, 0, -1.571])
qHome = np.array([np.deg2rad(0), np.deg2rad(-90),np.deg2rad(-90),np.deg2rad(0),np.deg2rad(90),np.deg2rad(0),])

print("xyzrpyTest:\t", xyzrpyTest)
print("rotvecHome:\t", rotvecHomeSim)
print("xyzrpyHome:\t", xyzrpyHomeSim)
print("qHome:\t\t", qHome)

#1. RPY == XYZ
print("\n1. RPY == XYZ")

Trpy = rl.rpy_2_T(xyzrpyHomeSim)
print("Trpy:\n", Trpy)

xyzrpyTest = rl.T_2_rpy(Trpy)
print("xyzrpy: ",xyzrpyTest)


#2. ZYX
print("\n2. ZYX")

Tzyx = rl.zyx_2_T(xyzrpyHomeSim)
print("Tzyx:\n", Tzyx)

xyzrpyTest = rl.T_2_zyx(Tzyx)
print("xyzrpy: ",xyzrpyTest)


#3. Rotation Vector
print("\n3. Rotation Vector")

rotvecTest = rl.T_2_rotvec(Trpy)
print("rotvecHome: ", rotvecTest)

TrotvecHome = rl.rotvec_2_T(rotvecHomeSim)
print(" TrotvecHome:\n", TrotvecHome)

rotvecHome = rl.T_2_rotvec(TrotvecHome)
print("rotvecHome: ", rotvecHome)


#4. Denavit Hartenberg
print("\n4. Denavit Hartenberg")

alpha = np.deg2rad(90)
a = 1
d = 1
theta = np.deg2rad(90)

print("\ndh = dh(%.3f,%.3f,%.3f,%.3f)" % (alpha, a, d, theta))

dh = rl.dh(alpha, a, d, theta)
print(dh)

print("\ndhm = dhm(%.3f,%.3f,%.3f,%.3f)" % (alpha, a, d, theta))
dhm = rl.dhm(alpha, a, d, theta)
print(dhm)

#5. [DH]  Forwardkinematik
print("\n5. [DH]  Forwardkinematik")
#q = np.array([0,0,0,0,0,0])
#q = np.array([np.deg2rad(90),0,0,0,0,0])
#qHome
q = np.array([0,np.deg2rad(-90),np.deg2rad(-90),0,np.deg2rad(90),0])
#q = np.array([np.deg2rad(45),np.deg2rad(45),np.deg2rad(45),np.deg2rad(45),np.deg2rad(45),np.deg2rad(45)])
print("Winkel q: " )
print(q)

#--> V1: Parameter aus File
#print("\nV1: Parameter aus File")
#a = [0.00000, -0.24365, -0.21325, 0.00000, 0.00000, 0.0000]
#d = [0.1519, 0.00000, 0.00000, 0.11235, 0.08535, 0.0819]
#alpha = [ 1.570796327, 0, 0, 1.570796327, -1.570796327, 0 ]
#q_home_offset = [0, -1.570796327, 0, -1.570796327, 0, 0]
#joint_direction = [1, 1, -1, 1, 1, 1]


#Parameter Robodk
#l_ur = np.array([118,243.65,213,110.4,83.4,82.4])
dhParaUR3 = np.array([(np.deg2rad(-90), 0,         118,     np.deg2rad(180)),
                      (0,               243.65,    0,       0),
                      (0,               213,       0,       0),
                      (np.deg2rad(-90), 0,         110.4,   0),
                      (np.deg2rad(90),  0,         83.4,    0),
                      (0,               0,         82.4,    np.deg2rad(180))])

#Parameter Kombiniert --> RoboDK
dhParaUR3 = np.array([(np.deg2rad(90),  0,          118,    0),
                      (0,               -243.65,    0,      0),
                      (0,               -213,       0,      0),
                      (np.deg2rad(90),  0,          110.4,  0),
                      (np.deg2rad(-90), 0,          83.4,   0),
                      (0,               0,          82.4,   0)])

#Parameter URSim
dhParaUR3 = np.array([(np.deg2rad(90),  0,          151.9,  0),
                      (0,               -243.65,    0,      0),
                      (0,               -213.25,    0,      0),
                      (np.deg2rad(90),  0,          112.35, 0),
                      (np.deg2rad(-90), 0,          85.35,  0),
                      (0,               0,          81.9,   0)])


#print("dhParaUR3: \n", dhParaUR3)
print("fk_UR3 = fk_ur(dhParaUR3,q)")
fk_UR3 = rl.fk_ur(dhParaUR3,q)
print(fk_UR3)

rotvecFk = rl.T_2_rotvec(fk_UR3)
print("rotvecFk: ", rotvecFk)


#6. Inverse kinematik
print("\n6. Inverse kinematik")
#a)xyzrpy --> q
#qHome = np.array([0,np.deg2rad(-90),np.deg2rad(-90),0,np.deg2rad(90),0])
#xyzrpyTest = np.array([-295.4, -110.4, 445.05, np.deg2rad(0),np.deg2rad(90),np.deg2rad(-90)])
#q = np.array([np.deg2rad(45),np.deg2rad(45),np.deg2rad(45),np.deg2rad(45),np.deg2rad(45),np.deg2rad(45)])
#xyzrpyTest = np.array([68.272, -170.257, -249.514, np.deg2rad(163.675),np.deg2rad(58.6),np.deg2rad(118.175)])
#xyzrpyTest = np.array([68.272, -170.257, -249.514, np.deg2rad(0),np.deg2rad(0),np.deg2rad(0)])
#q = np.array([0,np.deg2rad(0),np.deg2rad(0),0,np.deg2rad(0),0])
#xyzrpyTest = np.array([-456.65, -192.8, 34.6, np.deg2rad(90),np.deg2rad(0),np.deg2rad(0)])
#xyzrpyTest = np.array([0, -194.25, 694.15, 0,2.214,-2.2214])
#q = np.array([0,0,0,0,0,0])
#xyzrpyTest = np.array([-457, -193, 35, np.deg2rad(90),np.deg2rad(0),np.deg2rad(0)])
#print(xyzrpyTest)

#b)xyzrxryrz rotvec --> q
#qHome = np.array([0,np.deg2rad(-90),np.deg2rad(-90),0,np.deg2rad(90),0])
#tcp = np.array([ 295.15, -112.35, 480.9, -1.209, 1.209, -1.209])    #sol6
tcp = np.array([ 295.15, -112.35, 480.9, 2.4184, -2.4184, 2.4184])  #sol6
#q = np.array([np.deg2rad(45),np.deg2rad(45),np.deg2rad(45),np.deg2rad(45),np.deg2rad(45),np.deg2rad(45)])
#tcp = np.array([ 70.2, -170.59, -214.24, 2.066, -2.921, 1.461])

qIk = np.array([0,0,0,0,0,0])
sol = 0

#qIK = rl.ik_ur(dhParaUR3, tcp, sol)
#print("sol:", sol, qIK)

for sol in range(8):
    qIK = rl.ik_ur(dhParaUR3, tcp, sol)
    print("sol:", sol, qIK)
    




"""
theta = 1
alpha = 1
d = 1
print(np.dot(rl.rotz(theta),rl.transl(0,0,d)))
print(np.dot(rl.transl(0,0,d),rl.rotz(theta)))
print(np.dot(rl.rotz(theta),rl.rotx(alpha)))
print(np.dot(rl.rotx(alpha),rl.rotz(theta)))
"""