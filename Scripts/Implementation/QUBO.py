#This  file includes funcntions to implement the QUBO method classically

import numpy as np
import matplotlib.pyplot as plt
import itertools
import networkx as nx
from Graphs import DrawSolution, NetworkToFile, FileToNetwork
from Graphs import DrawNetwork, GraphPartitioning, RandomGraphGenerator 


def QMatrix(fileName, alpha, beta):
    '''
    This function returns the Q matrix for a given graph
    
    Input
    -----
    fileName  : string
                name of the file containing the graph
    alpha     : double
                weight for the balancing constraint
    beta      : double
                weight for the minimum edge cut size
    
    Output
    ------
    Q  : array
         Q matrix for the QUBO optimization problem
    '''
    
    vertex = []
    gi = []
    
    #Getting the information of the graph
    with open(fileName) as file:
        
        next(file) #discard line
        n, m = [int(x) for x in next(file).split()]
        
        for i in range(n):
            vertex.append([])
            gi.append([])
        
        #Degrees
        i = 0   
        for line in file:
            e = line.split()
            gi[i] = len(e)
            for j in range(len(e)):
                vertex[i].append(int(e[j]))
            i += 1
            

        #Building the Q matrix
        Q = np.full((n,n), alpha)
        
        for i in range(n):
            Q[i][i] = beta*gi[i] - alpha*(n-1)
        for i in range(len(vertex)):
            for j in range(len(vertex[i])):
                Q[i][vertex[i][j]-1] = alpha - beta
    return Q 

def QUBOSolution(Q, tol):
    '''
    Finds the solutions of the minimization problem
    
    Input
    -----
    Q    : array
           Q matrix for the QUBO optimization problem
    tol  : double
           tolerance for the minimum value
    
    Output
    ------
    num_sols  : double
                number of solutions         
    xmin      : array
                solutions to the GP problem
    '''
    
        
    #Preparing all possible vectors
    x = itertools.product([0,1], repeat = len(Q))
    list_x = list(x)
    
    #Verifying the number of combinations
    if (len(list_x)) != 2**len(Q):
        print("Not all vectors found \n")
        return None
    
    #Finding the solution
    sol = np.zeros(len(list_x))
    aux = 0
    for i in range(len(list_x)):
        aux = np.matmul(list_x[i], Q)
        sol[i] = np.matmul(aux, list_x[i])
    
    E = np.amin(sol)
    min_list = np.isclose(sol, E, atol = tol)
        
    xmin = []
    gap = []
    i = 0
    for item in min_list:
        if item == True:
            xmin.append(list_x[i])
        else:
            gap.append(sol[i])
        i += 1
    num_sols = len(xmin)
    
    #Energy gap
    E2 = np.amin(gap)
    Egap = E2-E
                
    return num_sols, xmin, Egap

def CheckIfEqual(fileName, xmin):
    '''
    Checks if any solution is equal to the solution found by METIS
    
    Input
    -----
    fileName  : string
                name of the file with the METIS solution
    xmin      : array
                QUBO solutions
    '''
    
    metis = []
    #Reading METIS solution
    with open(fileName) as file:
        for line in file:
            i = line.split()
            metis.append(int(i[0]))
    metis = np.array(metis)
    
    #Comparing
    for i in range(len(xmin)):
        sol = np.array(xmin[i])
        
        if (metis == sol).all():
            return True
        
    #Not found
    return False

def NumberCutEdges(partition, network):
    '''
    Returns the number of cut edges of a partition
    
    Input
    -----
    partition   : array
                  partition of the vertices
    network     : networkx graph
                  graph that has been partitioned
    
    Output
    ------
    cut_edges  : int
                 number of cut edges  
    '''
    
    edge_list = list(network.edges)
    cut_edges = 0
    for edge in edge_list:
        cut_edges += (partition[edge[0]] - partition[edge[1]])**2
        
    return cut_edges 

def IsConnected(partition, network):
    '''
    Checks if a solution gives a connected partition or not
    
    Input
    -----
    partition   : array
                  partition of the vertices
    network     : networkx graph
                  graph that has been partitioned               
    '''
    
    #Making sure edges are well-ordered
    edge_list = list(network.edges())
    e = 0
    for item in edge_list:
        if (item[1] < item[0]):
            edge_list[e] = (item[1], item[0])
        e += 1
        
    #Checking if connected
    for i in range(len(partition)-1):
        if partition[i] == partition[i+1]:
            if ((i, i+1) not in edge_list):
                return False
            
    return True
    
def IsBalanced(partition):
    '''
    Checks if a solution gives a balanced partition or not
    
    Input
    -----
    partition   : array
                  partition of the vertices            
    '''
    count1=0
    count2=0
    
    for item in partition:
        if (item == 0):
            count1 += 1
        else:
            count2 += 1
    if (count1 == count2):
        return True
    else:
        return False

#EXAMPLE
#n = 10
#p = 0.3
#I = RandomGraphGenerator(n, p)

#NetworkToFile(I, "example5.txt")
#DrawNetwork(I, "example5.png")

#beta = 1
#alpha_values = np.linspace(0, 1.5, 15)

#METIS solution
#GraphPartitioning("example5.txt", 2)

#DrawSolution(I, "example5.txt.part.2", "example5.part.plot.png")

#xmin = []
#print("alpha" + "\t" + "num sol" + "\t  " + "equal" + "\t  " + "cut edges")
#for alpha in alpha_values:
    
    #Q =QMatrix("example5.txt", alpha, beta)
    #num_sols, xmin_aux, Egap = QUBOSolution(Q, 1e-2)
    #xmin.append(xmin_aux)
    #solution = CheckIfEqual("example5.txt.part.2", xmin_aux)

    #edge_list = []
    #for vect in xmin_aux:
        #edge_list.append(NumberCutEdges(vect,I))
    #cut_edge_min = np.amin(edge_list) 
    #index = np.where(edge_list == cut_edge_min)  
        
    #print("{0:.2f}".format(alpha)+ "\t   " + str(num_sols) + "\t  " + str(solution) + "\t     " + str(cut_edge_min))