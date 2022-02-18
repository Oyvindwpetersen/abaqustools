# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 17:07:27 2022

@author: oyvinpet
"""
#%%

import numtools

import numpy as np


#%%

ind=[]
for k in range(100):
    
    ind.append(np.ix_(k*6+np.arange(6),k*6+np.arange(6)))


t0=numtools.tic()

for n in range(1000):
  
    
    A=np.zeros((1000,1000))
    
    for k in range(100):
    
        # K_el=[1,0,0,0,0,0  , 1,0,0,0,0,0  , 1,0,0,0,0,0  , 1,0,0,0,10,0  , 1,0,0,0,0,100  , 1,0,0,0,0,200  ]
        # A[ind[k]]=np.array(K_el).reshape((6,6))
        
        
        K_el=np.array( [ [1,0,0,0,0,0]  , [1,0,0,0,0,0]  , [1,0,0,0,0,0]  , [1,0,0,0,10,0]  , [1,0,0,0,0,100]  , [1,0,0,0,0,200]  ])
        A[ind[k]]=K_el
        
        
numtools.toc(t0)