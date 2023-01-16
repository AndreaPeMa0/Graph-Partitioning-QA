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

# This code plots the average of the results

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import FormatStrFormatter
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
    with open("results-" + str(p[i]) + ".txt", "r") as file:
        for line in file:
            info = line.split()

            ratio1[i].append(float(info[2]))
            ratio2[i].append(float(info[5]))

ratio3 = []
ratio4 = []
for i in range(len(p)):
    ratio3.append([])
    ratio4.append([])

for i in range(len(p)):
    with open("results-2-" + str(p[i]) + ".txt", "r") as file:
        for line in file:
            info = line.split()

            ratio3[i].append(float(info[2]))
            ratio4[i].append(float(info[5]))


cut_edges = []
energy = []
dev_edges = []
dev_energy = []
for i in range(len(p)):
    cut_edges.append([])
    energy.append([])
    dev_edges.append([])
    dev_energy.append([])

for i in range(len(p)):
    for j in range(len(n)):
        aux = ratio1[i][j] + ratio3[i][j]
        cut_edges[i].append(aux/2)
        
        aux2 = ratio2[i][j] + ratio4[i][j]
        energy[i].append(aux2/2)

for i in range(len(p)):
    for j in range(len(n)):
        aux = (ratio1[i][j] - cut_edges[i][j])**2
        aux2 = (ratio3[i][j] - cut_edges[i][j])**2
        dev_edges[i].append(np.sqrt(aux+aux2))

        aux3 = (ratio2[i][j] - energy[i][j])**2
        aux4 = (ratio4[i][j] - energy[i][j])**2
        dev_energy[i].append(np.sqrt(aux3+aux4))
        






#Plot results(2 y axis)
#color = ["royalblue", "orange", "green"]
#fig = plt.figure()
#ax = fig.add_subplot()
#ax2 = ax.twinx()

#lns1 = []
#lns2 = []
#for i in range(len(p)):
    #lns1.append(ax.plot(n, cut_edges[i], ".", color = color[i], label = "p = " + str(p[i])))
    #lns2.append(ax2.plot(n, energy[i], "x", color = color[i], label = "p = " + str(p[i])))

#lns = lns1[0]+lns1[1]+lns1[2]
#lns_e = lns2[0]+lns2[1]+lns2[2]
#labs = [l.get_label() for l in lns]
#labs_e = [l.get_label() for l in lns_e]
#ax.legend(lns, labs, loc=0)
#ax2.legend(lns_e, labs_e, loc=4)

#n2 = [10, 20, 30, 40, 50, 60, 70]  
#const = np.full(len(n2), 1)
#ax.plot(n2, const, "--", color="lightcoral")
#ax2.plot(n2, const, "--", color="plum")


#plt.xlim([15, 65])

#ax.set_xlabel("Number of vertices")
#ax.set_ylabel("Ratio 1 (⚫)")
#ax.set_ylim([0.8, 1.5])

#ax2.set_ylabel("Ratio 2 (×)")
#ax2.set_ylim([0.9, 1.05])

#plt.show()
#plt.savefig("Ratio_DW_METIS_average.png")




#Plot results(same x axis)
color = ["royalblue", "blueviolet", "green"]
fig = plt.figure()
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])

plt.rc('legend', fontsize=14)

ax0 = plt.subplot(gs[1])
ax0.set_xlabel("Number of vertices", size = 12)
ax0.set_xlim([15, 65])
ax0.set_ylim([0.8, 1.5])
ax0.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax0.set_ylabel("Nc D-Wave / Nc METIS", size = 12)
lns1 = []

lns1.append(ax0.plot(n, cut_edges[0], ".", color = color[0], label = "p = " + str(p[0])))
lns1.append(ax0.plot(n, cut_edges[1], "^", color = color[1], label = "p = " + str(p[1])))
lns1.append(ax0.plot(n, cut_edges[2], "x", color = color[2], label = "p = " + str(p[2])))

ax0.tick_params(labelsize=14)

ax1 = plt.subplot(gs[0], sharex = ax0)
ax1.set_ylim([0.9, 1.05])
ax1.set_xlim([15, 65])
ax1.set_ylabel("E D-Wave / E METIS", size = 12)
lns2 = []

lns2.append(ax1.plot(n, energy[0], ".", color = color[0], label = "p = " + str(p[0])))
lns2.append(ax1.plot(n, energy[1], "^", color = color[1], label = "p = " + str(p[1])))
lns2.append(ax1.plot(n, energy[2], "x", color = color[2], label = "p = " + str(p[2])))

ax1.tick_params(labelsize=14)

plt.setp(ax1.get_xticklabels(), visible=False)
yticks = ax0.yaxis.get_major_ticks()
yticks[-1].label1.set_visible(False)

n2 = [10, 20, 30, 40, 50, 60, 70]  
const = np.full(len(n2), 1)
ax0.plot(n2, const, "--", color="lightcoral")
ax1.plot(n2, const, "--", color="plum")

lns = lns1[0]+lns1[1]+lns1[2]
lns_e = lns2[0]+lns2[1]+lns2[2]
labs = [l.get_label() for l in lns]
labs_e = [l.get_label() for l in lns_e]
#ax0.legend(lns, labs, loc=0)
ax1.legend(lns_e, labs_e, loc=3)


plt.subplots_adjust(hspace=.0)
#plt.show()
plt.savefig("Ratio_DW_METIS_average5.png")