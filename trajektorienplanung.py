# -*- coding: utf-8 -*-
"""
toDO: keine Winkeländerung!

"""

import numpy as np
import math
import matplotlib.pyplot as plt
import robolib3 as rl
import os

"""
Teil 1:  Trajektorie einzelner Achse
"""

#1. Berechnung Schaltzeitpunkte für qDiff, vMax, aMax einer Achse 
def traj_timestamps(qStart, qTarget, vMax, aMax):    

    qDiff = abs(qTarget - qStart)
    
    qGrenz = (vMax * vMax) / aMax
    #print("qGrenz Rad: ", qGrenz)
    #print("qGrenz Grad: ", qGrenz * 360 / (2 * np.pi))
        
    if qDiff <= qGrenz:
        #Dreieck: tS1 = tS2, tGes
        tS1 =  math.sqrt(qDiff / aMax)
        tS2 = tS1
        tGes = 2 * tS1
        
        #tGes = math.sqrt((4 * qDiff) / aMax)
        #tS1 = tGes/2
        #tS2 = tS1
		
    else:
        #Trapez: tS1, tS2, tGes
        tGes = (vMax / aMax) + (qDiff / vMax)
        tS1 = vMax / aMax
        tS2 = tGes - tS1
    
    return [tS1, tS2, tGes]

def traj_PoseTimestamps(pStart, pTarget, vMax, aMax):
    
    #norm = sqrt(x^2 + y^2 + z^2)
    pDiff = math.sqrt((pStart[0] - pTarget[0])**2 + (pStart[1] - pTarget[1])**2 + (pStart[2] - pTarget[2])**2)
    pGrenz = (vMax * vMax) / aMax
    
    if pDiff <= pGrenz:
        #Dreieck: tS1 = tS2, tGes
        tGes = math.sqrt((4 * pDiff) / aMax)
        tS1 = tGes/2
        tS2 = tS1
		
    else:
        #Trapez: tS1, tS2, tGes
        tGes = (vMax / aMax) + (pDiff / vMax)
        tS1 = vMax / aMax
        tS2 = tGes - tS1
    
    return [tS1, tS2, tGes]


#2. a) Berechnung vNeu, aNeu für vorgegebene Schaltzeitpunkte tS1 + tGes
def traj_getVA(qStart, qTarget, tS1, tGes):
    qDiff = abs(qTarget - qStart)
    
    print((tS1 * tGes - tS1**2))
    
    aNew = qDiff / (tS1 * tGes - tS1**2)
    vNew = aNew * tS1
    
    return [vNew, aNew]
	

def traj_getVAtimestamps(qStart, qTarget, vMax, aMax, tGes):
    #tGes vorgegeben: vMaxNeu
    qDiff = abs(qTarget - qStart)
    aNew = aMax
        
    #NAN check!
    try:
        vNew = (tGes - np.sqrt(tGes*tGes - 4 * qDiff/aMax))/(2/aMax)
    except:
        return [0, 0, 0, 0, 0]
        
    #alternativ
    #tS1 = (tGes * aMax - math.sqrt(tGes * tGes * aMax * aMax - 4 * aMax * qDiff))/ (2 * aMax)
    #vMaxNeu = aMax * tS1
    
    #print("vMaxNeu: ", vMaxNeu)
   
    [tS1, tS2, tGes] = traj_timestamps(qStart, qTarget, vNew, aNew)
    #print(tS1, tS2, tGes)
            
    return [vNew, aNew, tS1, tS2, tGes]


