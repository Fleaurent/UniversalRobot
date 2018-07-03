# -*- coding: utf-8 -*-
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import robolib as rl
import os


"""
Teil 1:  Berechnung Parameter
"""
#1. Berechnung Schaltzeitpunkte [tS1, tS2, tGes] für qStart, qTarget, vMax, aMax (Gelenkwinkel) 
def traj_timestamps(qStart, qTarget, vMax, aMax):    

    qDiff = abs(qTarget - qStart)
    qGrenz = (vMax * vMax) / aMax

        
    if qDiff <= qGrenz:
        #Dreieck: tS1 = tS2, tGes
        tS1 =  math.sqrt(qDiff / aMax)
        tS2 = tS1
        tGes = 2 * tS1
        
		#alternativ
        #tGes = math.sqrt((4 * qDiff) / aMax)
        #tS1 = tGes/2
        #tS2 = tS1
		
    else:
        #Trapez: tS1, tS2, tGes
        tGes = (vMax / aMax) + (qDiff / vMax)
        tS1 = vMax / aMax
        tS2 = tGes - tS1
    
    return [tS1, tS2, tGes]

#2. Berechnung Schaltzeitpunkte [tS1, tS2, tGes] für pStart, pTarget, vMax, aMax (Arbeitsraum)
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


#3. Berechnung [vNew, aNew] für qDiff mit Schaltzeitpunkten tS1 + tGes
def traj_getVA(qStart, qTarget, tS1, tGes):
    qDiff = abs(qTarget - qStart)
    
    print((tS1 * tGes - tS1**2))
    
    aNew = qDiff / (tS1 * tGes - tS1**2)
    vNew = aNew * tS1
    
    return [vNew, aNew]
	
#4. Berechnung [vNew, aNew, tS1, tS2, tGes] für qDiff mit vMax, aMax,tGes
def traj_getVAtimestamps(qStart, qTarget, vMax, aMax, tGes):
    #tGes vorgegeben: vNew gesucht
    qDiff = abs(qTarget - qStart)
    aNew = aMax
        
    #NAN check!
    try:
        vNew = (tGes - np.sqrt(tGes*tGes - 4 * qDiff/aMax))/(2/aMax)
    except:
        return [0, 0, 0, 0, 0]
    
    [tS1, tS2, tGes] = traj_timestamps(qStart, qTarget, vNew, aNew)
	
	#alternativ
    #tS1 = (tGes * aMax - math.sqrt(tGes * tGes * aMax * aMax - 4 * aMax * qDiff))/ (2 * aMax)
    #vMaxNeu = aMax * tS1
            
    return [vNew, aNew, tS1, tS2, tGes]

"""
Teil 2:  sample Trajektorie
"""
#1. Sample Gelenkwinkel Trajektorie --> [qT, vT, aT, t]
def traj_sample(qStart, qTarget, tS1, tS2, tGes, vMax, aMax, tDelta):

    qDiff = qTarget - qStart
    
    if(qStart > qTarget):
        aMax = - aMax
        vMax = - vMax
    
    t = np.arange(0, tGes + tDelta, tDelta) 
    qT = np.zeros(t.size)
    vT = np.zeros(t.size)
    aT = np.zeros(t.size)
    
	#a) keine Änderung Gelenkwinkel
    if(np.abs(qDiff) < 1e-4):
        #qDiff == 0
        qTS1 = qStart
        qTS2 = qTarget
        
        for i in range(t.size):     
            qT[i] = qStart
            vT[i] = 0
            aT[i] = 0
    
	#b) Dreieckverlauf Trajektorie    
    elif(tS1 == tS2):
        #qDiff > 0
        i=0
        
        #Paramter Zeitpunkt tS1
        qTS = qStart + 0.5 * aMax * tS1**2
        vTS = aMax * tS1
        
		#für jeden sample: q(t), v(t), a(t)
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
                
    #c) Trapezverlauf Trajektorie 
    else:
        #qDiff > 0
        i = 0
        
        qTS1 = qStart + 0.5 * aMax * tS1**2
        qTS2 = qTarget - vMax**2 / (2 * aMax)
    
		#alternativ
        #qTS1 = qStart + vMax**2 / (2 * aMax)
        #qTS2 = qTS1 + (tS2 - tS1) * vMax
  
        #für jeden sample: q(t), v(t), a(t)
        for i in range(t.size):
            
            if(t[i] < tS1):
                #Trapez Phase 1: Beschleunigung
                qT[i] = qStart + 0.5 * aMax * t[i]**2
                vT[i] = aMax * t[i]
                aT[i] = aMax
                
            elif(t[i] < tS2):
                #Trapez Phase 2: konstante Geschwindigkeit
                qT[i] = qTS1 + (t[i] - tS1) * vMax
                vT[i] = vMax
                aT[i] = 0
                
            else:
                #Trapez Phase 2: Abbremsen
                qT[i] = qTS2 + (vMax + (aMax * qDiff)/ vMax) * (t[i] - tS2) - 0.5 * aMax * (t[i]**2 - tS2**2)
                vT[i] = - aMax * t[i] + vMax + (aMax * qDiff) / vMax
                aT[i] = - aMax
      
    return[qT, vT, aT, t]

	
