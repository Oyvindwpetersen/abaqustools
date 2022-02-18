# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 12:35:26 2022

@author: oyvinpet
"""

import scipy
import numpy as np

import sys
sys.path.append("C:/Cloud/OD_OWP/Work/Python/Github/abaqustools")

import numtools

from scipy import sparse
from Corot import *

#%%

def Assembly(r,RT,ModelInfo):

    N_nodes=np.shape(ModelInfo.NodeMatrix)[0]
    N_NodeDof=6
    N_el=np.shape(ModelInfo.ElementMatrix)[0]
    
    K=np.zeros((N_NodeDof*N_nodes,N_NodeDof*N_nodes))
    #K=sparse.dok_matrix((N_NodeDof*N_nodes,N_NodeDof*N_nodes))
    
    RHS=np.zeros(N_NodeDof*N_nodes)
    N=np.zeros(N_el)
    t00=numtools.tic()
    for k in np.arange(N_el):
        
        # Index of all DOFs to DOFs in nodes
        n=ModelInfo.ElDofIndex[k][0]
        m=ModelInfo.ElDofIndex[k][1]
        
        # Initial coordinates of nodes
        X1=ModelInfo.ElCoord[k][0]
        X2=ModelInfo.ElCoord[k][1]
        
        # Lateral vector
        e2=ModelInfo.e2mat[k,1:]
        
        # Cross sectional properties
        ElType=ModelInfo.ElementMatrix[k,3]
        ElTypeIndex=ModelInfo.TypeElIndex2[k]
        
        A=ModelInfo.A[ModelInfo.TypeElIndex2[k]]
        Iz=ModelInfo.Iz[ElTypeIndex]
        Iy=ModelInfo.Iy[ElTypeIndex]
        It=ModelInfo.It[ElTypeIndex]
        E=ModelInfo.E[ElTypeIndex]
        G=ModelInfo.G[ElTypeIndex]
        rho=ModelInfo.rho[ElTypeIndex]
        TC0=ModelInfo.TC0[k]
        
        NodeIndex=[ModelInfo.ElementMatrix[k,1],ModelInfo.ElementMatrix[k,2]]
        
        r_sub=r[n+m]
        RT_sub=RT[:,:,NodeIndex]
        
        # Get matrix
        (RHSsub1,RHSsub2,K_el_sub11,K_el_sub12,K_el_sub21,K_el_sub22,Nx_el)=K_el_matrix(r_sub,RT_sub,A,Iz,Iy,It,E,G,X1,X2,e2,TC0)


        # (RHSsub1,RHSsub2,K_el_sub11,K_el_sub12,K_el_sub21,K_el_sub22,Nx_el)=K_el_matrix(r_sub,RT_sub,
        #                                                                                 ModelInfo.A[ModelInfo.TypeElIndex2[k]],
        #                                                                                 ModelInfo.Iz[ModelInfo.TypeElIndex2[k]],
        #                                                                                 ModelInfo.Iy[ModelInfo.TypeElIndex2[k]],
        #                                                                                 ModelInfo.It[ModelInfo.TypeElIndex2[k]],
        #                                                                                 ModelInfo.E[ModelInfo.TypeElIndex2[k]],
        #                                                                                 ModelInfo.G[ModelInfo.TypeElIndex2[k]],
        #                                                                                 X1,X2,e2,TC0)

        # Assign to global stiffness matrix  
        K_el=np.concatenate( (np.concatenate((K_el_sub11,K_el_sub12),axis=1),np.concatenate((K_el_sub21,K_el_sub22),axis=1)),axis=0)
        K[ModelInfo.K_idx[k]] += K_el
        
        # K[np.ix_(n, n)] += K_el_sub11
        # K[np.ix_(n, m)] += K_el_sub12
        # K[np.ix_(m, n)] += K_el_sub21
        # K[np.ix_(m, m)] += K_el_sub22

        # Axial force
        N[k]=Nx_el;
        
        # RHS
        # RHS[n]=RHS[n]+RHSsub1
        # RHS[m]=RHS[m]+RHSsub2
        
        RHS[n]+=RHSsub1
        RHS[m]+=RHSsub2
        
        
    numtools.toc(t00)

   # K=sparse.csr_matrix(K)
    KT=K
    
    return RHS,KT,N