def traj_sample(qStart, qTarget, tS1, tS2, tGes, vMax, aMax, tDelta):
    qDiff = qTarget - qStart
    
    if(qStart > qTarget):
        aMax = - aMax
        vMax = - vMax
    
    t = np.arange(0, tGes + tDelta, tDelta) 
    qT = np.zeros(t.size)
    vT = np.zeros(t.size)
    aT = np.zeros(t.size)
    
    if(tS1 == tS2):
        print("Dreieck")
        i=0
        
        #Paramter Zeitpunkt tS1
        qTS = qStart + 0.5 * aMax * tS1**2
        vTS = aMax * tS1
        #print(vTS)
        #vTS = np.sqrt(aMax * qDiff)
        #print(vTS)
        
        for i in range(t.size):
            
            if(t[i] < tS1):
                #Dreieck steigend
                qT[i] = qStart + 0.5 * aMax * t[i]**2
                vT[i] = aMax * t[i]
                aT[i] = aMax
            else:
                #Dreieck fallend
                qT[i] = qTS + vTS * (t[i] - tS1) - 0.5 * aMax * (t[i] - tS1)**2
                vT[i] = vTS - aMax * (t[i] - tS1) 
                aT[i] = - aMax
                
        
        #print(qT)
        
    else:
        print("Trapez")
        i = 0
        
        if(np.abs(qDiff) < 1e-4):
            #qDiff == 0
            qTS1 = qStart
            qTS2 = qTarget
            
            for i in range(t.size):     
                qT[i] = qStart
                vT[i] = 0
                aT[i] = 0


        else:
            #qDiff > 0
            qTS1 = qStart + 0.5 * aMax * tS1**2
            qTS2 = qTarget - vMax**2 / (2 * aMax)
        
            #qTS1 = qStart + vMax**2 / (2 * aMax)
            #qTS2 = qTS1 + (tS2 - tS1) * vMax
        
            print(0.5 * aMax * tS1**2)
            print(vMax**2 / (2 * aMax))
            print(qTS1)
            print(qTS2)
            
            for i in range(t.size):
                
                if(t[i] < tS1):
                    #Trapez steigend
                    qT[i] = qStart + 0.5 * aMax * t[i]**2
                    vT[i] = aMax * t[i]
                    aT[i] = aMax
                    
                elif(t[i] < tS2):
                    #Trapez konst
                    qT[i] = qTS1 + (t[i] - tS1) * vMax
                    vT[i] = vMax
                    aT[i] = 0
                    
                else:
                    #Trapez fallend
                    qT[i] = qTS2 + (vMax + (aMax * qDiff)/ vMax) * (t[i] - tS2) - 0.5 * aMax * (t[i]**2 - tS2**2)
                    vT[i] = - aMax * t[i] + vMax + (aMax * qDiff) / vMax
                    aT[i] = - aMax
    
        
    return[qT, vT, aT, t]


def traj_samplePose(pStart, pTarget, vMax, aMax, tDelta):
    
    [tS1, tS2, tGes] =  traj_PoseTimestamps(pStart, pTarget, vMax, aMax)
    
    pDiff = np.sqrt((pStart[0] - pTarget[0])**2 + (pStart[1] - pTarget[1])**2 + (pStart[2] - pTarget[2])**2)
    
    direction = pTarget[0:3] - pStart[0:3]
    length = np.sqrt((direction[0]**2) + (direction[1]**2) + (direction[2]**2))
    gradient = direction / length
    
    """
    x = 5
    linEq = pStart[0:3] + x * gradient
    print(linEq)
    """
    
    t = np.arange(0, tGes + tDelta, tDelta)
    xyzrxryrzT = np.zeros([t.size,6])
    vT = np.zeros(t.size)
    aT = np.zeros(t.size)
    
    if(tS1 == tS2):
        print("Dreieck")
        i=0
        
        #Paramter Zeitpunkt tS1
        xyzrxryrzTs = np.zeros(3)
        xyzrxryrzTs[0:3] = pStart[0:3] + 0.5 * aMax * (tS1**2) * gradient
        vTs = aMax * tS1
        #print(vTS)
        #vTS = np.sqrt(aMax * qDiff)
        #print(vTS)
        
        for i in range(t.size):
            
            if(t[i] < tS1):
                #Dreieck steigend
                xyzrxryrzT[i,0:3] = pStart[0:3] + 0.5 * aMax * (tS1**2) * gradient
                xyzrxryrzT[i,3:6] = pStart[3:6]
                vT[i] = aMax * t[i]
                aT[i] = aMax
            else:
                #Dreieck fallend
                xyzrxryrzT[i,0:3] = xyzrxryrzTs[0:3] + (vTs * (t[i] - tS1) - 0.5 * aMax * ((t[i] - tS1)**2)) * gradient
                xyzrxryrzT[i,3:6] = pStart[3:6]
                vT[i] = vTs - aMax * (t[i] - tS1) 
                aT[i] = - aMax
                
        
        #print(qT)
        
    else:
        print("Trapez")
        i = 0
        
        if(np.abs(pDiff) < 1e-4):
            #qDiff == 0
            
            for i in range(t.size):     
                xyzrxryrzT[i,0:3] = pStart[0:3]
                xyzrxryrzT[i,3:6] = pStart[3:6]
                vT[i] = 0
                aT[i] = 0


        else:
            #qDiff > 0
            xyzrxryrzTs1 = np.zeros(3)
            xyzrxryrzTs2 = np.zeros(3)
            xyzrxryrzTs1[0:3] = pStart[0:3] + 0.5 * aMax * (tS1**2) * gradient
            xyzrxryrzTs2[0:3] = pTarget[0:3] - (vMax**2 / (2 * aMax)) * gradient
        
            #qTS1 = qStart + vMax**2 / (2 * aMax)
            #qTS2 = qTS1 + (tS2 - tS1) * vMax
        
            print(0.5 * aMax * tS1**2)
            print(vMax**2 / (2 * aMax))
            print(xyzrxryrzTs1[0:3])
            print(xyzrxryrzTs2[0:3])
            
            for i in range(t.size):
                
                if(t[i] < tS1):
                    #Trapez steigend
                    xyzrxryrzT[i,0:3] = pStart[0:3] + (0.5 * aMax * t[i]**2) * gradient
                    xyzrxryrzT[i,3:6] = pStart[3:6]
                    vT[i] = aMax * t[i]
                    aT[i] = aMax
                    
                elif(t[i] < tS2):
                    #Trapez konst
                    xyzrxryrzT[i,0:3] = xyzrxryrzTs1[0:3] + ((t[i] - tS1) * vMax) * gradient
                    xyzrxryrzT[i,3:6] = pStart[3:6]
                    vT[i] = vMax
                    aT[i] = 0
                    
                else:
                    #Trapez fallend
                    xyzrxryrzT[i,0:3] = xyzrxryrzTs2[0:3] + ((vMax + (aMax * pDiff)/ vMax) * (t[i] - tS2)  - 0.5 * aMax * (t[i]**2 - tS2**2)) * gradient
                    xyzrxryrzT[i,3:6] = pStart[3:6]
                    vT[i] = - aMax * t[i] + vMax + (aMax * pDiff) / vMax
                    aT[i] = - aMax
    
        
    return[xyzrxryrzT, vT, aT, t]
    
    