#2. Sample Trajektorie im Arbeitsraum --> [xyzrxryrzT, xyzrxryrzVT, xyzrxryrzAT, vT, aT, t]
#mit vMax, aMax == TCP begrenzung Bewegung
def traj_samplePose(pStart, pTarget, vMax, aMax, tDelta):
    
    [tS1, tS2, tGes] =  traj_PoseTimestamps(pStart, pTarget, vMax, aMax)
    
	#norm = sqrt(x^2 + y^2 + z^2)
    pDiff = np.sqrt((pStart[0] - pTarget[0])**2 + (pStart[1] - pTarget[1])**2 + (pStart[2] - pTarget[2])**2)
    
	#gradient = normierter Richtungsvektor
    direction = pTarget[0:3] - pStart[0:3]
    length = np.sqrt((direction[0]**2) + (direction[1]**2) + (direction[2]**2))
    gradient = direction / length
    
    
    t = np.arange(0, tGes + tDelta, tDelta)
    xyzrxryrzT = np.zeros([t.size,6])
    xyzrxryrzVT = np.zeros([t.size,6])
    xyzrxryrzAT = np.zeros([t.size,6])
    vT = np.zeros(t.size)
    aT = np.zeros(t.size)
    
	#a) Dreieckverlauf Trajektorie 
    if(tS1 == tS2):
        i=0
        
        #Parameter Zeitpunkt tS1
        xyzrxryrzTs = np.zeros(3)
        xyzrxryrzTs[0:3] = pStart[0:3] + 0.5 * aMax * (tS1**2) * gradient
        vTs = aMax * tS1
        
		#für jeden sample: xyzrxryrz(t), xyzrxryrzV(t), xyzrxryrzA(t)
        for i in range(t.size):
            
            if(t[i] < tS1):
                #Dreieck steigend
                xyzrxryrzT[i,0:3] = pStart[0:3] + 0.5 * aMax * (tS1**2) * gradient
                xyzrxryrzT[i,3:6] = pStart[3:6]
                
                xyzrxryrzVT[i,0:3] = aMax * tS1 * gradient
                xyzrxryrzAT[i,0:3] = aMax * gradient
                
                vT[i] = aMax * t[i]
                aT[i] = aMax
            else:
                #Dreieck fallend
                xyzrxryrzT[i,0:3] = xyzrxryrzTs[0:3] + (vTs * (t[i] - tS1) - 0.5 * aMax * ((t[i] - tS1)**2)) * gradient
                xyzrxryrzT[i,3:6] = pStart[3:6]
                
                xyzrxryrzVT[i,0:3] = vTs - aMax * ((t[i] - tS1)) * gradient
                xyzrxryrzAT[i,0:3] = - aMax * gradient
                vT[i] = vTs - aMax * (t[i] - tS1) 
                aT[i] = - aMax
    
	
    else:
        i = 0
        
		#b) keine Änderung TCP
        if(np.abs(pDiff) < 1e-4):
            #qDiff == 0
            
            for i in range(t.size):     
                xyzrxryrzT[i,0:3] = pStart[0:3]
                xyzrxryrzT[i,3:6] = pStart[3:6]
                vT[i] = 0
                aT[i] = 0

		#c) Trapezverlauf Trajektorie
        else:
            #qDiff > 0
            xyzrxryrzTs1 = np.zeros(3)
            xyzrxryrzTs2 = np.zeros(3)
            xyzrxryrzTs1[0:3] = pStart[0:3] + 0.5 * aMax * (tS1**2) * gradient
            xyzrxryrzTs2[0:3] = pTarget[0:3] - (vMax**2 / (2 * aMax)) * gradient
            
			#für jeden sample: xyzrxryrz(t), xyzrxryrzV(t), xyzrxryrzA(t)
            for i in range(t.size):
                
                if(t[i] < tS1):
                    #Trapez Phase 1: Beschleunigung
                    xyzrxryrzT[i,0:3] = pStart[0:3] + (0.5 * aMax * t[i]**2) * gradient
                    xyzrxryrzT[i,3:6] = pStart[3:6]
                    
                    xyzrxryrzVT[i,0:3] =aMax * t[i] * gradient
                    xyzrxryrzAT[i,0:3] = aMax * gradient
                    
                    vT[i] = aMax * t[i]
                    aT[i] = aMax
                    
                elif(t[i] < tS2):
                    #Trapez Phase 2: konstante Geschwindigkeit
                    xyzrxryrzT[i,0:3] = xyzrxryrzTs1[0:3] + ((t[i] - tS1) * vMax) * gradient
                    xyzrxryrzT[i,3:6] = pStart[3:6]
                    
                    xyzrxryrzVT[i,0:3] = vMax * gradient
                    
                    vT[i] = vMax
                    aT[i] = 0
                    
                else:
                    #Trapez Phase 3: Abbremsen
                    xyzrxryrzT[i,0:3] = xyzrxryrzTs2[0:3] + ((vMax + (aMax * pDiff)/ vMax) * (t[i] - tS2) * gradient  - 0.5 * aMax * (t[i]**2 - tS2**2)) * gradient
                    xyzrxryrzT[i,3:6] = pStart[3:6]
                    
                    xyzrxryrzVT[i,0:3] = (vMax + ((aMax * pDiff)/ vMax)) * gradient - aMax * t[i] * gradient
                    xyzrxryrzAT[i,0:3] = - aMax * gradient
                    
                    vT[i] = - aMax * t[i] + vMax + (aMax * pDiff) / vMax
                    aT[i] = - aMax
     
    return[xyzrxryrzT, xyzrxryrzVT, xyzrxryrzAT, vT, aT, t]
    
    
