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
from itertools import combinations
from collections import defaultdict
from Graphs import NetworkToFile, FileToNetwork, GraphPartitioning
from qubo import QMatrix

#Setting up the graph
G = FileToNetwork("graph8.txt")
n = nx.number_of_nodes(G)
m = nx.number_of_edges(G)
print(G.edges())

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
Q2 = QMatrix("graph8.txt", alpha, beta)
#Q_dict = defaultdict(int)

#for i in range(len(Q)):
    #Q_dict[(i,i)] = Q[i][i]
    #for j in range(i, len(Q)):
        #Q_dict[(i,j)] = Q[i][j]

gamma = 1.25
# Initialize our Q matrix
Q = defaultdict(int)

# Fill in Q matrix
for u, v in G.edges:
    Q[(u,u)] += 1
    Q[(v,v)] += 1
    Q[(u,v)] += -2

for i in G.nodes:
    Q[(i,i)] += gamma*(1-len(G.nodes))

for i, j in combinations(G.nodes, 2):
	Q[(i,j)] += 2*gamma

dim = len(Q2)
Q3 = np.zeros((dim, dim))
for i in range(dim):
    for j in range(dim):
        Q3[i][j] = Q[(i,j)]
print(Q2)
print(Q3)

#-------- Running QUBO on the QPU --------

#Set chain strength
#maxQ = max(Q_dict.values())
#minQ = min(Q_dict.values())
#max_strength = max(np.abs(maxQ), np.abs(minQ))