"""
Teil 2: mehrere Achsen synchronisieren
"""

def leadingAxisTimestamps(qStart, qTarget, vMax, aMax):
    
    tGesLead = 0
    axis = 0
    leadingAxis = 0 
    
    for axis in range(qStart.size):
        [tS1Temp, tS2Temp, tGesTemp] = traj_timestamps(qStart[axis],qTarget[axis],vMax[axis],aMax[axis])
        
        if(tGesTemp > tGesLead):
            [tS1Lead, tS2Lead, tGesLead] = [tS1Temp, tS2Temp, tGesTemp]
            leadingAxis = axis
    
    return[tS1Lead, tS2Lead, tGesLead, leadingAxis]
    
    
def followingAxesVA(qStart, qTarget, tS1Lead, tS2Lead, tGesLead):
    
    vNew = np.zeros(qStart.size)
    aNew = np.zeros(qStart.size)
    axis = 0
    
    for axis in range(qStart.size):
       [vNew[axis],aNew[axis]] = traj_getVA(qStart[axis], qTarget[axis], tS1Lead, tGesLead)
    
    return [vNew, aNew]


def traj_sampleAxes(qStart, qTarget, vMax, aMax, tDelta):
    
    [tS1Lead, tS2Lead, tGesLead, leadingAxis] = leadingAxisTimestamps(qStart, qTarget, vMax, aMax)
    
    [vNew, aNew] = followingAxesVA(qStart, qTarget, tS1Lead, tS2Lead, tGesLead)
    
    t = np.arange(0, tGesLead + tDelta, tDelta)
    qT = np.zeros([t.size,qStart.size])
    vT = np.zeros([t.size,qStart.size])
    aT = np.zeros([t.size,qStart.size])
    
    for axis in range(qStart.size):
       [qT[:,axis], vT[:,axis], aT[:,axis], t] = traj_sample(qStart[axis], qTarget[axis], tS1Lead, tS2Lead, tGesLead, vNew[axis], aNew[axis], tDelta)
          
    return[qT, vT, aT, t]
     

def traj_samplePoseFk(qT, dhPara):
    
    xyzrxryrz = np.zeros((qT.shape[0],6))
    T = np.zeros((4,4))
    
    for i in range(qT.shape[0]):
         T = rl.fk_ur(dhPara,qT[i,:])
         xyzrxryrz[i,:] = rl.T_2_rotvec(T)
    
    return xyzrxryrz

