# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""
    
#%%

import numpy as np
from .. import numtools

#%%

def ElementNormal(ElementMatrix,NodeMatrix):

    e2mat=np.zeros(( np.shape(ElementMatrix)[0],4 ))
    e3mat=np.zeros(( np.shape(ElementMatrix)[0],4 ))

    for k in np.arange(np.shape(ElementMatrix)[0]):
        
        NodeNumber=ElementMatrix[k,1:3]

        Index1=ElementMatrix[k,1]
        Index2=ElementMatrix[k,2]
        
        Index1=int(Index1)
        Index2=int(Index2)

        X1=NodeMatrix[Index1,1:]
        X2=NodeMatrix[Index2,1:]

        e1=X2-X1
        e1=e1/numtools.norm_fast(e1)
        e3_guess=np.array([0,0,1])

        e2=numtools.cross_fast(e3_guess,e1)
        e2=e2/numtools.norm_fast(e2)

        e3=numtools.cross_fast(e1,e2)
        e3=e3/numtools.norm_fast(e3)

        e2mat[k,1:4]=e2
        e3mat[k,1:4]=e3

        e2mat[k,0]=ElementMatrix[k,0]
        e3mat[k,0]=ElementMatrix[k,0]

    return (e2mat,e3mat)
