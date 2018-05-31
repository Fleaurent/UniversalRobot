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
filenameCSV1 = "csv/achse1Dreieck.csv"
#tp.plotCSV(filenameCSV1)


"""
2. Trapez Trajektorie: deltaQ > qGrenz
"""
filenameCSV2 = "csv/achse2Trapez.csv"
#tp.plotCSV(filenameCSV2)


"""
3. Trapez Trajektorie: Vorgabe Gesamtzeit Führungsachse #TODO
"""
filenameCSV3 = "csv/achse3vaNeu.csv"
#tp.plotCSV(filenameCSV3)


"""
4. Trapez Trajektorie: Vorgabe Schaltzeiten von Führungsachse
"""
filenameCSV4 = "csv/achse4vaNeu.csv"
#tp.plotCSV(filenameCSV4)


"""
5. Trapez Trajektorie Symmetrisch: Vorgabe Gesamtzeit Führungsache (25% tGes Beschleunigen)
"""
filenameCSV = "csv/achse5vaNeu.csv"
#tp.plotCSV(filenameCSV)




"""
Teil B: eine Achse
"""

"""
1. Führungsachse Dreieck Trajektorie: qG < qGrenz
"""
filenameCSVB1 = "csv/Achsen1Dreieck.csv"
#tp.plotCSV(filenameCSVB1)


"""
2. Führungsachse Trapez Trajektorie: qG > qGrenz
"""
filenameCSVB2 = "csv/Achsen2Trapez.csv"
#tp.plotCSV(filenameCSVB2)

"""
3. Trajektorie 25% Trapezverlauf
"""
filenameCSVB3 = "csv/Achsen3Trapez25.csv"
#tp.plotCSV(filenameCSVB3)


"""
Teil C: Roboteraufzeichnung
"""
filenameRobo = "csv/robot_data1.csv"
#tp.plotCSV(filenameRobo)

filenameRobo = "csv/robot_movej_30.csv"
#tp.plotCSV(filenameRobo)

filenameRobo = "csv/robot_movej_90.csv"
#tp.plotCSV(filenameRobo)

filenameRobo = "csv/robot_movej_30_4s.csv"
#tp.plotCSV(filenameRobo)

filenameRobo = "csv/robot_movej_90_8s.csv"
#tp.plotCSV(filenameRobo)

filenameRobo = "csv/robot_movej_90_45_135.csv"
tp.plotCSV(filenameRobo)