def traj_sampleAxesIk(tcpT, dhParaUR3, sol):
    
    qT = np.zeros((tcpT.shape[0],6))
    
    print(tcpT.shape[0])
    
    """
    for i in range(8):
        try:
            qT[i,:] = rl.ik_ur(dhParaUR3, tcpT[0,:],i)
            print(qT[i,:])
        except:
                print("fail")
    """
    
    
    try:
        for i in range(tcpT.shape[0]):
            qT[i,:] = rl.ik_ur(dhParaUR3, tcpT[i,:],sol)
            
            #Korrektur movel_x400
            q4 = qT[i,3]
            if np.abs(q4) >= (np.pi):
                q4 = q4 - np.pi
            if np.abs(q4) >= (np.pi):
                q4 = q4 - np.pi
            qT[i,3] = q4
            
    except:
        #print("Fail")
        return 0
        
    
    #qIK = rl.ik_ur(dhParaUR3, rotvecQ, sol)
    #print("sol:", sol, qIK)
    
    return qT

"""
Teil 2B: mehrere Achsen synchronisieren mit Zeitvorgabe
"""

# Berechnung vNeu, aNeu und Schaltzeitpunkte für vorgegebenes tGes
def traj_TimegetVATimestamps(qStart, qTarget, vMax, aMax, time):
    #tGes vorgegeben: vMaxNeu
    vNew    =    np.zeros(qStart.size)
    aNew    =    np.zeros(qStart.size)
    tS1     =    np.zeros(qStart.size)
    tS2     =    np.zeros(qStart.size)
    tGes    =    np.zeros(qStart.size)
    
    #1. Parameter Führungachse == langsamste Achse
    [tS1Lead, tS2Lead, tGesLead, leadingAxis] = leadingAxisTimestamps(qStart, qTarget, vMax, aMax)
    
    if(tGesLead > time):
        #vorgegebenes tGes zu klein
        return [0, 0, 0, 0]
    
    
    #2.Fuehrungsachse an tGes anpassen
    if(tS1Lead == tS2Lead):
        #Dreieck:
        tS1[leadingAxis] = time/2
        tS2[leadingAxis] = tS1[leadingAxis]
        [vNew[leadingAxis], aNew[leadingAxis]] = traj_getVA(qStart[leadingAxis], qTarget[leadingAxis], tS1[leadingAxis], time)
    else:
        #Trapez:
        [vNew[leadingAxis], aNew[leadingAxis], tS1[leadingAxis], tS2[leadingAxis], tGes[leadingAxis]] = traj_getVAtimestamps(qStart[leadingAxis], qTarget[leadingAxis], vMax[leadingAxis], aMax[leadingAxis], time)
        
    
    #3. restliche Achsen an Führungsachse anpassen
    axis = 0
    for axis in range(qStart.size):
            
        if(axis != leadingAxis):
            [vNew[axis],aNew[axis]] = traj_getVA(qStart[axis], qTarget[axis], tS1[leadingAxis], time)
            
            if( (np.abs(vNew[axis]) < 1e-4) or (np.abs(aNew[axis]) < 1e-4) ):
                #keine Winkeländerung
                vNew[axis] = 0
                aNew[axis] = 0
                tS1[axis] = tS1[leadingAxis]
                tS2[axis] = tS2[leadingAxis]
                tGes[axis] = time
                    
                #print("vaNeu: ",vNew[axis], aNew[axis], tS1[axis], tS2[axis], tGes[axis])
                
            else:  
                #Zeitbedingung eingehalten: synchrone Trapeztrajektorie mit tS1, tS2, tGes
                tS1[axis] = tS1[leadingAxis]
                tS2[axis] = tS2[leadingAxis]
                tGes[axis] = tGes[leadingAxis]
                
    return [vNew, aNew, tS1, tS2, tGes]


