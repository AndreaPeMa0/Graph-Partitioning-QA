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

# This code scans the GP problem over different random generated graphs with fixed RCS and annealing time values

import numpy as np
import networkx as nx
import dwave_networkx as dnx
import math
from collections import defaultdict
from itertools import combinations
from graphs import NetworkToFile, FileToNetwork, GraphPartitioning, RandomGraphGenerator
from QUBO import QMatrix
from dwave.system.samplers import DWaveSampler, LeapHybridSampler
from dwave.system.composites import EmbeddingComposite, FixedEmbeddingComposite, LazyFixedEmbeddingComposite
import dwave.inspector
import minorminer as mm


#-------- Graphs --------
n = [20, 30, 40, 50, 60]
p = 0.8


#-------- Parameters --------
annealing_time_value = 20.0
num_reads_value  = 500
alpha = 1.25
beta = 1
RCS = 0.25
cut_edges_DW = np.empty(5)
solution_DW = []
select = 0   #to choose solver
success_rate = np.zeros(5)
deviation = np.zeros(5)


for i in range(len(n)):
    graphName = "graph-" + str(p) + "-" + str(n[i]) + ".txt"
    G = RandomGraphGenerator(n[i], p)
    NetworkToFile(G, graphName)
    
    #-------- QUBO dictionary --------
    Q = defaultdict(int)

    for u, v in G.edges:
        Q[(u,u)] += 1*beta
        Q[(v,v)] += 1*beta
        Q[(u,v)] += -2*beta

    for u in G.nodes:
        Q[(u,u)] += alpha*(1-n[i])

    for u, v in combinations(G.nodes, 2):
        Q[(u,v)] += 2*alpha



    #-------- Running QUBO on the QPU --------

    #Set chain strength
    maxQ = max(Q.values())
    minQ = min(Q.values())
    max_strength = max(np.abs(maxQ), np.abs(minQ))

    ##Computing minor-embeddings
    if (select == 0):
        #Choosing DW_2000Q_6
        sampler = EmbeddingComposite(DWaveSampler(solver = 'DW_2000Q_6'))
    elif (select == 1):
        #Choosing Advantage
        sampler = EmbeddingComposite(DWaveSampler(solver = 'Advantage_system5.3'))


    #Running QUBO on the solver chosen

    sampleset = sampler.sample_qubo(Q,
                                chain_strength = RCS*max_strength,
                                num_reads = num_reads_value,
                                auto_scale = True,
                                annealing_time = annealing_time_value,
                                label = 'Graph partitioning'
                                    )

    #Saving results
    if (select == 0):
        print("--------------- DW_2000Q_6 ---------------")
    elif (select == 1):
        print("----------- Advantage_system5.3 -----------")

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
fileName = "DW" + str(p) + ".txt"
with open(fileName, "w") as file:
    for i in range(len(n)):
        file.write(str(n[i]) + " " + str(success_rate[i]) + " " + str(deviation[i]) + " " + str(cut_edges_DW[i]) + " " + str(solution_DW[i]) + "\n")




