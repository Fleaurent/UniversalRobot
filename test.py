# -*- coding: utf-8 -*-
"""
toDO: keine Winkeländerung!

"""

import numpy as np
import math
import matplotlib.pyplot as plt
import robolib3 as rl
import os
import trajektorienplanung as tp

qStart = 2
qTarget =0
vMax = 1
aMax = 2
tDelta = 1/125

[tS1, tS2, tGes] = tp.traj_timestamps(qStart, qTarget, vMax, aMax)
print(tS1, tS2, tGes)

[vNeu, aNeu] = tp.traj_getVA(qStart, qTarget/4, vMax, aMax, tS1, tGes)
print(vNeu, aNeu)

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