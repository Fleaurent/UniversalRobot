# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 14:13:50 2018

@author: flore
"""

import numpy as np
import math

np.set_printoptions(precision=3,suppress=True)


def rotx(a):
    """
    Rotation about x axis
    """
    ca = np.cos(a)
    sa = np.sin(a)
    T = np.array([(1, 0, 0, 0), (0, ca, -sa, 0), (0, sa, ca, 0), (0, 0, 0, 1)])
    return T

def roty(a):
    """
    Rotation about y axis
    """
    ca = np.cos(a)
    sa = np.sin(a)
    T = np.array([(ca, 0, sa, 0), (0, 1, 0, 0), (-sa, 0, ca, 0), (0, 0, 0, 1)])
    return T

def rotz(a):
    """
    Rotation about z axis
    """
    ca = np.cos(a)
    sa = np.sin(a)
    T = np.array([(ca, -sa, 0, 0), (sa, ca, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)])
    return T

def transl(x, y, z):
    """
    Translation about x,y,z
    """
    T = np.array([(1, 0, 0, x), (0, 1, 0, y), (0, 0, 1, z), (0, 0, 0, 1)])
    return T

def Tinv(T):
    """
    Inverse of homogeneous trafo matrix
    """
    R = T[0:3, 0:3]
    Ri = R.transpose()
    Ti = np.eye(4)
    Ti[0:3, 0:3] = Ri
    Ti[0:3, 3:4] = -(Ri.dot(T[0:3, 3:4]))
    return Ti

def T_2_rpy(T):
    """
    Matrix to roll pitch yaw (KUKA)
    X-Y-Z Darstellung
    1. Rotation um x-Achse um Winkel gamma == roll
    2. Rotation um y-Achse um Winkel beta == pitch
    3. Rotation um z-Achse um Winkel alpha == yaw
    """
    #Translation
    x = T[0,3]
    y = T[1,3]
    z = T[2,3]
    
    #Rotation
    R = T[0:3,0:3]
    #Singularität bei pitch == 90deg!
    pitch = np.arctan2(-R[2,0], np.sqrt(R[0,0]*R[0,0] + R[1,0]*R[1,0]))  #ry == beta == pitch
    yaw = np.arctan2((R[1,0]/np.cos(pitch)), (R[0,0]/np.cos(pitch)))  #rz == alpha == yaw
    roll = np.arctan2((R[2,1]/np.cos(pitch)), (R[2,2]/np.cos(pitch))) #rx == gamma == roll
    
    return np.array([x,y,z,roll,pitch,yaw])

def rpy_2_T(xyzrpy):
    """
    roll pitch yaw to matrix (KUKA)
    X-Y-Z Darstellung
    1. Rotation um x-Achse um Winkel gamma == roll
    2. Rotation um y-Achse um Winkel beta == pitch
    3. Rotation um z-Achse um Winkel alpha == yaw
    """
    x = xyzrpy[0]
    y = xyzrpy[1]
    z = xyzrpy[2]   
    roll = xyzrpy[3]
    pitch = xyzrpy[4]
    yaw = xyzrpy[5]
    
    T = np.eye(4)
    
    #Translation
    T[0,3] = x
    T[1,3] = y
    T[2,3] = z   
    
    #Rotation
    R = np.eye(3)
    #3. rz == alpha == yaw 2. ry == beta == pitch 1. rx == gamma == roll
    R = np.dot(rotz(yaw), np.dot(roty(pitch), rotx(roll)))
    T[0:3,0:3] = R[0:3, 0:3]
    
    return T

def T_2_zyx(T):
    """
    Matrix to rx ry rz (UR)
    Z-Y-X-Darstellung
    1. Rotation um z-Achse um Winkel gamma == rz
    2. Rotation um y-Achse um Winkel beta == ry
    3. Rotation um x-Achse um Winkel alpha == rx
    """
    #Translation
    x = T[0,3]
    y = T[1,3]
    z = T[2,3]
    
    #Rotation
    R = T[0:3,0:3]
    #Singularität bei ry == 90deg!
    ry = math.atan2(R[0,2], math.sqrt(R[1,2]*R[1,2] + R[2,2]*R[2,2]))  
    rx = math.atan2((-R[1,2]/math.cos(ry)), (R[2,2]/math.cos(ry))) 
    rz = math.atan2((-R[0,1]/math.cos(ry)), (R[0,0]/math.cos(ry)))
    
    return np.array([x,y,z,rx,ry,rz])

def zyx_2_T(xyzrpy):
    """
    rx ry rz to Matrix (UR)
    Z-Y-X-Darstellung
    1. Rotation um z-Achse um Winkel gamma == rz
    2. Rotation um y-Achse um Winkel beta == ry
    3. Rotation um x-Achse um Winkel alpha == rx
    """
    x = xyzrpy[0]
    y = xyzrpy[1]
    z = xyzrpy[2]   
    rx = xyzrpy[3]
    ry = xyzrpy[4]
    rz = xyzrpy[5]
    
    T = np.eye(4)
    
    #Translation
    T[0,3] = x
    T[1,3] = y
    T[2,3] = z   
    
    #Rotation
    R = np.eye(3)

    #3. rx == alpha 2. ry == beta 1. rz == gamma
    R = np.dot(np.dot(rotx(rx), roty(ry)), rotz(rz))
    T[0:3,0:3] = R[0:3, 0:3]
    
    return T

def T_2_rotvec(T):
    """
    Matrix to rotation vector representation
    """
    
    #Translation
    x = T[0,3]
    y = T[1,3]
    z = T[2,3]
    
    #Rotation
    R = np.eye(3)
    R[0:3,0:3] = T[0:3, 0:3]

    theta = math.acos(((R[0, 0] + R[1, 1] + R[2, 2]) - 1) / 2)
    
    if np.abs(math.sin(theta)) < 1e-6:
        rx = 0
        ry = 0
        rz = 0
        
    else:
        multi = 1 / (2 * math.sin(theta))
        
        rx = multi * (R[2, 1] - R[1, 2]) * theta
        ry = multi * (R[0, 2] - R[2, 0]) * theta
        rz = multi * (R[1, 0] - R[0, 1]) * theta
        
    return np.array([x,y,z,rx,ry,rz])

def rotvec_2_T(xyzrxryrz):
    """
    rotation vector representation to matrix
    """
    x = xyzrxryrz[0]
    y = xyzrxryrz[1]
    z = xyzrxryrz[2]
    rx = xyzrxryrz[3]
    ry = xyzrxryrz[4]
    rz = xyzrxryrz[5]
    
    T = np.eye(4)
    
    #Translation
    T[0,3] = x
    T[1,3] = y
    T[2,3] = z 
    
    #Rotation
    theta = math.sqrt(rx**2 + ry**2 + rz**2)
    
    kx = rx / theta
    ky = ry / theta 
    kz = rz / theta

    st = math.sin(theta)
    ct = math.cos(theta)
    vt = 1 - ct
	   
    T[0,0] = kx * kx * vt + ct
    T[0,1] = kx * ky * vt - kz * st
    T[0,2] = kx * kz * vt + ky * st

    T[1,0] = kx * ky * vt + kz * st
    T[1,1] = ky * ky * vt + ct
    T[1,2] = ky * kz * vt - kx * st

    T[2,0] = kx * kz * vt -ky * st
    T[2,1] = ky * kz * vt + kx * st
    T[2,2] = kz * kz * vt + ct

    return T

def dh(alpha, a, d, theta):
    """
    Denavit-Hartenberg (classic)
    """
    T = np.eye(4)
    #T =  T_theta * T_d * T_a * T_alpha
    T = np.dot(np.dot(np.dot(rotz(theta),transl(0,0,d)),transl(a,0,0)),rotx(alpha))
    
    return T

def dhm(alpha, a, d, theta):
    """
    Denavit-Hartenberg (modified)
    """
    T = np.eye(4)
    #T = T_a * T_alpha * T_d * T_theta
    T = np.dot(np.dot(np.dot(transl(a,0,0),rotx(alpha)),transl(0,0,d)),rotz(theta))
    
    return T

def fk_ur(dh_para, q):
    """
    Forward Kinematics for UR type robots
    """
    T_0_6 = np.eye(4)
    i = 0
    for dhSP in dh_para:
        #print(dhSP)
        T = dh(dhSP[0],dhSP[1],dhSP[2],dhSP[3] + q[i])
        #print(T)
        T_0_6 = np.dot(T_0_6,T)
        #print(T_0_6)
        i = i+1
    return T_0_6

def ik_ur(dh_para, tcp, sol):
    """
    Inverse Kinematics for UR type robots
    """
    T_0_6 = rotvec_2_T(tcp)
    #T_0_6 = zyx_2_T(tcp)
    
    # Achse 5 in 0
    #O5_in_0 = np.dot(T_0_6, transl(0, 0, -dh_para[5, 2]))
    #print(O5_in_0)
    O5_in_0 = np.dot(T_0_6, np.array([0, 0, -dh_para[5, 2], 1]))
    #print(O5_in_0)
    
    # Winkel q1
    #alpha1 = math.atan2(O5_in_0[1,3],O5_in_0[0,3])
    #R = math.sqrt(O5_in_0[0,3]**2 + O5_in_0[1,3]**2)
    alpha1 = math.atan2(O5_in_0[1],O5_in_0[0])
    R = math.sqrt(O5_in_0[0]**2 + O5_in_0[1]**2)
    l4 = abs(dh_para[3, 2])
    alpha2 = math.acos(l4 / R)
        
    if (sol & 4 == 0):
        q1 = alpha1 + alpha2 + np.pi / 2
    else:
        q1 = alpha1 - alpha2 + np.pi / 2
    #print("q1+: ", alpha1 + alpha2 + np.pi / 2)
    #print("q1-: ", alpha1 - alpha2 + np.pi / 2)
    
    # Winkel q5
    s1 = math.sin(q1)
    c1 = math.cos(q1)
    l6 = abs(dh_para[5,2])
    x = T_0_6[0,3]
    y = T_0_6[1,3]
    
    z = (x*s1 - y*c1 - l4) / l6
    if(z > 1):
        #print("(x*s1 - y*c1 - l4) / l6 = ", z)
        z = 0.9999
        #print("--> q5 = acos(1) = 0")
        
    q5 = math.acos(z)
    if sol & 1:
        q5 = -q5
    
    #print("\nq5: ", q5)
    
    # Winkel q6
    T_0_1 = dh(dh_para[0, 0], dh_para[0, 1], dh_para[0, 2], q1)
    T_1_0 = Tinv(T_0_1)
    T_1_6 = np.dot(T_1_0, T_0_6)
    
    s5 = math.sin(q5)
    #c5 = math.cos(q5)
    q6 = math.atan2((-T_1_6[1,2]/s5),(T_1_6[0,2]/s5))
    #print("q6",q6)
    

    #r11 = T_0_6[0,0]
    #r21 = T_0_6[1,0]
    #r12 = T_0_6[0,1]
    #r22 = T_0_6[1,1]
      
    #q6 = math.atan2((-r21*s1 + r22*c1) / s5, (r11*s1 - r12*c1) / s5)
    #print("\nq6: ", q6)
    #q6 = np.deg2rad(45)
    
    # Ebenes Problem mit drei parallelen Achsen
    T_0_1 = dh(dh_para[0, 0], dh_para[0, 1], dh_para[0, 2], q1)
    T_4_5 = dh(dh_para[4, 0], dh_para[4, 1], dh_para[4, 2], q5)
    T_5_6 = dh(dh_para[5, 0], dh_para[5, 1], dh_para[5, 2], q6)
    T_4_6 = np.dot(T_4_5, T_5_6)
    T_6_4 = Tinv(T_4_6)
    T_1_0 = Tinv(T_0_1)
    T_1_4 = np.dot(np.dot(T_1_0, T_0_6), T_6_4)
    # 90 Grad Rotation zwischen 4 und 5 kompensieren
    #T_1_4 = np.dot(T_1_4, rotx(-np.pi / 2))
    #print("T_1_4 ", T_1_4)
    
    x_S = T_1_4[0, 3]
    y_S = T_1_4[1, 3]
    #z_S = T_1_4[2,3]
    l1 = abs(dh_para[1, 1])
    l2 = abs(dh_para[2, 1])
    
    
    # Winkel q3
    #test = (x_S**2 + y_S**2 - l1**2 - l2**2) / (2 * l1 * l2)
    #print("Value: ", test )
    try:
        q3 = math.acos((x_S**2 + y_S**2 - l1**2 - l2**2) / (2 * l1 * l2))
    except:
        return 0
    
    if (sol & 2 == 0):
        q3 = q3
    else:
        q3 = -q3
    
    #print("\nq3: ", q3)
        
    
    # Winkel q2
    beta = math.atan2(y_S, x_S)
    psi = math.acos((x_S**2 + y_S**2 + (l1)**2 - (l2)**2) / (2 * (l1) * math.sqrt(x_S**2 + y_S**2)))
    #psi = math.acos(0)
    
    if q3 > 0:
        q2 = beta - psi - np.pi
    else:
        q2 = beta + psi - np.pi
    if q2 < -np.pi:
        q2 = q2 + 2 * np.pi
    
    #print("\nq2: ", q2)
    
    # Gesamtwinkel
    #rotvec = T_2_rotvec(T_1_4)
    #T_0_4 = np.dot(T_0_1,T_1_4)
    #xyzrxryrz = T_2_zyx(np.dot(T_0_4,transl(0,0,1)))
    print(T_1_4)
    #print(xyzrxryrz)
    #q234 = np.arctan(xyzrxryrz[0]/xyzrxryrz[2])
    
    xyzrxryrz = T_2_zyx(T_1_4)
    #print(xyzrxryrz)
    q234 = xyzrxryrz[5]
        
    # Winkel q4
    q4 = q234 - q2 - q3
    
    #print("\nq4: ", q4)
    
    
    return np.array([q1, q2, q3, q4, q5, q6])
    