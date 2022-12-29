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

# This code analises the results from the files

import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
import dwave_networkx as dnx
import math
from collections import defaultdict
from itertools import combinations
from QUBO import QMatrix

p = 0.8
n = [20, 30, 40, 50, 60]
isSol = []

#-------------- CUT EDGES METIS -------------------
cut_edges_MET = []

for i in range(len(n)):

    fileName = "METIS-graph-" + str(p) + "-" + str(n[i]) + ".txt"

    with open(fileName, "r") as file:
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


#-------------- CUT EDGES DW -------------------

cut_edges_DW = np.empty(len(n))

with open("DW-2-" + str(p) + ".txt") as file:
    i = 0
    for line in file:
        info = line.split()
        cut_edges_DW[i] = float(info[3])
        i += 1
print(cut_edges_DW)


#-------------- ENERGY DW -------------------
energy_DW = np.empty(len(n))

with open("DW-2-" + str(p) + ".txt") as file:
    i = 0
    for line in file:
        info = line.split()
        state = []
        for j in range(4, len(info)):
            aux = info[j]
            aux = aux.replace(",", "")
            if (j == 4):
                aux = aux.replace("[", "")
            if (j == len(info)-1):
                aux = aux.replace("]", "")
            aux = float(aux)
            state.append(aux)
        

        graphName = "graph-" + str(p) + "-" + str(n[i]) + ".txt"
        QM = QMatrix(graphName, 1.25, 1)

        energy_DW[i] = np.matmul(state, np.matmul(QM, state))
        i += 1
print(energy_DW)


#-------------- ENERGY METIS -------------------
energy_METIS = np.empty(len(n))
states = []
for i in range(len(n)):
    states.append([])

for i in range(len(n)):
    fileName = "graph-" + str(p) + "-" + str(n[i]) + ".txt.part.2"

    with open(fileName, "r") as file:
        for line in file:
            info = line.split()
            states[i].append(float(info[0]))
    
    graphName = "graph-" + str(p) + "-" + str(n[i]) + ".txt"
    QM = QMatrix(graphName, 1.25, 1)

    energy_METIS[i] = np.matmul(states[i], np.matmul(QM, states[i]))
print(energy_METIS)


states2 = []
for i in range(len(n)):
    states2.append([])

for i in range(len(n)):
    for j in range(len(states[i])):
        if (states[i][j] == 1):
            states2[i].append(0.0)
        else:
            states2[i].append(1.0)



#-------------- SOLUTION METIS IN DW -------------------
isSol = []
for i in range(len(n)):
    
    fileName = "screen-2-graph-" + str(p) + "-" + str(n[i]) + ".txt"
    aux = False

    with open(fileName, "r") as file:
        next(file) #discard line
        line_number = [0]

        for j, line in enumerate(file):
            if j not in line_number:
                info = line.split()
                if (info[0] == "['BINARY',"):
                    break
                
                state = []
                for k in range(1, n[i]+1):
                    state.append(float(info[k]))
                
              
                if (state == states[i] or state == states2[i]):
                    aux = True
    isSol.append(aux)           
print(isSol)      
            
#-------------- ENERGY METIS IN DW -------------------
isEnergy = []
for i in range(len(n)):
    
    fileName = "screen-2-graph-" + str(p) + "-" + str(n[i]) + ".txt"
    aux = False

    with open(fileName, "r") as file:
        next(file) #discard line
        line_number = [0]

        for j, line in enumerate(file):
            if j not in line_number:
                info = line.split()
                if (info[0] == "['BINARY',"):
                    break
                
                energy = float(info[n[i]+1])
                
                if(energy == energy_METIS[i]):
                    aux = True
            
                    break
    isEnergy.append(aux)
print(isEnergy) 
            

#-------------- SAVING RESULTS -------------------
ratio1 = []
ratio2 = []
for i in range(len(n)):
    ratio1.append(cut_edges_DW[i]/float(cut_edges_MET[i]))
    ratio2.append(energy_DW[i]/energy_METIS[i])

fileName = "results-2-" + str(p) + ".txt"
with open(fileName, "w") as file:
    #Cut_edges_DW, cut_edges_METIS, ratio_ce, energy_DW, energy_METIS, ratio_e, isSol, isEnergy
    for i in range(len(n)):
        file.write(str(cut_edges_DW[i]) + " " + str(cut_edges_MET[i]) + " " + str(ratio1[i]) + " " + str(energy_DW[i]) + " " + str(energy_METIS[i]) + " " + str(ratio2[i]) + " " + str(isSol[i]) + " " + str(isEnergy[i]) + "\n")
    