# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 16:17:11 2018

@author: flore
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import trajektorienplanung as tp
import robolib3 as rl

"""
Berechnung Jakobimatrix(q) für Universal Robot
"""
def jacobi_UR(q, dh_para):
    
    J = np.zeros((q.size,q.size))
    T = np.eye(4)
    T_0_i = np.eye(4)
    
    T_0_6 = rl.fk_ur(dh_para, q)
    #print(T_0_6)
    p = T_0_6[0:3,3]
    
    i=0
    for i in range(6):
        
        z_i = T_0_i[0:3, 2]
        p_i = T_0_i[0:3, 3]
        
        T = rl.dh(dh_para[i,0], dh_para[i,1], dh_para[i,2], dh_para[i,3] + q[i])
        T_0_i = np.dot(T_0_i, T)
        #print(T_0_i)
        
        r = p - p_i
        
        J[0:3, i] = np.cross(z_i, r)
        J[3:6, i] = z_i

    return J

"""
TCP Geschwindigkeit(t) = Jakobimatrix(q(t)) * Gelenkwinkelgeschwindigkeit(t)
"""
def vTcp(qT, vT, dh_para):
    
    vTcpT = np.zeros((qT.shape[0],6))
    
    for t in range(qT.shape[0]):
        Jt = jacobi_UR(qT[t], dh_para)
        vTcpT[t] = np.dot(Jt,vT[t])
    
    return vTcpT

"""
Gelenkwinkelgeschwindigkeit(t) = TCP Geschwindigkeit(t) * inverseJakobimatrix(q(t)) 
"""
def vT(qT, xyzrxryrzVT, dh_para):
    
    vT = np.zeros((qT.shape[0],6))
    
    for t in range(qT.shape[0]):
        Jt = jacobi_UR(qT[t], dh_para)
        try:
            Jtinv = np.linalg.inv(Jt)
            vT[t] = np.dot(Jtinv,xyzrxryrzVT[t])
        except:
            vT[t] = np.zeros(6)
                
    
    return vT

def force(qT, rd, dh_para):
    
    forceT = np.zeros((qT.shape[0],6))
    
    for i in range(qT.shape[0]):
        J = jacobi_UR(qT[i], dh_para)
        Jinv = np.linalg.inv(J)
        forceT[i] = np.dot(Jinv, rd)
        
    return forceT


def singular(qT, dh_para):
    
    singularT = np.zeros(qT.shape[0])
    
    for i in range(qT.shape[0]):
        J = jacobi_UR(qT[i], dh_para)
        singularT[i] = np.linalg.det(J)
        
    return singularT


def plotVTcp(vTcpT,t):
    
    # plot
    fig1 = plt.figure().gca()
    try:
        fig1.plot(t, vTcpT[:,0], color='r', label='dX')
        fig1.plot(t, vTcpT[:,1], color='g', label='dY')
        fig1.plot(t, vTcpT[:,2], color='b', label='dZ')
    except:
        return 1
        
    fig1.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig1.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("Pose Geschwindigkeit XYZ")
    plt.ylabel('Geschwindigkeit in mm/s')
    plt.xlabel('Zeit in s')
    plt.legend()
    #plt.show()
    
    
    fig2 = plt.figure().gca()
    try:
        
        fig2.plot(t, vTcpT[:,3], color='c', label='drx')
        fig2.plot(t, vTcpT[:,4], color='magenta', label='dry')
        fig2.plot(t, vTcpT[:,5], color='orange', label='drz')
    except:
        return 2
    
    fig2.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig2.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("Pose Geschwindigkeit rxryrz")
    plt.ylabel('drxryrz in Rad/s')
    plt.xlabel('Zeit in s')
    plt.legend()
    #plt.show()
    
    return 0

def plotQd(vTcpT,t):
    fig2 = plt.figure().gca()
    try:
        fig2.plot(t, vTcpT[:,0], color='r', label='qd0')
        fig2.plot(t, vTcpT[:,1], color='g', label='qd1')
        fig2.plot(t, vTcpT[:,2], color='b', label='qd2')
        fig2.plot(t, vTcpT[:,3], color='c', label='qd3')
        fig2.plot(t, vTcpT[:,4], color='magenta', label='qd4')
        fig2.plot(t, vTcpT[:,5], color='orange', label='qd5')
    except:
        return 2
    
    fig2.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig2.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("Gelenkwinkelgeschindigkeit")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s')
    plt.xlabel('Zeit in s')
    plt.legend()
    #plt.show()
    #plt.savefig('png/' + filename + '_qd.png')

def plotForce(forceT,t):
    
    fig1 = plt.figure().gca()
    try:
        fig1.plot(t, forceT[:,0], color='r', label='fq1')
        fig1.plot(t, forceT[:,1], color='g', label='fq2')
        fig1.plot(t, forceT[:,2], color='b', label='fq3')
        fig1.plot(t, forceT[:,3], color='c', label='fq4')
        fig1.plot(t, forceT[:,4], color='magenta', label='fq5')
        fig1.plot(t, forceT[:,5], color='orange', label='fq6')
    except:
        return 2
    
    fig1.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig1.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("Axes Force")
    plt.ylabel('Force in N')
    plt.xlabel('Zeit in s')
    plt.legend()
    #plt.show()
    return 0
    
def plotSingular(singularT,t):
    print("plot")
    
    fig1 = plt.figure().gca()
    try:
        fig1.plot(t, singularT[:], color='c', label='singularity')
    except:
        return 2
    
    fig1.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig1.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("Pose Singularity")
    plt.ylabel('Singularity')
    plt.xlabel('Zeit in s')
    plt.legend()
    #plt.show()
    return  0