# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 16:17:11 2018

@author: flore
"""

import numpy as np
import trajektorienplanung as tp
import robolib3 as rl


def jacobi_UR(dh_para,q):
    
    J = np.zeros((q.size,q.size))
    T = np.eye(4)
    T_0_i = np.eye(4)
    
    T_0_6 = rl.fk_ur(dh_para, q)
    p = T_0_6[0:3,3]
    
    for i in range(6):
        T = rl.dh(dh_para[i,0], dh_para[i,1], dh_para[i,2], dh_para[i,3] + q[i])
        T_0_i = np.dot(T_0_i, T)
        
        z_i = T_0_i[0:3, 2]
        p_i = T_0_i[0:3, 3]
        
        r = p - p_i
        
        J[0:3, i] = np.cross(z_i, r)
        J[3:6, i] = z_i
    
    return J


def vTcp(dh_para, qT, vT):
    
    vTcpT = np.zeros((qT.shape[0],6))
    
    for i in range(qT.shape[0]):
        J = jacobi_UR(dh_para, qT[i])
        vTcpT[i] = np.dot(J,vT[i])
    
    return vTcpT


def force(dh_para, qT, rd):
    
    forceT = np.zeros((qT.shape[0],6))
    
    for i in range(qT.shape[0]):
        J = jacobi_UR(dh_para, qT[i])
        Jinv = np.linalg.inv(J)
        forceT[i] = np.dot(Jinv, rd)
        
    return forceT


def singular(dh_para, qT):
    
    singularT = np.zeros(qT.shape[0])
    
    for i in range(qT.shape[0]):
        J = jacobi_UR(dh_para, qT[i])
        singularT[i] = np.linalg.det(J)
        
    return singularT


def plotVTcp(vTcpT,t):
    print("plot")
    return 0


def plotForce(forceT,t):
    print("plot")
    return 0
    
def plotSingular(singularT,t):
    print("plot")
    return  0