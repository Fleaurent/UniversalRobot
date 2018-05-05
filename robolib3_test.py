# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 18:21:09 2018

@author: flore
"""

import numpy as np
import robolib3 as rl

np.set_printoptions(precision=3,suppress=True)

xyzrpyTest = np.array([10, 20, 30, np.deg2rad(45),np.deg2rad(45),np.deg2rad(45)])
print(xyzrpyTest)


#1. RPY == XYZ
TTest = rl.rpy_2_T(xyzrpyTest)
print(TTest)

xyzrpyTest = rl.T_2_rpy(TTest)
print(xyzrpyTest)


#2. ZYX
TTest = rl.zyx_2_T(xyzrpyTest)
print(TTest)

xyzrpyTest = rl.T_2_zyx(TTest)
print(xyzrpyTest)


#3. Rotation Vector
rotvecTest = rl.T_2_rotvec(TTest)
print(rotvecTest)

#Rotation Vector Matrix
TTest = rl.rotvec_2_T(rotvecTest)
print(TTest)

rotvecTest = rl.T_2_rotvec(TTest)
print(rotvecTest)

xyzrpyTest = rl.T_2_rpy(TTest)
print(xyzrpyTest)

#Denavit Hartenberg --> Vorwärtskinematik
alpha = 0 
a = 0
d = 0
theta = 0
dhSP = np.array([alpha, a, d, theta])
print("\ndh = dh(%3.f,%3.f,%3.f,%3.f)" % (dhSP[0],dhSP[1],dhSP[2],dhSP[3]))
dh = rl.dh(dhSP[0],dhSP[1],dhSP[2],dhSP[3])
print(dh)

print("\ndhm = dhm(%3.f,%3.f,%3.f,%3.f)" % (dhSP[0],dhSP[1],dhSP[2],dhSP[3]))
dhm = rl.dhm(dhSP[0],dhSP[1],dhSP[2],dhSP[3])
print(dhm)

#[DH]  Forwardkinematik
q = np.array([0,0,0,0,0,0])
#qHome
#q = np.array([0,np.deg2rad(-90),np.deg2rad(-90),0,np.deg2rad(90),0])
#q = np.array([np.deg2rad(45),np.deg2rad(45),np.deg2rad(45),np.deg2rad(45),np.deg2rad(45),np.deg2rad(45)])

#--> V1: Parameter aus File
print("\nV1: Parameter aus File")
#a = [0.00000, -0.24365, -0.21325, 0.00000, 0.00000, 0.0000]
#d = [0.1519, 0.00000, 0.00000, 0.11235, 0.08535, 0.0819]
#alpha = [ 1.570796327, 0, 0, 1.570796327, -1.570796327, 0 ]
#q_home_offset = [0, -1.570796327, 0, -1.570796327, 0, 0]
#joint_direction = [1, 1, -1, 1, 1, 1]
dhParaUR3 = np.array([(1.5708,  0,          151.9,  0),
                      (0,       -243.65,    0,      -1.5708),
                      (0,       -213.25,    0,      0),
                      (1.5708,  0,          112.35, -1.5708),
                      (-1.5708, 0,          85.35,  0),
                      (0,       0,          81.9,   0)])
print("dhParaUR3: \n", dhParaUR3)
print("q = ",q)
print("fk_UR3 = fk_ur(dhParaUR3,q)")
fk_UR3 = rl.fk_ur(dhParaUR3,q)
print(fk_UR3)

xyzrxryrzTCP = rl.T_2_rpy(fk_UR3)
print(xyzrxryrzTCP)

qIk = np.array([0,0,0,0,0,0])
sol = 4
qIK = rl.ik_ur(dhParaUR3, xyzrxryrzTCP, sol)
print(qIK)


theta = 1
alpha = 1
d = 1
print(np.dot(rl.rotz(theta),rl.transl(0,0,d)))
print(np.dot(rl.transl(0,0,d),rl.rotz(theta)))
print(np.dot(rl.rotz(theta),rl.rotx(alpha)))
print(np.dot(rl.rotx(alpha),rl.rotz(theta)))