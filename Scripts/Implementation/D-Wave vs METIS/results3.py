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

p = [0.2, 0.5, 0.8]
n = [20, 30, 40, 50, 60]

ratio1 = []
ratio2 = []
for i in range(len(p)):
    ratio1.append([])
    ratio2.append([])

for i in range(len(p)):
    with open("ratio" + str(p[i]) + ".txt", "r") as file:
        for line in file:
            info = line.split()
            
            for item in info:
                ratio1[i].append(float(item))

for i in range(len(p)):
    with open("ratio" + str(p[i]) + "-2.txt", "r") as file:
        for line in file:
            info = line.split()
            
            for item in info:
                ratio2[i].append(float(item))
        


#Plot results
#plt.ylim([-0.1, 1.1])
color = ["royalblue", "orange", "green"]
plt.xlim([15, 65])
plt.xlabel("Number of vertices")
plt.ylabel("Ratio")
for i in range(len(p)):
    plt.plot(n, ratio1[i], ".", color = color[i], label = "p = " + str(p[i]))
    plt.plot(n, ratio2[i], "x", color = color[i], label = "p = " + str(p[i]))
    
n2 = [10, 20, 30, 40, 50, 60, 70]    
const = np.full(len(n2), 1)
plt.plot(n2, const, "--", color="lightcoral")
plt.legend()
plt.savefig("Ratio_DW_METIS.png")


