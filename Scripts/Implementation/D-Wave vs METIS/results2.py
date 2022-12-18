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

# This code analises the results

import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
import dwave_networkx as dnx
import math
from collections import defaultdict
from itertools import combinations
from graphs import NetworkToFile, FileToNetwork, GraphPartitioning
from QUBO import QMatrix

p = 0.8
n = [20, 30, 40, 50, 60]
cut_edges_MET = []

for i in range(len(n)):

    graphName = "graph-" + str(p) + "-" + str(n[i]) + ".txt"
    # METIS
    GraphPartitioning(graphName, 2)

    with open("METIS-"+ graphName, "r") as file:
        #Line to read
        line_number = [14]

        #To store the line
        info = []

        for i, line in enumerate(file):
            if i in line_number:
                for word in line.split():
                    info.append(word)
                
    cut_edges = str(info[2])
    cut_edges_MET.append(cut_edges.replace(",", ""))

print(cut_edges_MET)


#-------------- CUT EDGES -------------------

cut_edges_DW = np.empty(len(n))
#success_rate = np.zeros(len(n))
#deviation = np.zeros(len(n))

with open("DW" + str(p) + "-2.txt") as file:
    i = 0
    for line in file:
        info = line.split()
        #success_rate[i] = float(info[1])
        #deviation[i] = float(info[2])
        cut_edges_DW[i] = float(info[3])
        i += 1
print(cut_edges_DW)

#Save results
ratio = []
for i in range(len(n)):
    ratio.append(float(cut_edges_DW[i])/float(cut_edges_MET[i]))
print(ratio)
with open("ratio" + str(p) + "-2.txt", "w") as file:
    for i in range(len(n)):
        file.write(str(ratio[i]) + " ")



#Plot results
#plt.ylim([-0.1, 1.1])
#plt.xlim([-0.1, 1.1])
#plt.xlabel("RCS")
#plt.ylabel("Success Rate")
#plt.errorbar(RCS, success_rate, yerr = deviation, fmt='.', color='black', ecolor='lightgray', capsize = 3)
#plt.savefig("Success_Rate_vs_RCS-graph3(40).png")


