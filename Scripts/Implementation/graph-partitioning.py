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

# This code scans the GP problem over different RCS values with a fixed annealing time

import numpy as np
import networkx as nx
import dwave_networkx as dnx
import math
from collections import defaultdict
from graphs import NetworkToFile, FileToNetwork, GraphPartitioning
from QUBO import QMatrix
from dwave.system.samplers import DWaveSampler, LeapHybridSampler
from dwave.system.composites import EmbeddingComposite
import dwave.inspector

#Setting up the graph
G = FileToNetwork("graph8.txt")
n = nx.number_of_nodes(G)
m = nx.number_of_edges(G)


#Tunable parameters
annealing_time_value = 20.0
num_reads_value  = 500
alpha = 1.25
beta = 1
min_RCS = 0.0
max_RCS = 1.0
num_RCS = 20
RCS = np.linspace(min_RCS, max_RCS, num_RCS)
cut_edges_DW = np.empty(num_RCS)
cut_edges_MET = np.empty(num_RCS)
select = 0   #to choose solver
success_rate = np.zeros(num_RCS)
deviation = np.zeros(num_RCS)

#Setting up the QUBO dictionary
Q = QMatrix("graph8.txt", alpha, beta)
Q_dict = defaultdict(int)

for i in range(len(Q)):
    Q_dict[(i,i)] = Q[i][i]
    for j in range(i, len(Q)):
        Q_dict[(i,j)] = Q[i][j]


#-------- Running QUBO on the QPU --------

#Set chain strength
maxQ = max(Q_dict.values())
minQ = min(Q_dict.values())
max_strength = max(np.abs(maxQ), np.abs(minQ))

#Computing minor-embeddings
if (select == 0):
    #Choosing DW_2000Q_6
    sampler = EmbeddingComposite(DWaveSampler(solver = 'DW_2000Q_6'))
elif (select == 1):
    #Choosing Advantage
    sampler = EmbeddingComposite(DWaveSampler(solver = 'Advantage_system5.2'))

#Running QUBO on the solver chosen
for i in range(num_RCS):
    sampleset = sampler.sample_qubo(Q_dict,
                                chain_strength = RCS[i]*max_strength,
                                num_reads = num_reads_value,
                                auto_scale = True,
                                annealing_time = annealing_time_value,
                                label = 'Graph partitioning'
                                    )

    #Printing results
    if (select == 0):
        print("--------------- DW_2000Q_6 ---------------")
    elif (select == 1):
        print("----------- Advantage_system5.2 -----------")

    print(sampleset.to_pandas_dataframe())
    print(" ")
    print("Energy: " + str(sampleset.first.energy))

    #Checking if the  best solution found is correct and counting cut edges
    dict_state = sampleset.first.sample.values()
    state = list(dict_state)
    print(state)

    if sum(state) in [math.floor(len(G.nodes)/2), math.ceil(len(G.nodes)/2)]:
        num_cut_edges = 0
        for i, j in G.edges:
            num_cut_edges += (state[i]-state[j])**2
        cut_edges_DW[i] = num_cut_edges/4
        print("Valid partition found with", num_cut_edges, "cut edges\n")
        print("Solution: ", state)

        groundStateSet = sampleset.lowest(atol = 0.1)
        success_rate[i] = float(np.sum(groundStateSet.record.num_occurrences))/float(num_reads_value)
        deviation[i] = np.sqrt(success_rate[i]*(1-success_rate[i])/num_reads_value)



    else:
        print("No valid partition found")
        cut_edges_DW[i] = 0.0
        success_rate[i] = 0.0
        deviation[i] = 0.0

    
    # METIS
    GraphPartitioning("graph8.txt", 2)

    with open("METIS-graph8.txt", "r") as file:
        #Line to read
        line_number = [14]

        #To store the line
        info = []

        for i, line in enumerate(file):
            if i in line_number:
                for word in line.split():
                    info.append(word)
            
    cut_edges = str(info[2])
    cut_edges_MET[i] = cut_edges.replace(",", "")

#Save results
fileName = "Cut Edges DW (" + str(n) + ").txt"
with open(fileName, "w") as file:
    for i in range(num_RCS):
        file.write(str(RCS[i]) + " " + str(success_rate[i]) + " " + str(deviation[i]) + " " + str(cut_edges_DW[i]) + " " + str(cut_edges_MET[i]) + "\n")




