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
from itertools import combinations
from graphs import NetworkToFile, FileToNetwork, GraphPartitioning
from QUBO import QMatrix
from dwave.system.samplers import DWaveSampler, LeapHybridSampler
from dwave.system.composites import EmbeddingComposite
import dwave.inspector


#-------- Graph --------
G = FileToNetwork("graph8.txt")
n = nx.number_of_nodes(G)
m = nx.number_of_edges(G)


#-------- Parameters --------
min_tf = 1.0
max_tf = 2000.0
num_tf = 20
tf = np.linspace(min_tf, max_tf, num_tf)
num_reads_value  = 500
alpha = 1.25
beta = 1
RCS = 0.2
cut_edges_DW = np.empty(num_tf)
solution_DW = []
select = 0   #to choose solver
success_rate = np.zeros(num_tf)
deviation = np.zeros(num_tf)


#-------- QUBO dictionary --------
Q = defaultdict(int)

for u, v  in G.edges:
    Q[(u,u)] += 1*beta
    Q[(v,v)] += 1*beta
    Q[(u,v)] += -2*beta

for i in G.nodes:
    Q[(i,i)] += alpha*(1-n)

for i, j in combinations(G.nodes, 2):
    Q[(i,j)] += 2*alpha



#-------- Running QUBO on the QPU --------

#Set chain strength
maxQ = max(Q.values())
minQ = min(Q.values())
max_strength = max(np.abs(maxQ), np.abs(minQ))

#Computing minor-embeddings
if (select == 0):
    #Choosing DW_2000Q_6
    sampler = EmbeddingComposite(DWaveSampler(solver = 'DW_2000Q_6'))
elif (select == 1):
    #Choosing Advantage
    sampler = EmbeddingComposite(DWaveSampler(solver = 'Advantage_system5.2'))

#Running QUBO on the solver chosen
for i in range(num_tf):
    sampleset = sampler.sample_qubo(Q,
                                chain_strength = RCS*max_strength,
                                num_reads = num_reads_value,
                                auto_scale = True,
                                annealing_time = tf[i],
                                label = 'Graph partitioning'
                                    )

    #Saving results into a file
    if (select == 0):
        fileName = "DW-RCS-(" + str(RCS) + ").txt"
        print("--------------- DW_2000Q_6 ---------------")
    elif (select == 1):
        fileName = "Adv-RCS-(" + str(RCS) + ").txt"
        print("----------- Advantage_system5.2 -----------")

    print(sampleset.to_pandas_dataframe())
    
    #Checking if the  best solution found is correct and counting cut edges
    dict_state = sampleset.first.sample.values()
    state = list(dict_state)

    if sum(state) in [math.floor(len(G.nodes)/2), math.ceil(len(G.nodes)/2)]:
        num_cut_edges = 0
        for u, v in G.edges:
            num_cut_edges += state[u] + state[v] -2*state[u]*state[v]
        
        cut_edges_DW[i] = num_cut_edges
        print("Valid partition found with", num_cut_edges, "cut edges\n")
        print("Solution: ", state)

        solution_DW.append(state)

        groundStateSet = sampleset.lowest(atol = 0.1)
        success_rate[i] = float(np.sum(groundStateSet.record.num_occurrences))/float(num_reads_value)
        deviation[i] = np.sqrt(success_rate[i]*(1-success_rate[i])/num_reads_value)


    else:
        print("No valid partition found")
        cut_edges_DW[i] = 0.0
        solution_DW.append(0.0)
        success_rate[i] = 0.0
        deviation[i] = 0.0

    
#Save results
with open(fileName, "w") as file:
    for i in range(num_tf):
        file.write(str(tf[i]) + " " + str(success_rate[i]) + " " + str(deviation[i]) + " " + str(cut_edges_DW[i]) + " " + str(solution_DW[i]) + "\n")