"""
Teil 3A: Synchronisierung mehrerer Achsen 
"""
#1. return Timestamps [tS1Lead, tS2Lead, tGesLead, leadingAxis] der langsamsten Achse = größtes tGes
def leadingAxisTimestamps(qStart, qTarget, vMax, aMax):
    
    tGesLead = 0
    axis = 0
    leadingAxis = 0 
    
    for axis in range(qStart.size):
        [tS1Temp, tS2Temp, tGesTemp] = traj_timestamps(qStart[axis],qTarget[axis],vMax[axis],aMax[axis])
        
		#Werte nur überschreiben wenn Achse langsamer = größeres tGes
        if(tGesTemp > tGesLead):
            [tS1Lead, tS2Lead, tGesLead] = [tS1Temp, tS2Temp, tGesTemp]
            leadingAxis = axis
    
    return[tS1Lead, tS2Lead, tGesLead, leadingAxis]
    
	
#2. Folgeachsen v, a an Vorgabe Timestamps der Führungachse anpassen
def followingAxesVA(qStart, qTarget, tS1Lead, tS2Lead, tGesLead):
    
    vNew = np.zeros(qStart.size)
    aNew = np.zeros(qStart.size)
    axis = 0
    
    for axis in range(qStart.size):
		#bestimme jeweils v, a für Vorgabe Achsparameter
       [vNew[axis],aNew[axis]] = traj_getVA(qStart[axis], qTarget[axis], tS1Lead, tGesLead)
    
    return [vNew, aNew]

	
#3. Sample Gelenkwinkel Trajektorie für mehrere Achsen --> [qT, vT, aT, t] (alle Achsen)
def traj_sampleAxes(qStart, qTarget, vMax, aMax, tDelta):
    
	#1. Parameter Führungsachse
    [tS1Lead, tS2Lead, tGesLead, leadingAxis] = leadingAxisTimestamps(qStart, qTarget, vMax, aMax)
    
	#2. Folgeachsen an Führungsachse anpassen
    [vNew, aNew] = followingAxesVA(qStart, qTarget, tS1Lead, tS2Lead, tGesLead)
    
    t = np.arange(0, tGesLead + tDelta, tDelta)
    qT = np.zeros([t.size,qStart.size])
    vT = np.zeros([t.size,qStart.size])
    aT = np.zeros([t.size,qStart.size])
    
	#3. jede Achse mit spez. Parametern sample
    for axis in range(qStart.size):
       [qT[:,axis], vT[:,axis], aT[:,axis], t] = traj_sample(qStart[axis], qTarget[axis], tS1Lead, tS2Lead, tGesLead, vNew[axis], aNew[axis], tDelta)
          
    return[qT, vT, aT, t]
     

#4. Sample Pose xyzrxryrzT über gegebene Gelenkwinkel qT: Forwärtskinematik
def traj_samplePoseFk(qT, dhPara):
    
    xyzrxryrzT = np.zeros((qT.shape[0],6))
    T = np.zeros((4,4))
    
    for i in range(qT.shape[0]):
         T = rl.fk_ur(dhPara,qT[i,:])
         xyzrxryrzT[i,:] = rl.T_2_rotvec(T)
    
    return xyzrxryrzT


#5. Sample Gelenkwinkel qT über gegebene Pose xyzrxryrzT: Inverse Kinematik
def traj_sampleAxesIk(xyzrxryrzT, dhParaUR3, sol):
    
    qT = np.zeros((xyzrxryrzT.shape[0],6))
    
    try:
        for i in range(xyzrxryrzT.shape[0]):
            qT[i,:] = rl.ik_ur(dhParaUR3, xyzrxryrzT[i,:],sol) 
            
    except:
        return 0
        
    
    return qT

	
