#Adiabatic evolution related functions

import numpy as np
from matplotlib import pyplot as plt

#Hamiltonian
def Hamiltonian(t, tau, HI, HF):
    '''
    Returns de Hamiltonian of the adiabatic evolution

    Input
    -----
    t    : double
           time
    tau  : double
           total time evolution
    HI   : array
           initial hamiltonian
    HF   : array
           final hamiltonian
    '''

    if t < tau:
        return (1-t/tau)*HI + (t/tau)*HF
    else:
        return HF

#Crank-Nicolson
def CrankNicolson(H, psi, delta_t):
    '''
    Crank-Nicolson algorithm for the time evolution of the wavefunction

    Input
    -----
    H        : array
               Hamiltonian of the system
    psi      : array
               wave function at t
    delta_t  : double
               time increase
    
    Output
    ------
    psi  : array
           wave function at t + delta_t
    '''

    M = np.identity(2, dtype=complex) - (0. + 1.j)*delta_t/2*H
    Minv = np.linalg.inv(np.identity(2, dtype=complex) + (0. + 1.j)*delta_t/2*H)
    
    psi = np.matmul(M, psi)
    psi = np.matmul(Minv, psi)
    
    return psi

#Evolution and overlap with instantaneous ground state and first excited state
def evolution(tau, ts, delta_t, func):
    '''
    Calculates the evolution of the system and the overlaps with ground state and first excited state

    Input
    -----
    tau      : double
               total time evolution
    ts       : array
               time interval [0, tau]
    delta_t  : double
               time increase
    func     : Hamiltonian

    Output
    ------
    overlap0  : array
                overlap with ground state
    overlap1  : array
                overlap with first excited state
    '''

    overlap0 = []
    overlap1 = []

    for i, t in enumerate(ts):
        
        H = func(t,tau)
        
        if (t == 0):
            
            vap, vep = np.linalg.eigh(H)
            psi0 = vep[:, 0]
            psi0 = np.conjugate(psi0)
            psi1 = vep[:, 1]
            psi1 = np.conjugate(psi1)
            
            psi = psi0
    
            prod0 = np.dot(psi,psi0)
            mod0 = (np.real(prod0)*np.real(prod0) + np.imag(prod0)*np.imag(prod0))
            mod0 = mod0**(1/2)
            overlap0.append(mod0)
    
            prod1 = np.dot(psi,psi1)
            mod1 = (np.real(prod1)*np.real(prod1) + np.imag(prod1)*np.imag(prod1))
            mod1 = mod1**(1/2)
            overlap1.append(mod1)
            
        
        else:
            
            psi = CrankNicolson(H, psi, delta_t)
            
            vap, vep = np.linalg.eigh(H)
            psi0 = vep[:, 0]
            psi0 = np.conjugate(psi0)
            psi1 = vep[:, 1]
            psi1 = np.conjugate(psi1)
    
    
            prod0 = np.dot(psi,psi0)
            mod0 = (np.real(prod0)*np.real(prod0) + np.imag(prod0)*np.imag(prod0))
            mod0 = mod0**(1/2)
            overlap0.append(mod0)
    
            prod1 = np.dot(psi,psi1)
            mod1 = (np.real(prod1)*np.real(prod1) + np.imag(prod1)*np.imag(prod1))
            mod1 = mod1**(1/2)
            overlap1.append(mod1)
        
    return np.array(overlap0), np.array(overlap1)