# -*- coding: utf-8 -*-
"""
Created on Mon May 28 21:50:02 2018

@author: flore
"""

#plot CSV just work with python 2.7
#run trajektorienplanung_*_test first to create CSVs


import trajektorienplanung as tp

"""
Teil A: eine Achse
"""


"""
1. Dreieck Trajektorie: deltaQ < qGrenz
"""
filenameCSV1 = "achse1Dreieck.csv"
#tp.plotCSV(filenameCSV1)


"""
2. Trapez Trajektorie: deltaQ > qGrenz
"""
filenameCSV2 = "achse2Trapez.csv"
#tp.plotCSV(filenameCSV2)


"""
3. Trapez Trajektorie: Vorgabe Gesamtzeit Führungsachse #TODO
"""
filenameCSV3 = "achse3vaNeu.csv"
#tp.plotCSV(filenameCSV3)


"""
4. Trapez Trajektorie: Vorgabe Schaltzeiten von Führungsachse
"""
filenameCSV4 = "achse4vaNeu.csv"
#tp.plotCSV(filenameCSV4)


"""
5. Trapez Trajektorie Symmetrisch: Vorgabe Gesamtzeit Führungsache (25% tGes Beschleunigen)
"""
filenameCSV = "achse5vaNeu.csv"
#tp.plotCSV(filenameCSV)




"""
Teil B: eine Achse
"""

"""
1. Führungsachse Dreieck Trajektorie: qG < qGrenz
"""
filenameCSVB1 = "Achsen1Dreieck.csv"
#tp.plotCSV(filenameCSVB1)


"""
2. Führungsachse Trapez Trajektorie: qG > qGrenz
"""
filenameCSVB2 = "Achsen2Trapez.csv"
#tp.plotCSV(filenameCSVB2)

"""
3. Trajektorie 25% Trapezverlauf
"""
filenameCSVB3 = "Achsen3Trapez25.csv"
#tp.plotCSV(filenameCSVB3)


"""
Teil C: Roboteraufzeichnung
"""
#1. movej_Dreieck
filenameRobo = "robot_movej_Dreieck.csv"
#tp.plotCSV(filenameRobo)
#tp.plotPoseCSV(filenameRobo)

#2. movej_Trapez
filenameRobo = "robot_movej_Trapez.csv"
#tp.plotCSV(filenameRobo)
#tp.plotPoseCSV(filenameRobo)

#3. movej_Dreieck_Zeit
filenameRobo = "robot_movej_Dreieck_Zeit.csv"
#tp.plotCSV(filenameRobo)
#tp.plotPoseCSV(filenameRobo)

#4. movej_Trapez_Zeit
filenameRobo = "robot_movej_Trapez_Zeit.csv"
#tp.plotCSV(filenameRobo)
#tp.plotPoseCSV(filenameRobo)

#5. movej_Synchron
filenameRobo = "robot_movej_Synchron.csv"
#tp.plotCSV(filenameRobo)
#tp.plotPoseCSV(filenameRobo)

#6. movel_x400
filenameRobo = "robot_movel_x400.csv"
tp.plotCSV(filenameRobo)
tp.plotPoseCSV(filenameRobo)

filenameRobo = "robot_movel_x400_Zeit.csv"
tp.plotCSV(filenameRobo)
tp.plotPoseCSV(filenameRobo)

#7. movel_x400_Singular
filenameRobo = "robot_movel_x400_Singular.csv"
tp.plotCSV(filenameRobo)
tp.plotPoseCSV(filenameRobo)

filenameRobo = "robot_movel_x400_Singular_Zeit.csv"
tp.plotCSV(filenameRobo)
tp.plotPoseCSV(filenameRobo)

