# Copyright [2022] [Andrea Pérez Martín]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This code plots the results

import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
import dwave_networkx as dnx
import math
from collections import defaultdict
from itertools import combinations
from graphs import NetworkToFile, FileToNetwork, GraphPartitioning
from QUBO import QMatrix

p = [0.2, 0.5, 0.8]
n = [20, 30, 40, 50, 60]

ratio1 = []
ratio2 = []
for i in range(len(p)):
    ratio1.append([])
    ratio2.append([])

for i in range(len(p)):
    with open("results-2-" + str(p[i]) + ".txt", "r") as file:
        for line in file:
            info = line.split()

            ratio1[i].append(float(info[2]))
            ratio2[i].append(float(info[5]))
            




#Plot results
color = ["royalblue", "orange", "green"]
fig = plt.figure()
ax = fig.add_subplot()
ax2 = ax.twinx()

lns1 = []
lns2 = []
for i in range(len(p)):
    lns1.append(ax.plot(n, ratio1[i], ".", color = color[i], label = "p = " + str(p[i])))
    lns2.append(ax2.plot(n, ratio2[i], "x", color = color[i], label = "p = " + str(p[i])))

lns = lns1[0]+lns1[1]+lns1[2]
lns_e = lns2[0]+lns2[1]+lns2[2]
labs = [l.get_label() for l in lns]
labs_e = [l.get_label() for l in lns_e]
ax.legend(lns, labs, loc=0)
ax2.legend(lns_e, labs_e, loc=4)

n2 = [10, 20, 30, 40, 50, 60, 70]  
const = np.full(len(n2), 1)
ax.plot(n2, const, "--", color="lightcoral")
ax2.plot(n2, const, "--", color="plum")




plt.xlim([15, 65])

ax.set_xlabel("Number of vertices")
ax.set_ylabel("Ratio 1 (⚫)")
ax.set_ylim([0.8, 1.5])

ax2.set_ylabel("Ratio 2 (×)")
ax2.set_ylim([0.9, 1.05])

#plt.show()
plt.savefig("Ratio_DW_METIS2.png")