"""
Teil 3B: Synchronisierung mehrerer Achsen mit Zeitvorgabe
"""
#1. Berechnung Parameter vNeu, aNeu, Schaltzeitpunkte für vorgegebenes tGes = time mit Gelenkparametern
def traj_TimegetVATimestamps(qStart, qTarget, vMax, aMax, time):
    #tGes vorgegeben: neues vMaxNeu berechnen
    vNew    =    np.zeros(qStart.size)
    aNew    =    np.zeros(qStart.size)
    tS1     =    np.zeros(qStart.size)
    tS2     =    np.zeros(qStart.size)
    tGes    =    np.zeros(qStart.size)
    
    #1. Parameter Führungachse
    [tS1Lead, tS2Lead, tGesLead, leadingAxis] = leadingAxisTimestamps(qStart, qTarget, vMax, aMax)
    
    if(tGesLead > time):
        #vorgegebenes tGes zu klein
        return [0, 0, 0, 0]
    
    #2.Fuehrungsachse an Zeitvorgabe anpassen
    if(tS1Lead == tS2Lead):
        #Führungsachse Dreiecktrajektorie:
        tS1[leadingAxis] = time/2
        tS2[leadingAxis] = tS1[leadingAxis]
        [vNew[leadingAxis], aNew[leadingAxis]] = traj_getVA(qStart[leadingAxis], qTarget[leadingAxis], tS1[leadingAxis], time)
    else:
        #Führungachse Trapeztrajektorie:
        [vNew[leadingAxis], aNew[leadingAxis], tS1[leadingAxis], tS2[leadingAxis], tGes[leadingAxis]] = traj_getVAtimestamps(qStart[leadingAxis], qTarget[leadingAxis], vMax[leadingAxis], aMax[leadingAxis], time)
        
    
    #3. Folgeachsen an Führungsachse anpassen
    axis = 0
    for axis in range(qStart.size):
            
        if(axis != leadingAxis):
            [vNew[axis],aNew[axis]] = traj_getVA(qStart[axis], qTarget[axis], tS1[leadingAxis], time)
            
			#a) Folgeachse ohne Winkeländerung
            if( (np.abs(vNew[axis]) < 1e-4) or (np.abs(aNew[axis]) < 1e-4) ):
                vNew[axis] = 0
                aNew[axis] = 0
                tS1[axis] = tS1[leadingAxis]
                tS2[axis] = tS2[leadingAxis]
                tGes[axis] = time
            
			#b) Folgeachse synchrone trajektorie mit tS1, tS2, tGes
            else:
                tS1[axis] = tS1[leadingAxis]
                tS2[axis] = tS2[leadingAxis]
                tGes[axis] = tGes[leadingAxis]
                
    return [vNew, aNew, tS1, tS2, tGes]


#2. Sample Gelenkwinkel Trajektorie für mehrere Achsen mit Zeitvorgabe --> [qT, vT, aT, t] (alle Achsen) 
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
    
	#1. Achsen an Parameter anpassen --> v, a
    [vNew, aNew, tS1, tS2, tGes] = traj_TimegetVATimestamps(qStart, qTarget, vMax, aMax, time)
    print(tS1, tS2, tGes)
    
	#2. jede Achse mit spez. Parametern sample
    for axis in range(qStart.size):
        [qT[:,axis], vT[:,axis], aT[:,axis], t] = traj_sample(qStart[axis], qTarget[axis], tS1[axis], tS2[axis], time, vNew[axis], aNew[axis], tDelta)
          
    return[qT, vT, aT, t]
    

"""
Teil 4: Trajektorien Plotten
"""
#1. plot qT, vT, aT Gelenk
def plotTrajAxes(qT, vT, aT, t):
    
    c = np.array(['r','g','b','c','magenta','orange'])
    lq = np.array(['q0','q1','q2','q3','q4','q5'])
    lqd = np.array(['qd0','qd1','qd2','qd3','qd4','qd5'])
    lqdd = np.array(['qdd0','qdd1','qdd2','qdd3','qdd4','qdd5'])
    
    fig1 = plt.figure().gca()
    try:
        for axis in range(6):
            fig1.plot(t, qT[:,axis], color=c[axis], label=lq[axis])
    except:
        return axis
    
    plt.grid(True)
    fig1.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig1.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.title("Gelenkwinkel")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    
	
    fig2 = plt.figure().gca()
    try:
        for axis in range(6):
            fig2.plot(t, vT[:,axis], color=c[axis], label=lqd[axis])
    except:
        return axis
    plt.grid(True)
    fig2.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig2.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.title("Winkelgeschwindigkeit")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s')
    plt.xlabel('Zeit in s')
    plt.legend()

    
    fig3 = plt.figure().gca()
    try:
        for axis in range(6):
            fig3.plot(t, aT[:,axis], color=c[axis], label=lqdd[axis])
    except:
        return axis
    plt.grid(True)
    fig3.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig3.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.title("Winkelbeschleunigung")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s**2')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    return 0

