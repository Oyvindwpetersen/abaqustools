# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 17:07:27 2022

@author: oyvinpet
"""
#%%
import numpy as np

from ypstruct import *
from scipy import sparse
from Corot import *

import sys
sys.path.append("C:/Cloud/OD_OWP/Work/Python/Github/abaqustools")
import numtools

#%%

def ProcessModel(ModelInfo):
    
    
    ModelInfo.N_DOF=len(ModelInfo.DofLabel)
    ModelInfo.N_node=np.shape(ModelInfo.NodeMatrix)[0]
    ModelInfo.N_el=np.shape(ModelInfo.ElementMatrix)[0]
    # Element types
    
    ModelInfo.ElTypeId=np.unique(ModelInfo.ElementMatrix[:,3])
    
    ModelInfo.TypeElIndex=[None]*len(ModelInfo.ElTypeId)
    ModelInfo.TypeElNumber=[None]*len(ModelInfo.ElTypeId)
    
    # Find elements, element index, nodes, and node index for each type
    for k in np.arange(len(ModelInfo.ElTypeId)):
    
        ModelInfo.TypeElIndex[k]=np.nonzero(ModelInfo.ElementMatrix[:,3]==ModelInfo.ElTypeId[k])[0]
        ModelInfo.TypeElNumber[k]=ModelInfo.ElementMatrix[ModelInfo.TypeElIndex[k],0]
        
    # Initial coordinates and index of dofs
    
    ModelInfo.ElDofIndex=[None]*ModelInfo.N_el
    ModelInfo.ElCoord=[None]*ModelInfo.N_el
    ModelInfo.K_idx=[None]*ModelInfo.N_el
    
    ModelInfo.TypeElIndex2=[None]*ModelInfo.N_el

    for k in np.arange(ModelInfo.N_el):
        
        ModelInfo.TypeElIndex2[k]=np.nonzero(ModelInfo.ElTypeId==ModelInfo.ElementMatrix[k,3])[0][0]
        
        ModelInfo.ElDofIndex[k]=[None,None]
        ModelInfo.ElCoord[k]=[None,None]

        for j in [0,1]:
            
            NodeIndex=ModelInfo.ElementMatrix[k,j+1]
            
            NodeNo=ModelInfo.NodeMatrix[NodeIndex,0]
            
            ModelInfo.ElDofIndex[k][j]=numtools.listindex(ModelInfo.DofLabel,numtools.genlabel(NodeNo,'all'))
    
            ind=np.nonzero(ModelInfo.NodeMatrix[:,0]==NodeNo)[0]
            ModelInfo.ElCoord[k][j]=ModelInfo.NodeMatrix[ind,1:][0]


        n=ModelInfo.ElDofIndex[k][0]
        m=ModelInfo.ElDofIndex[k][1]
        
        ModelInfo.K_idx[k]=np.ix_(n+m, n+m)

    # Check that e2 is normal to e1 (along element)
    
    e2_norm_temp=np.sqrt(np.sum(ModelInfo.e2mat[:,1:]**2,1))
    ModelInfo.e2mat[:,1:]=ModelInfo.e2mat[:,1:]/e2_norm_temp[:,None]

    ModelInfo.TC0=[None]*ModelInfo.N_el
    ModelInfo.L0=np.zeros(ModelInfo.N_el)
    
    for k in np.arange(ModelInfo.N_el):
        
        ModelInfo.L0[k]=np.linalg.norm(ModelInfo.ElCoord[k][1]-ModelInfo.ElCoord[k][0])
    
        X1=ModelInfo.ElCoord[k][0].T
        X2=ModelInfo.ElCoord[k][1].T
        L0=ModelInfo.L0[k]
        
        e1=(X2-X1)/L0;
        e2=ModelInfo.e2mat[k,1:]
        
        # Transformation matrix between global coordinates to initial (C0) configuration
        TC0=CoordinateTransform(e1,e2)
        
        ModelInfo.TC0[k]=TC0
        
    # Elimination of restrained DOFs
    ModelInfo.IndexExclude=numtools.listindex(ModelInfo.DofLabel,ModelInfo.DofExclude)
    ModelInfo.IndexInclude=np.setdiff1d(np.arange(ModelInfo.N_DOF),ModelInfo.IndexExclude)
    
    row=ModelInfo.IndexInclude
    col=np.arange(len(ModelInfo.IndexInclude))
    data=np.ones(np.shape(ModelInfo.IndexInclude))
    ModelInfo.S_red=sparse.csr_matrix((data, (row, col))) #.toarray()

    # A_red=np.atleast_2d(np.arange(22)+10).T
    # A_full=ModelInfo.S_red @ A_red
    
    return ModelInfo


    # ModelInfo.S_red=sparse( ...
    # ModelInfo.IndexInclude,1:length(ModelInfo.DofInclude),...
    # ones(1,length(ModelInfo.DofInclude)),length(ModelInfo.DofLabel),length(ModelInfo.DofInclude));



