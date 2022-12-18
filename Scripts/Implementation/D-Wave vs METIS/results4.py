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

p = 0.2
n = [20, 30, 40, 50, 60]
cut_edges_MET = []

for i in range(1):

    graphName = "graph-" + str(p) + "-" + str(n[i]) + ".txt"
    
    with open("METIS-"+ graphName, "r") as file:
        #Line to read
        line_number = [28]

        #To store the line
        info = []

        for i, line in enumerate(file):
            if i in line_number:
                for word in line.split():
                    info.append(word)

        print(info)       
   

