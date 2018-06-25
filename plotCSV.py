# -*- coding: utf-8 -*-
"""
Created on Mon May 28 21:50:02 2018

@author: flore
"""

#plot CSV just work with python 2.7
#1. run trajektorienplanung_robolib to create CSVs (python3.6)
#2. run plotCSV to create PNG plots (python2.7)

import trajektorienplanung as tp


"""
robolib Berechnung
"""
"""
#1. movej_Dreieck
filenameRobo = "robolib_movej_Dreieck.csv"
tp.plotCSV(filenameRobo)

#2. movej_Trapez
filenameRobo = "robolib_movej_Trapez.csv"
tp.plotCSV(filenameRobo)

#3. movej_Dreieck_Zeit
filenameRobo = "robolib_movej_Dreieck_Zeit.csv"
tp.plotCSV(filenameRobo)

#4. movej_Trapez_Zeit
filenameRobo = "robolib_movej_Trapez_Zeit.csv"
tp.plotCSV(filenameRobo)

#5. movej_Synchron
filenameRobo = "robolib_movej_Synchron.csv"
tp.plotCSV(filenameRobo)
"""
#6. movel_x400
filenameRobo = "robolib_movel_x400.csv"
tp.plotCSVTcp(filenameRobo)

#7. movel_x400_Singular
filenameRobo = "robolib_movel_x400_Singular.csv"
tp.plotCSVTcp(filenameRobo)
