# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 17:07:27 2022

@author: oyvinpet
"""
#%%
import numpy as np

from ypstruct import *
from scipy import sparse
from . Corot import *

import putools

#%%

def ProcessModel(ModelInfo):
    
    ModelInfo.N_DOF=len(ModelInfo.DofLabel)
    ModelInfo.N_node=np.shape(ModelInfo.NodeMatrix)[0]
    ModelInfo.N_el=np.shape(ModelInfo.ElementMatrix)[0]    
    ModelInfo.ElTypeId=np.unique(ModelInfo.ElementMatrix[:,3])
    
    ModelInfo.TypeElIndex=[None]*len(ModelInfo.ElTypeId)
    ModelInfo.TypeElNumber=[None]*len(ModelInfo.ElTypeId)
    
    # Find elements, element index, nodes, and node index for each type
    for k in np.arange(len(ModelInfo.ElTypeId)):
    
        ModelInfo.TypeElIndex[k]=np.nonzero(ModelInfo.ElementMatrix[:,3]==ModelInfo.ElTypeId[k])[0]
        ModelInfo.TypeElNumber[k]=ModelInfo.ElementMatrix[ModelInfo.TypeElIndex[k],0]
        
    # Initial coordinates and index of dofs
    ModelInfo.NodeIndex=[None]*ModelInfo.N_el
    ModelInfo.ElDofIndex_1=[None]*ModelInfo.N_el
    ModelInfo.ElDofIndex_2=[None]*ModelInfo.N_el
    ModelInfo.ElCoord_1=[None]*ModelInfo.N_el
    ModelInfo.ElCoord_2=[None]*ModelInfo.N_el
    ModelInfo.K_idx=[None]*ModelInfo.N_el
    ModelInfo.TypeElIndex2=[None]*ModelInfo.N_el
    ModelInfo.TC0=[None]*ModelInfo.N_el
    ModelInfo.L0=np.zeros(ModelInfo.N_el)
    
    # Normalize e2
    e2_norm_temp=np.sqrt(np.sum(ModelInfo.e2mat[:,1:]**2,1))
    ModelInfo.e2mat[:,1:]=ModelInfo.e2mat[:,1:]/e2_norm_temp[:,None]    
        
    for k in np.arange(ModelInfo.N_el):
        
        
        ModelInfo.NodeIndex[k]=[ModelInfo.ElementMatrix[k,1],ModelInfo.ElementMatrix[k,2]]
        
        ModelInfo.TypeElIndex2[k]=np.nonzero(ModelInfo.ElTypeId==ModelInfo.ElementMatrix[k,3])[0][0]

        for j in [0,1]:
            
            NodeIndex=ModelInfo.ElementMatrix[k,j+1]
            NodeNo=ModelInfo.NodeMatrix[NodeIndex,0]
            
            ElDofIndex_temp=putools.num.listindex(ModelInfo.DofLabel,putools.num.genlabel(NodeNo,'all'))
            ind=np.nonzero(ModelInfo.NodeMatrix[:,0]==NodeNo)[0]
            ElCoord_temp=ModelInfo.NodeMatrix[ind,1:][0]
            
            if j==0:
                ModelInfo.ElDofIndex_1[k]=ElDofIndex_temp
                ModelInfo.ElCoord_1[k]=ElCoord_temp
            elif j==1:
                ModelInfo.ElDofIndex_2[k]=ElDofIndex_temp
                ModelInfo.ElCoord_2[k]=ElCoord_temp


        n=ModelInfo.ElDofIndex_1[k]
        m=ModelInfo.ElDofIndex_2[k]
        ModelInfo.K_idx[k]=np.ix_(n+m, n+m)
    
        X1=ModelInfo.ElCoord_1[k]
        X2=ModelInfo.ElCoord_2[k]
        L0=putools.num.norm_fast(X2-X1)
        
        ModelInfo.L0[k]=L0
    
        e1=(X2-X1)/L0;
        e2=ModelInfo.e2mat[k,1:]
        
        if np.abs(e1.dot(e2))>0.9:
            putools.txt.starprint('Dot product between e1 and e2 larger than 0.9')
            putools.txt.starprint('Element number =  ' + str(ModelInfo.ElementMatrix[k,0]))
            putools.txt.starprint('k = ' + str(k))

        # Transformation matrix between global coordinates to initial (C0) configuration
        TC0=CoordinateTransform(e1,e2)
        ModelInfo.TC0[k]=TC0
        
    # Elimination of restrained DOFs
    ModelInfo.IndexExclude=putools.num.listindex(ModelInfo.DofLabel,ModelInfo.DofExclude)
    ModelInfo.IndexInclude=np.setdiff1d(np.arange(ModelInfo.N_DOF),ModelInfo.IndexExclude)
    
    row=ModelInfo.IndexInclude
    col=np.arange(len(ModelInfo.IndexInclude))
    data=np.ones(np.shape(ModelInfo.IndexInclude))
    ModelInfo.S_red=sparse.csr_matrix((data, (row, col))) #.toarray()

    ModelInfo.IxInclude=np.ix_(ModelInfo.IndexInclude,ModelInfo.IndexInclude)

    return ModelInfo