def traj_sampleAxesTime(qStart, qTarget, vMax, aMax, time, tDelta):
    
    vNew = np.zeros(qStart.size)
    aNew = np.zeros(qStart.size)
    tS1 = np.zeros(qStart.size)
    tS2 = np.zeros(qStart.size)
    tGes = np.zeros(qStart.size)
    
    t = np.arange(0, time + tDelta, tDelta)
    qT = np.zeros([t.size,qStart.size])
    vT = np.zeros([t.size,qStart.size])
    aT = np.zeros([t.size,qStart.size])
    
    [vNew, aNew, tS1, tS2, tGes] = traj_TimegetVATimestamps(qStart, qTarget, vMax, aMax, time)

    for axis in range(qStart.size):
        [qT[:,axis], vT[:,axis], aT[:,axis], t] = traj_sample(qStart[axis], qTarget[axis], tS1[axis], tS2[axis], time, vNew[axis], aNew[axis], tDelta)
          
    return[qT, vT, aT, t]
    

"""
Teil 3: Trajektorien Plotten
"""
def plotTrajAxes(qT, vT, aT, t):
    
    c = np.array(['r','g','b','c','magenta','orange'])
    lq = np.array(['q0','q1','q2','q3','q4','q5'])
    lqd = np.array(['qd0','qd1','qd2','qd3','qd4','qd5'])
    lqdd = np.array(['qdd0','qdd1','qdd2','qdd3','qdd4','qdd5'])
    
    plt.figure()
    #plt.plot(t,qT,color=c, label=l)
    try:
        for axis in range(6):
            plt.plot(t, qT[:,axis], color=c[axis], label=lq[axis])
    except:
        return axis
    
    plt.grid(True)
    plt.title("Gelenkwinkel")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    
    plt.figure()
    try:
        for axis in range(6):
            plt.plot(t, vT[:,axis], color=c[axis], label=lqd[axis])
    except:
        return axis
    
    plt.grid(True)
    plt.title("Winkelgeschindigkeit")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    plt.figure()
    try:
        for axis in range(6):
            plt.plot(t, aT[:,axis], color=c[axis], label=lqdd[axis])
    except:
        return axis
    
    plt.grid(True)
    plt.title("Winkelbeschleunigung")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s**2')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    return 0


