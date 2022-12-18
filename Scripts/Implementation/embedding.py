import numpy as np
import networkx as nx
import dwave_networkx as dnx
import math
from collections import defaultdict
from itertools import combinations
from graphs import NetworkToFile, FileToNetwork, GraphPartitioning
from QUBO import QMatrix
from dwave.system.samplers import DWaveSampler, LeapHybridSampler
from dwave.system.composites import EmbeddingComposite, FixedEmbeddingComposite, LazyFixedEmbeddingComposite
import dwave.inspector
import minorminer as mm

#-------- Graph --------
graphName = "graph3.txt"
G = FileToNetwork(graphName)
n = nx.number_of_nodes(G)
m = nx.number_of_edges(G)

#-------- Parameters --------
alpha = 1.25
beta = 1
RCS = 0.5

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

#Set chain strength
maxQ = max(Q.values())
minQ = min(Q.values())
max_strength = max(np.abs(maxQ), np.abs(minQ))
chain_strength = RCS*max_strength
print(chain_strength)

target = dnx.chimera_graph(16)
embedding = {1: [1779], 0: [1783, 1777], 3: [1781, 1776], 2: [1780]}

tQ = dwave.embedding.embed_qubo(Q, embedding, target, chain_strength=chain_strength)
print(tQ)
