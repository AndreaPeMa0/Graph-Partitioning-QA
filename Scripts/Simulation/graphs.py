#This file includes graph related functions

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations
from random import random
import os

def RandomGraphGenerator(n, p):
    '''
    Generates a random graph of n vertices using Erdös–Rényi model
    
    Input
    -----
    n  : int
         number of vertices
    p  : float
         probability that an edge exists between a given pair of vertices

    Output
    ------
    graph  :  networkx graph
              random graph created
    '''
    
    #Vertex set and edge set
    V = set([v for v in range(n)])
    E = set()
    
    #Possible edges
    for combination in combinations(V, 2):
        
        a = random()  #a in [0, 1)
        if a < p:
            E.add(combination)
            
    graph = nx.Graph()
    graph.add_nodes_from(V)
    graph.add_edges_from(E)
    
    return graph

def DrawNetwork(network, figName):
    '''
    Plots a networkx graph and saves it as a png file
    
    Input
    -----
    network   : networkx graph
                graph to be plotted
    figName   : string
                name of the png file
    '''
    
    pos = nx.spring_layout(network)
    nx.draw_networkx(network, pos)
    plt.savefig(figName)
    plt.show()
    
def NetworkToFile(network, fileName):
    '''
    Saves the networkx graph in a file
    
    Input
    -----
    network   : networkx graph
                graph to be saved in the file
    fileName  : string
                name of the file
    '''
    #Preparing data for the text file
    n = 0
    m = 0
    vertex = []
    
    n = len(network.nodes)
    m = len(network.edges)
    
    for i in range(n):
        vertex.append([])
    
    for e in network.edges:
        vertex[e[0]].append(e[1]+1)
        vertex[e[1]].append(e[0]+1)
    
    #Writing in the file
    with open(fileName, "w") as file:
        file.write("%%%%%% graph file %%%%%%")
        file.write("\n")
        file.write(str(n) + " " + str(m))
        file.write("\n")
        
        for i in range(len(vertex)):
            for j in range(len(vertex[i])):
                file.write(str(vertex[i][j]) + " ")
            file.write("\n")

def FileToNetwork(fileName):
    '''
    Saves the information of a file as a networkx graph
    
    Input
    -----
    fileName  : string
                name of the file
    
    Output
    ------
    network   : networkx graph
                graph created
    '''
    
    network = nx.Graph()
    vertex = []
    
    #Reading file
    with open(fileName) as file:
        
        next(file) #discard line
        n, m = [int(x) for x in next(file).split()]
        
        for i in range(n):
            vertex.append([])
            
        i = 0   
        for line in file:
            e = line.split()
            for j in range(len(e)):
                vertex[i].append(int(e[j])-1)
            i += 1
        
        #Edge list
        edge = []
        aux = []
        for i in range(len(vertex)):
            for j in range(len(vertex[i])):
                if (i) < vertex[i][j]:
                    aux.append([i, vertex[i][j]])
                else:
                    aux.append([vertex[i][j], i])
        for item in aux:
            if item not in edge:
                edge.append(item)
        
        #Adding edges to the networkx graph
        for item in edge:
            network.add_edge(item[0], item[1])
            
    return network

def DrawSolution(network, fileName, figName):
    '''
    Plots the solution of the partition and saves it as a png file
    
    Input
    -----
    network   : networkx graph
                graph to be plotted
    fileName  : string
                name of the file
    figName   : string
                name of the png file
    '''
    
    color_map_aux = []
    
    #Reading file
    with open(fileName) as file:
        
        for line in file:
            i = line.split()
            
            if int(i[0]) == 0:
                color_map_aux.append("blue")
            if int(i[0]) == 1:
                color_map_aux.append("green")
                
    #Making sure colors are in the right order           
    color_map = []
    for node in network.nodes():
        color_map.append(color_map_aux[node])
        
    #Drawing
    pos = nx.spring_layout(network)
    nx.draw_networkx(network, pos, node_color=color_map)
    plt.savefig(figName)
    plt.show()
    
def GraphPartitioning(fileName, k):
    '''
    Partitions a graph into k parts using METIS
    
    Input
    -----
    fileName  : string
                name of the file with the graph
    k         : int
                parts to be madee
    '''
    os.system("gpmetis " + fileName + " " + str(k))



#Example
#n = 10
#p = 0.8
#G = RandomGraphGenerator(n, p)

#DrawNetwork(G, "graph.png")
#NetworkToFile(G, "graph.txt")
#GraphPartitioning("graph.txt", 2)
#DrawSolution(G, "graph.txt.part.2", "graph.part.plot.png")