def plotTrajPoseFk(xyzrxryrzT, t):
    
    # plot
    plt.figure()
    try:
        plt.plot(t, xyzrxryrzT[:,0], color='r', label='X')
        plt.plot(t, xyzrxryrzT[:,1], color='g', label='Y')
        plt.plot(t, xyzrxryrzT[:,2], color='b', label='Z')
    except:
        return 1
        
    plt.grid(True)
    plt.title("Pose XYZ")
    plt.ylabel('XYZ in m')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    
    plt.figure()
    try:
        plt.plot(t, xyzrxryrzT[:,3], color='c', label='rx')
        plt.plot(t, xyzrxryrzT[:,4], color='magenta', label='ry')
        plt.plot(t, xyzrxryrzT[:,5], color='orange', label='rz')
    except:
        return 2
        
    plt.grid(True)
    plt.title("Pose rxryrz")
    plt.ylabel('rxryrz in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    return 0

def plotTrajPose(xyzrxryrzT, vTcPT, aTcpT, t):
    # plot
    plt.figure()
    try:
        plt.plot(t, xyzrxryrzT[:,0], color='r', label='X')
        plt.plot(t, xyzrxryrzT[:,1], color='g', label='Y')
        plt.plot(t, xyzrxryrzT[:,2], color='b', label='Z')
    except:
        return 1
        
    plt.grid(True)
    plt.title("Pose XYZ")
    plt.ylabel('XYZ in mm')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    
    plt.figure()
    try:
        plt.plot(t, xyzrxryrzT[:,3], color='c', label='rx')
        plt.plot(t, xyzrxryrzT[:,4], color='magenta', label='ry')
        plt.plot(t, xyzrxryrzT[:,5], color='orange', label='rz')
    except:
        return 2
        
    plt.grid(True)
    plt.title("Pose rxryrz")
    plt.ylabel('rxryrz in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    
    plt.figure()
    try:
        plt.plot(t, vTcPT[:], color='r', label='vTCP')
    except:
        return 3
    
    plt.grid(True)
    plt.title("TCP Geschindigkeit")
    plt.ylabel('Geschwindigkeit in mm/s')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    plt.figure()
    try:
        plt.plot(t, aTcpT[:], color='r', label='aTCP')
    except:
        return 4
    
    plt.grid(True)
    plt.title("TCP Beschleunigung")
    plt.ylabel('Beschleunigung in mm/ s**2')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    return 0

def plotTrajAxesIk(qT,  t):
    
    c = np.array(['r','g','b','c','magenta','orange'])
    lq = np.array(['q0','q1','q2','q3','q4','q5'])

    plt.figure()
    #plt.plot(t,qT,color=c, label=l)
    try:
        for axis in range(6):
            plt.plot(t, qT[:,axis], color=c[axis], label=lq[axis])
    except:
        return axis
    
    plt.grid(True)
    plt.title("Gelenkwinkel")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    return 0

"""
Teil 4: CSV Files
"""
#nur Python 3.6: größe np.array Problem in 2.7
#def writeCSV(qT, vT, aT, xyzrxryrz, t, filenameCSV):
def writeCSV(qT, vT, aT, xyzrxryrzT, t, filenameCSV):
    #"exampleCsv.csv" # directory relative to script
    
    csv = open('csv/' + filenameCSV, "w")  #open File in write mode
    
    axNum = qT.shape[1]
    
    #print("CSV: ",qT.shape)
    if(axNum == 1):
        csv.write("timestamp target_q_0 target_qd_0 target_qdd_0\n")
    elif(axNum == 6):
        csv.write("timestamp target_q_0 target_q_1 target_q_2 target_q_3 target_q_4 target_q_5 target_qd_0 target_qd_1 target_qd_2 target_qd_3 target_qd_4 target_qd_5 target_qdd_0 target_qdd_1 target_qdd_2 target_qdd_3 target_qdd_4 target_qdd_5 actual_TCP_pose_0 actual_TCP_pose_1 actual_TCP_pose_2 actual_TCP_pose_3 actual_TCP_pose_4 actual_TCP_pose_5\n")
    else:
        return 1

    
    for timestamp in range(t.size):
        
        #1. timestamp
        time = np.float32(t[timestamp])
        csv.write(str(time) + " ")
        
        #2. q_X
        for axis in range(axNum):
            csv.write(str(qT[timestamp,axis]) + " ")
        
        #3. qd_X
        for axis in range(axNum):
            csv.write(str(vT[timestamp,axis]) + " ")
            
        #4. qdd_X
        for axis in range(axNum):
            csv.write(str(aT[timestamp,axis]) + " ")
        
        
        #5- actual_TCP_pose_X
        for para in range(6):
            csv.write(str(xyzrxryrzT[timestamp,para]) + " ")
        
            
        csv.write("\n")
        
    return 0


def writeCSVTcp(qT, xyzrxryrzT, vTcpT, aTcpT, t, filenameCSV):
    #"exampleCsv.csv" # directory relative to script
    
    csv = open('csv/' + filenameCSV, "w")  #open File in write mode
    
    axNum = qT.shape[1]
    
    #print("CSV: ",qT.shape)
    if(axNum == 6):
        csv.write("timestamp target_q_0 target_q_1 target_q_2 target_q_3 target_q_4 target_q_5 actual_TCP_pose_0 actual_TCP_pose_1 actual_TCP_pose_2 actual_TCP_pose_3 actual_TCP_pose_4 actual_TCP_pose_5 actual_TCP_v actual_TCP_a\n")
    else:
        return 1

    
    for timestamp in range(t.size):
        
        #1. timestamp
        time = np.float32(t[timestamp])
        csv.write(str(time) + " ")
        
        #2. q_X
        for axis in range(axNum):
            csv.write(str(qT[timestamp,axis]) + " ")
        
        #3. xyzrxryrz
        for para in range(6):
            csv.write(str(xyzrxryrzT[timestamp,para]) + " ")
            
        #4. vTcp
        csv.write(str(vTcpT[timestamp]) + " ")
        
        
        #5- aTcp
        csv.write(str(aTcpT[timestamp]) + " ")
        
            
        csv.write("\n")
        
    return 0


#plotCSV: python2.7
import csv_reader

def plotCSV(filenameCSV):
    
    filename = os.path.splitext(filenameCSV)[0]
    
    with open(('csv/' + filenameCSV)) as csvfile:
        r = csv_reader.CSVReader(csvfile)

    # Axes
    plt.figure()
    try:
        plt.plot(r.timestamp, r.target_q_0, color='r', label='q0')
        plt.plot(r.timestamp, r.target_q_1, color='g', label='q1')
        plt.plot(r.timestamp, r.target_q_2, color='b', label='q2')
        plt.plot(r.timestamp, r.target_q_3, color='c', label='q3')
        plt.plot(r.timestamp, r.target_q_4, color='magenta', label='q4')
        plt.plot(r.timestamp, r.target_q_5, color='orange', label='q5')
    except:
        return 1
        
    plt.grid(True)
    plt.title("Gelenkwinkel")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_q.png')
    
    
    plt.figure()
    try:
        plt.plot(r.timestamp, r.target_qd_0, color='r', label='qd0')
        plt.plot(r.timestamp, r.target_qd_1, color='g', label='qd1')
        plt.plot(r.timestamp, r.target_qd_2, color='b', label='qd2')
        plt.plot(r.timestamp, r.target_qd_3, color='c', label='qd3')
        plt.plot(r.timestamp, r.target_qd_4, color='magenta', label='qd4')
        plt.plot(r.timestamp, r.target_qd_5, color='orange', label='qd5')
    except:
        return 2
    
    plt.grid(True)
    plt.title("Winkelgeschindigkeit")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_qd.png')
    
    
    plt.figure()
    try:
        plt.plot(r.timestamp, r.target_qdd_0, color='r', label='qdd0')
        plt.plot(r.timestamp, r.target_qdd_1, color='g', label='qdd1')
        plt.plot(r.timestamp, r.target_qdd_2, color='b', label='qdd2')
        plt.plot(r.timestamp, r.target_qdd_3, color='c', label='qdd3')
        plt.plot(r.timestamp, r.target_qdd_4, color='magenta', label='qdd4')
        plt.plot(r.timestamp, r.target_qdd_5, color='orange', label='qdd5')
    except:
        return 3
    
    plt.grid(True)
    plt.title("Winkelbeschleunigung")
    plt.ylabel('Winkelbeschleunigung in Rad / s**2')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_qdd.png')
    
    
    #Pose
    plt.figure()
    try:
        plt.plot(r.timestamp, r.actual_TCP_pose_0, color='r', label='X')
        plt.plot(r.timestamp, r.actual_TCP_pose_1, color='g', label='Y')
        plt.plot(r.timestamp, r.actual_TCP_pose_2, color='b', label='Z')
    except:
        return 4
        #nothing to do
    plt.grid(True)
    plt.title("Pose XYZ")
    plt.ylabel('XYZ in m')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_XYZ.png')
    
    
    
    plt.figure()
    try:
        plt.plot(r.timestamp, r.actual_TCP_pose_3, color='c', label='rx')
        plt.plot(r.timestamp, r.actual_TCP_pose_4, color='magenta', label='ry')
        plt.plot(r.timestamp, r.actual_TCP_pose_5, color='orange', label='rz')
    except:
        return 5
        #nothing to do
    plt.grid(True)
    plt.title("Pose rxryrz")
    plt.ylabel('rxryrz in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_rxryrz.png')
    return 0


#plotCSVTcp: python2.7
def plotCSVTcp(filenameCSV):
    
    filename = os.path.splitext(filenameCSV)[0]
    
    with open(('csv/' + filenameCSV)) as csvfile:
        r = csv_reader.CSVReader(csvfile)

     # Axes
    plt.figure()
    try:
        plt.plot(r.timestamp, r.target_q_0, color='r', label='q0')
        plt.plot(r.timestamp, r.target_q_1, color='g', label='q1')
        plt.plot(r.timestamp, r.target_q_2, color='b', label='q2')
        plt.plot(r.timestamp, r.target_q_3, color='c', label='q3')
        plt.plot(r.timestamp, r.target_q_4, color='magenta', label='q4')
        plt.plot(r.timestamp, r.target_q_5, color='orange', label='q5')
    except:
        return 1
        
    plt.grid(True)
    plt.title("Gelenkwinkel")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_q.png')
    
        
    #Pose
    plt.figure()
    try:
        plt.plot(r.timestamp, r.actual_TCP_pose_0, color='r', label='X')
        plt.plot(r.timestamp, r.actual_TCP_pose_1, color='g', label='Y')
        plt.plot(r.timestamp, r.actual_TCP_pose_2, color='b', label='Z')
    except:
        return 2
        #nothing to do
    plt.grid(True)
    plt.title("Pose XYZ")
    plt.ylabel('XYZ in mm')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_XYZ.png')
    
    
    
    plt.figure()
    try:
        plt.plot(r.timestamp, r.actual_TCP_pose_3, color='c', label='rx')
        plt.plot(r.timestamp, r.actual_TCP_pose_4, color='magenta', label='ry')
        plt.plot(r.timestamp, r.actual_TCP_pose_5, color='orange', label='rz')
    except:
        return 4
        #nothing to do
    plt.grid(True)
    plt.title("Pose rxryrz")
    plt.ylabel('rxryrz in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_rxryrz.png')
    
    
    plt.figure()
    try:
        plt.plot(r.timestamp, r.actual_TCP_v, color='r', label='vTcp')
    except:
        return 5
        #nothing to do
    plt.grid(True)
    plt.title("Tcp Geschwindigkeit")
    plt.ylabel('Tcp Geschwindigkeit in mm/s')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Tcp_v.png')
    
    
    
    plt.figure()
    try:
        plt.plot(r.timestamp, r.actual_TCP_a, color='c', label='aTcp')
    except:
        return 6
        #nothing to do
    plt.grid(True)
    plt.title("Tcp Beschleunigung")
    plt.ylabel('Tcp Beschleunigung in mm / s**2')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_TCP_a.png')
    
    return 0

    

"""
Append: Trapezverlauf mit 25% tGes Beschleunigung
"""

def trajektorie25aMax(qStart, qTarget, vMax, aMax, tGes):
    
    qDiff = abs(qTarget - qStart)
    
    tS1 = tGes / 4
    tS2 = tGes - tS1
    
    aMaxNeu = (qDiff * 16) / ( 3 * tGes**2)
    vMaxNeu = aMaxNeu * tS1 
    
    if((aMaxNeu > aMax) or (vMaxNeu > vMax)):
        vMaxNeu = 0
        aMaxNeu = 0
    
    return [vMaxNeu, aMaxNeu, tS1, tS2]

def trajektorie25Gesamtzeit(qStart,qTarget,vMax,aMax):
    
    qDiff = abs(qTarget - qStart)
    
    #1. Versuch 25% aMax
    tGes = math.sqrt((qDiff * 16) / (3 * aMax))
    aMaxNeu = aMax
    vMaxNeu = 0.25 * tGes * aMax
        
    #2. Versuch aMaxNeu < aMax --> tGesNeu > tGes
    if(vMaxNeu > vMax):
        tGes = (qDiff * 16) / (12 * vMax)
        aMaxNeu = (qDiff * 16) / (tGes* tGes * 3)
        vMaxNeu = vMax
    
    return [vMaxNeu, aMaxNeu, tGes]

def trajektorieFuehrungsachse25Gesamtzeit(qStart,qTarget,vMax,aMax):
    
    tQFuehrung = np.array([0,0,0])
    Achse = 0
    Fuehrungsachse = 0 
    
    for Achse in range(qStart.size):
        tQtemp = trajektorie25Gesamtzeit(qStart[Achse],qTarget[Achse],vMax[Achse],aMax[Achse])
        #print(tQtemp)
        
        if(tQtemp[2] > tQFuehrung[2]):
            tQFuehrung = tQtemp
            Fuehrungsachse = Achse + 1
    
    tGesFuehrung = tQFuehrung[2]
    
    return [tGesFuehrung, Fuehrungsachse]


def trajektorieFuehrungsachse25(qStart, qTarget, vMax, aMax):
   
    vMaxNeu =    np.zeros(qStart.size)
    aMaxNeu =    np.zeros(qStart.size)
    tS1     =    np.zeros(qStart.size)
    tS2     =    np.zeros(qStart.size)
    tGes    =    np.zeros(qStart.size)
    
    #1. Parameter Führungachse == langsamste Achse
    tQFuehrung = trajektorieFuehrungsachse25Gesamtzeit(qStart, qTarget, vMax, aMax)
    
    tGesFuehrung = tQFuehrung[0]
    
    #2. Achsen an tGes Fuehrungsachse anpassen
    Achse = 0
    for Achse in range(qStart.size):
        vMaxNeu[Achse], aMaxNeu[Achse], tS1[Achse], tS2[Achse] = trajektorie25aMax(qStart[Achse],qTarget[Achse],vMax[Achse],aMax[Achse], tGesFuehrung)
        tGes[Achse] = tGesFuehrung
        
        if((vMaxNeu[Achse] == 0) or (aMaxNeu[Achse] == 0)):
            #todo: Fehlerbehandlung: extra Verlauf berechnen
            print("Fehler: 25% nicht möglich für Achse: ", Achse)
    
    return [vMaxNeu, aMaxNeu, tS1, tS2, tGes]
