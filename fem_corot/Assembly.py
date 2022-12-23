# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 12:35:26 2022

@author: oyvinpet
"""

import numpy as np
import sys
from scipy import sparse

import putools

from . Corot import *

#%%

def Assembly(r,RT,ModelInfo):

    N_nodes=np.shape(ModelInfo.NodeMatrix)[0]
    N_NodeDof=6
    N_el=np.shape(ModelInfo.ElementMatrix)[0]
    
    K=np.zeros((N_NodeDof*N_nodes,N_NodeDof*N_nodes))
    # K=sparse.dok_matrix((N_NodeDof*N_nodes,N_NodeDof*N_nodes))
    # K=sparse.csr_matrix((N_NodeDof*N_nodes,N_NodeDof*N_nodes))
    # K=sparse.lil_matrix((N_NodeDof*N_nodes,N_NodeDof*N_nodes))
    
    RHS=np.zeros(N_NodeDof*N_nodes)
    N=np.zeros(N_el)
    
    e2_mat_all=ModelInfo.e2mat
    
    TypeElIndex2_all=ModelInfo.TypeElIndex2
    
    L0_all=ModelInfo.L0
    A_all=ModelInfo.A
    Iz_all=ModelInfo.Iz
    Iy_all=ModelInfo.Iy
    It_all=ModelInfo.It
    E_all=ModelInfo.E
    G_all=ModelInfo.G
    TC0_all=ModelInfo.TC0

    NodeIndex_all=ModelInfo.NodeIndex

    ElDofIndex_1_all=ModelInfo.ElDofIndex_1
    ElDofIndex_2_all=ModelInfo.ElDofIndex_2
    
    ElCoord_1_all=ModelInfo.ElCoord_1
    ElCoord_2_all=ModelInfo.ElCoord_2
    
    K_idx_all=ModelInfo.K_idx
    
    for k in np.arange(N_el):
        
        # Index of all DOFs to DOFs in nodes
        n=ElDofIndex_1_all[k]
        m=ElDofIndex_2_all[k]
        
        # Initial coordinates of nodes
        X1=ElCoord_1_all[k]
        X2=ElCoord_2_all[k]
        
        # Lateral vector
        e2=e2_mat_all[k,1:]
        
        # Cross sectional properties
        ElTypeIndex=TypeElIndex2_all[k]
        
        L0=L0_all[k]
        A=A_all[ElTypeIndex]
        Iz=Iz_all[ElTypeIndex]
        Iy=Iy_all[ElTypeIndex]
        It=It_all[ElTypeIndex]
        E=E_all[ElTypeIndex]
        G=G_all[ElTypeIndex]
        TC0=TC0_all[k]
        
        NodeIndex=NodeIndex_all[k]
        
        r_sub=r[n+m]
        RT_sub=RT[:,:,NodeIndex]
        
        # Get matrix
        # t00=numtools.tic()
        (RHSsub1,RHSsub2,K_el,Nx_el)=K_el_matrix(r_sub,RT_sub,L0,A,Iz,Iy,It,E,G,X1,X2,e2,TC0)
        # numtools.toc(t00)
        
        # Assign to global stiffness matrix  
        K[K_idx_all[k]] += K_el
        
        # Axial force
        N[k]=Nx_el;
        
        # RHS
        RHS[n]+=RHSsub1
        RHS[m]+=RHSsub2
        
    KT=K
    
    return RHS,KT,N


#%%

def Assembly_old(r,RT,ModelInfo):

    t00=putools.timing.tic()
    N_nodes=np.shape(ModelInfo.NodeMatrix)[0]
    N_NodeDof=6
    N_el=np.shape(ModelInfo.ElementMatrix)[0]
    
    K=np.zeros((N_NodeDof*N_nodes,N_NodeDof*N_nodes))
    #K=sparse.dok_matrix((N_NodeDof*N_nodes,N_NodeDof*N_nodes))
    
    RHS=np.zeros(N_NodeDof*N_nodes)
    N=np.zeros(N_el)
    
    for k in np.arange(N_el):
        
        # Index of all DOFs to DOFs in nodes
        n=ModelInfo.ElDofIndex_1[k]
        m=ModelInfo.ElDofIndex_2[k]
        
        # Initial coordinates of nodes
        X1=ModelInfo.ElCoord_1[k]
        X2=ModelInfo.ElCoord_2[k]
        
        # Lateral vector
        e2=ModelInfo.e2mat[k,1:]
        
        # Cross sectional properties
        ElTypeIndex=ModelInfo.TypeElIndex2[k]
        
        A=ModelInfo.A[ElTypeIndex]
        Iz=ModelInfo.Iz[ElTypeIndex]
        Iy=ModelInfo.Iy[ElTypeIndex]
        It=ModelInfo.It[ElTypeIndex]
        E=ModelInfo.E[ElTypeIndex]
        G=ModelInfo.G[ElTypeIndex]
        TC0=ModelInfo.TC0[k]
        
        NodeIndex=[ModelInfo.ElementMatrix[k,1],ModelInfo.ElementMatrix[k,2]]
        
        r_sub=r[n+m]
        RT_sub=RT[:,:,NodeIndex]
        
        # Get matrix
        (RHSsub1,RHSsub2,K_el_sub11,K_el_sub12,K_el_sub21,K_el_sub22,Nx_el)=K_el_matrix(r_sub,RT_sub,A,Iz,Iy,It,E,G,X1,X2,e2,TC0)

        # Assign to global stiffness matrix  
        K_el=np.concatenate( (np.concatenate((K_el_sub11,K_el_sub12),axis=1),np.concatenate((K_el_sub21,K_el_sub22),axis=1)),axis=0)
        K[ModelInfo.K_idx[k]] += K_el
        
        # Axial force
        N[k]=Nx_el;
        
        # RHS
        RHS[n]+=RHSsub1
        RHS[m]+=RHSsub2
        
    putools.timing.toc(t00)
    KT=K
    
    return RHS,KT,N