#2. plot xyzrxryrzT Pose
def plotTrajPoseFk(xyzrxryrzT, t):
    
    fig1 = plt.figure().gca()
    try:
        fig1.plot(t, xyzrxryrzT[:,0], color='r', label='X')
        fig1.plot(t, xyzrxryrzT[:,1], color='g', label='Y')
        fig1.plot(t, xyzrxryrzT[:,2], color='b', label='Z')
    except:
        return 1      
    fig1.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig1.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("Pose XYZ")
    plt.ylabel('XYZ in m')
    plt.xlabel('Zeit in s')
    plt.legend()

     
    fig2 = plt.figure().gca()
    try:
        fig2.plot(t, xyzrxryrzT[:,3], color='c', label='rx')
        fig2.plot(t, xyzrxryrzT[:,4], color='magenta', label='ry')
        fig2.plot(t, xyzrxryrzT[:,5], color='orange', label='rz')
    except:
        return 2
        
    fig2.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig2.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("Pose rxryrz")
    plt.ylabel('rxryrz in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    return 0

#3. plot xyzrxryrzT, xyzrxryrzVT, xyzrxryrzAT, vTcPT, aTcpT Pose
def plotTrajPose(xyzrxryrzT, xyzrxryrzVT, xyzrxryrzAT, vTcPT, aTcpT, t):

    fig1 = plt.figure().gca()
    try:
        fig1.plot(t, xyzrxryrzT[:,0], color='r', label='X')
        fig1.plot(t, xyzrxryrzT[:,1], color='g', label='Y')
        fig1.plot(t, xyzrxryrzT[:,2], color='b', label='Z')
    except:
        return 1
    fig1.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig1.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("Pose XYZ")
    plt.ylabel('XYZ in mm')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    
    fig2 = plt.figure().gca()
    try:
        fig2.plot(t, xyzrxryrzT[:,3], color='c', label='rx')
        fig2.plot(t, xyzrxryrzT[:,4], color='magenta', label='ry')
        fig2.plot(t, xyzrxryrzT[:,5], color='orange', label='rz')
    except:
        return 2
    fig2.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig2.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("Pose rxryrz")
    plt.ylabel('rxryrz in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    
    fig3 = plt.figure().gca()
    try:
        fig3.plot(t, vTcPT[:], color='r', label='vTCP')
    except:
        return 3
    fig3.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig3.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("TCP Geschwindigkeit")
    plt.ylabel('Geschwindigkeit in mm/s')
    plt.xlabel('Zeit in s')
    plt.legend()

    
    fig4 = plt.figure().gca()
    try:
        fig4.plot(t, aTcpT[:], color='r', label='aTCP')
    except:
        return 4
    fig4.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig4.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("TCP Beschleunigung")
    plt.ylabel('Beschleunigung in mm/ s**2')
    plt.xlabel('Zeit in s')
    plt.legend()

    
    fig5 = plt.figure().gca()
    try:
        fig5.plot(t, xyzrxryrzVT[:,0], color='r', label='dX')
        fig5.plot(t, xyzrxryrzVT[:,1], color='g', label='dY')
        fig5.plot(t, xyzrxryrzVT[:,2], color='b', label='dZ')
    except:
        return 5
    fig5.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig5.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("Pose Geschwindigkeit XYZ")
    plt.ylabel('XYZ in mm/s')
    plt.xlabel('Zeit in s')
    plt.legend()
    
	
    fig6 = plt.figure().gca()
    try:
        fig6.plot(t, xyzrxryrzAT[:,0], color='r', label='ddX')
        fig6.plot(t, xyzrxryrzAT[:,1], color='g', label='ddY')
        fig6.plot(t, xyzrxryrzAT[:,2], color='b', label='ddZ')
    except:
        return 6
    fig6.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig6.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("Pose Beschleunigung XYZ")
    plt.ylabel('XYZ in mm/s**2')
    plt.xlabel('Zeit in s')
    plt.legend()

    return 0

#plot qT, vT Gelenkwinkel
def plotTrajAxesIk(qT, vT,  t):
    
    c = np.array(['r','g','b','c','magenta','orange'])
    lq = np.array(['q0','q1','q2','q3','q4','q5'])
    lqd = np.array(['qd0','qd1','qd2','qd3','qd4','qd5'])

    fig1 = plt.figure().gca()
    try:
        for axis in range(6):
            fig1.plot(t, qT[:,axis], color=c[axis], label=lq[axis])
    except:
        return axis
    
    fig1.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig1.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("Gelenkwinkel")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    fig2 = plt.figure().gca()
    try:
        for axis in range(6):
            fig2.plot(t, vT[:,axis], color=c[axis], label=lqd[axis])
    except:
        return axis
    fig2.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig2.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title("Winkelgeschwindigkeit")
    plt.ylabel('Winkelgeschwindigkeit in Rad/s')
    plt.xlabel('Zeit in s')
    plt.legend()
    
    return 0

"""
Teil 5: CSV Files
"""
#nur Python 3.6!!!
#1. write Data to CSV: movej (Gelenkwinkel --> Fk --> Pose)
def writeCSV(qT, vT, aT, xyzrxryrzT, xyzrxryrzVT, t, filenameCSV):
    #"exampleCsv.csv" # directory relative to script
    csv = open('csv/' + filenameCSV, "w")  #open File in write mode
    
    axNum = qT.shape[1]
    
    if(axNum == 6):
        csv.write("timestamp target_q_0 target_q_1 target_q_2 target_q_3 target_q_4 target_q_5 target_qd_0 target_qd_1 target_qd_2 target_qd_3 target_qd_4 target_qd_5 target_qdd_0 target_qdd_1 target_qdd_2 target_qdd_3 target_qdd_4 target_qdd_5 target_TCP_pose_0 target_TCP_pose_1 target_TCP_pose_2 target_TCP_pose_3 target_TCP_pose_4 target_TCP_pose_5 target_TCP_speed_0 target_TCP_speed_1 target_TCP_speed_2 target_TCP_speed_3 target_TCP_speed_4 target_TCP_speed_5\n")
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
        
        #5. target_TCP_pose_X
        for para in range(6):
            csv.write(str(xyzrxryrzT[timestamp,para]) + " ")
            
        #6. target_TCP_speed_X
        for para in range(6):
            csv.write(str(xyzrxryrzVT[timestamp,para]) + " ")
            
        csv.write("\n")
        
    return 0

#2. write Data to CSV: movel (Pose --> Ik --> Gelenkwinkel)
def writeCSVTcp(qT, vT, xyzrxryrzT, xyzrxryrzVT, xyzrxryrzAT, t, filenameCSV):
    #"exampleCsv.csv" # directory relative to script
    csv = open('csv/' + filenameCSV, "w")  #open File in write mode
    
    axNum = qT.shape[1]
    
    if(axNum == 6):
        csv.write("timestamp target_q_0 target_q_1 target_q_2 target_q_3 target_q_4 target_q_5 target_qd_0 target_qd_1 target_qd_2 target_qd_3 target_qd_4 target_qd_5 target_TCP_pose_0 target_TCP_pose_1 target_TCP_pose_2 target_TCP_pose_3 target_TCP_pose_4 target_TCP_pose_5 target_TCP_speed_0 target_TCP_speed_1 target_TCP_speed_2 target_TCP_speed_3 target_TCP_speed_4 target_TCP_speed_5 target_TCP_acc_0 target_TCP_acc_1 target_TCP_acc_2 target_TCP_acc_3 target_TCP_acc_4 target_TCP_acc_5\n")
    else:
        return 1

    
    for timestamp in range(t.size):
        
        #1. timestamp
        time = np.float32(t[timestamp])
        csv.write(str(time) + " ")
        
        #2. q_X
        for axis in range(axNum):
            csv.write(str(qT[timestamp,axis]) + " ")
            
        #2. qd_X
        for axis in range(axNum):
            csv.write(str(vT[timestamp,axis]) + " ")
        
        #3. xyzrxryrz
        for para in range(6):
            csv.write(str(xyzrxryrzT[timestamp,para]) + " ")
            
        #4. xyzrxryrzVT
        for para in range(6):
            csv.write(str(xyzrxryrzVT[timestamp,para]) + " ")   
        
        #5. xyzrxryrzaT
        for para in range(6):
            csv.write(str(xyzrxryrzAT[timestamp,para]) + " ")
            
        csv.write("\n")
        
    return 0


#plotCSV: python2.7 --> save as .png
import csv_reader
#3. plot data of .csv File --> q, qd, qdd, tcp_pose, tcp_speed
def plotCSV(filenameCSV):
    
    filename = os.path.splitext(filenameCSV)[0]
    
    with open(('csv/' + filenameCSV)) as csvfile:
        r = csv_reader.CSVReader(csvfile)

    fig1 = plt.figure().gca()
    try:
        fig1.plot(r.timestamp, r.target_q_0, color='r', label='q0')
        fig1.plot(r.timestamp, r.target_q_1, color='g', label='q1')
        fig1.plot(r.timestamp, r.target_q_2, color='b', label='q2')
        fig1.plot(r.timestamp, r.target_q_3, color='c', label='q3')
        fig1.plot(r.timestamp, r.target_q_4, color='magenta', label='q4')
        fig1.plot(r.timestamp, r.target_q_5, color='orange', label='q5')
    except:
        return 1   
    fig1.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig1.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title(filenameCSV + " - Gelenkwinkel")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_q.png', dpi = 300)
    
    
    fig2 = plt.figure().gca()
    try:
        fig2.plot(r.timestamp, r.target_qd_0, color='r', label='qd0')
        fig2.plot(r.timestamp, r.target_qd_1, color='g', label='qd1')
        fig2.plot(r.timestamp, r.target_qd_2, color='b', label='qd2')
        fig2.plot(r.timestamp, r.target_qd_3, color='c', label='qd3')
        fig2.plot(r.timestamp, r.target_qd_4, color='magenta', label='qd4')
        fig2.plot(r.timestamp, r.target_qd_5, color='orange', label='qd5')
    except:
        return 2
    fig2.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig2.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title(filenameCSV + " - Winkelgeschwindigkeit")
    plt.ylabel('Winkelgeschwindigkeit in Rad / s')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_qd.png', dpi = 300)
    
    
    fig3 = plt.figure().gca()
    try:
        fig3.plot(r.timestamp, r.target_qdd_0, color='r', label='qdd0')
        fig3.plot(r.timestamp, r.target_qdd_1, color='g', label='qdd1')
        fig3.plot(r.timestamp, r.target_qdd_2, color='b', label='qdd2')
        fig3.plot(r.timestamp, r.target_qdd_3, color='c', label='qdd3')
        fig3.plot(r.timestamp, r.target_qdd_4, color='magenta', label='qdd4')
        fig3.plot(r.timestamp, r.target_qdd_5, color='orange', label='qdd5')
    except:
        return 3
    fig3.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig3.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title(filenameCSV + " - Winkelbeschleunigung")
    plt.ylabel('Winkelbeschleunigung in Rad / s**2')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_qdd.png', dpi = 300)
    
    
    fig4 = plt.figure().gca()
    try:
        fig4.plot(r.timestamp, r.target_TCP_pose_0, color='r', label='X')
        fig4.plot(r.timestamp, r.target_TCP_pose_1, color='g', label='Y')
        fig4.plot(r.timestamp, r.target_TCP_pose_2, color='b', label='Z')
    except:
        return 4
    fig4.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig4.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title(filenameCSV + " - Pose XYZ")
    plt.ylabel('XYZ in m')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_XYZ.png', dpi = 300)
    
    
    fig5 = plt.figure().gca()
    try:
        fig5.plot(r.timestamp, r.target_TCP_pose_3, color='c', label='rx')
        fig5.plot(r.timestamp, r.target_TCP_pose_4, color='magenta', label='ry')
        fig5.plot(r.timestamp, r.target_TCP_pose_5, color='orange', label='rz')
    except:
        return 5
    fig5.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig5.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title(filenameCSV + " - Pose rxryrz")
    plt.ylabel('rxryrz in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_rxryrz.png', dpi = 300)


    fig6 = plt.figure().gca()
    try:
        fig6.plot(r.timestamp, r.target_TCP_speed_0, color='r', label='dX')
        fig6.plot(r.timestamp, r.target_TCP_speed_1, color='g', label='dY')
        fig6.plot(r.timestamp, r.target_TCP_speed_2, color='b', label='dZ')
    except:
        return 4 
    fig6.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig6.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title(filenameCSV + " - Pose Geschwindigkeit XYZ")
    plt.ylabel('XYZ in m/s')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_Geschwindigkeit_XYZ.png', dpi = 300)
    
    
    fig7 = plt.figure().gca()
    try:
        fig7.plot(r.timestamp, r.target_TCP_speed_3, color='c', label='drx')
        fig7.plot(r.timestamp, r.target_TCP_speed_4, color='magenta', label='dry')
        fig7.plot(r.timestamp, r.target_TCP_speed_5, color='orange', label='drz')
    except:
        return 5
    fig7.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig7.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title(filenameCSV + " - Pose Geschwindigkeit rxryrz")
    plt.ylabel('rxryrz in Rad/s')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_Geschwindigkeit_rxryrz.png', dpi = 300)
        
    return 0


#4. plot data of .csv File --> q, qd, tcp_pose, tcp_speed, tcp_acc
def plotCSVTcp(filenameCSV):
    
    filename = os.path.splitext(filenameCSV)[0]
    
    with open(('csv/' + filenameCSV)) as csvfile:
        r = csv_reader.CSVReader(csvfile)

    fig1 = plt.figure().gca()
    try:
        fig1.plot(r.timestamp, r.target_q_0, color='r', label='q0')
        fig1.plot(r.timestamp, r.target_q_1, color='g', label='q1')
        fig1.plot(r.timestamp, r.target_q_2, color='b', label='q2')
        fig1.plot(r.timestamp, r.target_q_3, color='c', label='q3')
        fig1.plot(r.timestamp, r.target_q_4, color='magenta', label='q4')
        fig1.plot(r.timestamp, r.target_q_5, color='orange', label='q5')
    except:
        print("Singular target_q_0-5")
        #return 1 
    fig1.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig1.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title(filenameCSV + " - Gelenkwinkel")
    plt.ylabel('Gelenkwinkel in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_q.png', dpi = 300)
    
    
    fig12 = plt.figure().gca()
    try:
        fig12.plot(r.timestamp, r.target_qd_0, color='r', label='qd0')
        fig12.plot(r.timestamp, r.target_qd_1, color='g', label='qd1')
        fig12.plot(r.timestamp, r.target_qd_2, color='b', label='qd2')
        fig12.plot(r.timestamp, r.target_qd_3, color='c', label='qd3')
        fig12.plot(r.timestamp, r.target_qd_4, color='magenta', label='qd4')
        fig12.plot(r.timestamp, r.target_qd_5, color='orange', label='qd5')
    except:
        print("Singular target_qd_0-5")
        #return 12
    fig12.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig12.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title(filenameCSV + " - Winkelgeschwindigkeit")
    plt.ylabel('Winkelgeschwindigkeit in Rad/s')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_qd.png', dpi = 300)
    
    
    fig2 = plt.figure().gca()
    try:
        fig2.plot(r.timestamp, r.target_TCP_pose_0, color='r', label='X')
        fig2.plot(r.timestamp, r.target_TCP_pose_1, color='g', label='Y')
        fig2.plot(r.timestamp, r.target_TCP_pose_2, color='b', label='Z')
    except:
        print("Singular target_TCP_pose_0-2")
       # return 2  
    fig2.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig2.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title(filenameCSV + " - Pose XYZ")
    plt.ylabel('XYZ in m')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_XYZ.png', dpi = 300)
    
    
    fig3 = plt.figure().gca()
    try:
        fig3.plot(r.timestamp, r.target_TCP_pose_3, color='c', label='rx')
        fig3.plot(r.timestamp, r.target_TCP_pose_4, color='magenta', label='ry')
        fig3.plot(r.timestamp, r.target_TCP_pose_5, color='orange', label='rz')
    except:
        print("Singular target_TCP_pose_3-5")
        #return 3
    fig3.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig3.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title(filenameCSV + " - Pose rxryrz")
    plt.ylabel('rxryrz in Rad')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_rxryrz.png', dpi = 300)
    

    fig4 = plt.figure().gca()
    try:
        fig4.plot(r.timestamp, r.target_TCP_speed_0, color='r', label='dX')
        fig4.plot(r.timestamp, r.target_TCP_speed_1, color='g', label='dY')
        fig4.plot(r.timestamp, r.target_TCP_speed_2, color='b', label='dZ')
    except:
        print("Singular target_TCP_speed_0-2")
        #return 4
    fig4.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig4.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title(filenameCSV + " - Pose Geschwindigkeit XYZ")
    plt.ylabel('dXYZ in m/s')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_Geschwindigkeit_XYZ.png', dpi = 300)
    
    
    fig5 = plt.figure().gca()
    try:
        fig5.plot(r.timestamp, r.target_TCP_speed_3, color='c', label='drx')
        fig5.plot(r.timestamp, r.target_TCP_speed_4, color='magenta', label='dry')
        fig5.plot(r.timestamp, r.target_TCP_speed_5, color='orange', label='drz')
    except:
        print("Singular target_TCP_speed_3-5")
        #return 5
    fig5.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig5.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title(filenameCSV + " - Pose Geschwindigkeit rxryrz")
    plt.ylabel('drxryrz in Rad/s')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_Geschwindigkeit_rxryrz.png', dpi = 300)
    
    
    #target_TCP_acc_X
    fig6 = plt.figure().gca()
    try:
        fig6.plot(r.timestamp, r.target_TCP_acc_0, color='r', label='ddX')
        fig6.plot(r.timestamp, r.target_TCP_acc_1, color='g', label='ddY')
        fig6.plot(r.timestamp, r.target_TCP_acc_2, color='b', label='ddZ')
    except:
        print("Singular target_TCP_acc_X")
        #return 6
    fig6.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
    fig6.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    plt.grid(True)
    plt.title(filenameCSV + " - Pose Beschleunigung XYZ")
    plt.ylabel('ddXYZ in m/s**2')
    plt.xlabel('Zeit in s')
    plt.legend()
    plt.savefig('png/' + filename + '_Pose_Beschleunigung_XYZ.png', dpi = 300)
    
    
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
