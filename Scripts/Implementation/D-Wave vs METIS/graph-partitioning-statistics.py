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

# This code scans the GP problem for a given graph with fixed RCS and annealing time values

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


#-------- Parameters --------
annealing_time_value = 20.0
num_reads_value  = 500
alpha = 2
beta = 1
RCS = 0.25
cut_edges_DW = 0
solution_DW = []
select = 0   #to choose solver
success_rate = 0
deviation = 0



graphName = "graph-0.2-20.txt"
G = FileToNetwork(graphName)
n = nx.number_of_nodes(G)
m = nx.number_of_edges(G)
    
#-------- QUBO dictionary --------
Q = defaultdict(int)

for u, v in G.edges:
    Q[(u,u)] += 1*beta
    Q[(v,v)] += 1*beta
    Q[(u,v)] += -2*beta

for u in G.nodes:
    Q[(u,u)] += alpha*(1-n)

for u, v in combinations(G.nodes, 2):
    Q[(u,v)] += 2*alpha



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
print(sampleset.to_pandas_dataframe())

with open("screen" + graphName, "w") as file:
    if (select == 0):
        file.write("--------------- DW_2000Q_6 ---------------")
    elif (select == 1):
        file.write("----------- Advantage_system5.3 -----------")
        
    file.write(sampleset.to_pandas_dataframe())
    
#Checking if the  best solution found is correct and counting cut edges
dict_state = sampleset.first.sample.values()
state = list(dict_state)

if sum(state) in [math.floor(len(G.nodes)/2), math.ceil(len(G.nodes)/2)]:
    num_cut_edges = 0
    for u, v in G.edges:
        num_cut_edges += state[u] + state[v] -2*state[u]*state[v]
        
    cut_edges_DW = num_cut_edges
    print("Valid partition found with", num_cut_edges, "cut edges\n")
    print("Solution: ", state)

    solution_DW.append(state)

    groundStateSet = sampleset.lowest(atol = 0.1)
    success_rate = float(np.sum(groundStateSet.record.num_occurrences))/float(num_reads_value)
    deviation = np.sqrt(success_rate*(1-success_rate)/num_reads_value)


else:
    print("No valid partition found")
    cut_edges_DW = 0.0
    solution_DW.append(0.0)
    success_rate = 0.0
    deviation = 0.0

    
#Save results
fileName = "DW-" + graphName
with open(fileName, "w") as file:
    file.write(str(n) + " " + str(success_rate) + " " + str(deviation) + " " + str(cut_edges_DW) + " " + str(solution_DW) + "\n")




