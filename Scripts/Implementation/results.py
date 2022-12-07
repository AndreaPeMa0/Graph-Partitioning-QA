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



# METIS
#GraphPartitioning("graph2.txt", 2)

#with open("METIS-graph2.txt", "r") as file:
    #Line to read
    #line_number = [14]

    #To store the line
    #info = []

    #for i, line in enumerate(file):
        #if i in line_number:
            #for word in line.split():
                #info.append(word)
            
#cut_edges = str(info[2])
#cut_edges_MET = cut_edges.replace(",", "")

#-------------- RCS -------------------
min_RCS = 0.0
max_RCS = 1.0
num_RCS = 20
RCS = np.linspace(min_RCS, max_RCS, num_RCS)

cut_edges_DW = np.empty(num_RCS)
success_rate = np.zeros(num_RCS)
deviation = np.zeros(num_RCS)

with open("DW-RCS-graph4.txt") as file:
    i = 0
    for line in file:
        info = line.split()
        success_rate[i] = float(info[1])
        deviation[i] = float(info[2])
        cut_edges_DW[i] = float(info[3])
        i += 1

#Check results ok
#for i in range(num_RCS):
    #if (float(cut_edges_DW[i]) != cut_edges_MET):
        #success_rate[i] = 0.0
        #deviation[i] = 0.0
        

#Plot results
plt.ylim([-0.1, 1.1])
plt.xlim([-0.1, 1.1])
plt.xlabel("RCS")
plt.ylabel("Success Rate")
plt.errorbar(RCS, success_rate, yerr = deviation, fmt='.', color='black', ecolor='lightgray', capsize = 3)
plt.savefig("Success_Rate_vs_RCS(graph4)")


#-------------- TF -------------------
#min_tf = 0.0
#max_tf = 1500.0
#num_tf = 20
#tf = np.linspace(min_tf, max_tf, num_tf)

#cut_edges_DW = np.empty(num_tf)
#success_rate = np.zeros(num_tf)
#deviation = np.zeros(num_tf)

#with open("DW-TF-(graph2).txt") as file:
    #i = 0
    #for line in file:
        #info = line.split()
        #success_rate[i] = float(info[1])
        #deviation[i] = float(info[2])
        #cut_edges_DW[i] = float(info[3])
        #i += 1

#Check results ok
#for i in range(num_RCS):
    #if (float(cut_edges_DW[i]) != float(cut_edges_MET)):
        #success_rate[i] = 0.0
        #deviation[i] = 0.0
        

#Plot results
#plt.ylim([-0.1, 1])
#plt.xlabel("Annealing time (micro s)")
#plt.ylabel("Success Rate")
#plt.errorbar(tf, success_rate, yerr = deviation, fmt='.', color='black', ecolor='lightgray', capsize = 3)
#plt.savefig("Success_Rate_vs_TF(graph2)")


