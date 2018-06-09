# -*- coding: utf-8 -*-
"""
toDO: keine Winkeländerung!

"""

import numpy as np
import matplotlib.pyplot as plt
import trajektorienplanung as tp

qStart = 2
qTarget = -2

vMax = 1
aMax = 2
tDelta = 1/125

#Achse 1: Zeitparameter
[tS1, tS2, tGes] = tp.traj_timestamps(qStart, qTarget, vMax, aMax)
print(tS1, tS2, tGes)

#größerer Winkel --> größere Zeiparameter --> Dominante Achse
[tS1X, tS2X, tGesX] = tp.traj_timestamps(qStart*2, qTarget*2, vMax, aMax)
print(tS1X, tS2X, tGesX)

#Achse 1 zeitlich an Dominante Achse anpassen
[vNeu, aNeu] = tp.traj_getVA(qStart, qTarget, tS1X, tGesX)
print(vNeu, aNeu)

[tS1, tS2, tGes] = tp.traj_timestamps(qStart, qTarget, vNeu, aNeu)
print(tS1, tS2, tGes)

#Achse 1 mit  vNeu, aNeu + angepasster Zeit plotten
[qT, vT, aT, t] = tp.traj_sample(qStart, qTarget, tS1, tS2, tGes, vNeu, aNeu, tDelta)

plt.plot(t, qT)
plt.title('Position')
plt.show()
plt.plot(t, vT)
plt.title('Velocity')
plt.show()
plt.plot(t, aT)
plt.title('Acceleration')
plt.show()

#todo
#csv
#6 achsen 1. vergleich Fuehrungsachse 2. anderre achsen anpassen 3. traj_sample 4.plot