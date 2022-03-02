# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 17:07:27 2022

@author: oyvinpet
"""
#%%
import numpy as np

from ypstruct import *
from ProcessModel import ProcessModel
from NonLinearSolver import NonLinearSolver

#%%

ModelInfo=struct()

ModelInfo.NodeMatrix=np.array([ [1,2,3,10] , [0,2,5,6] , [0,0,0,0] , [0,0,0,0] ] ).T
ModelInfo.ElementMatrix=np.array([ [10,20,30] , [1-1,2-1,3-1] , [2-1,3-1,4-1] , [1,1,1] ] ).T
ModelInfo.e2mat=np.array([ [10,20,30] , [0,0,0] , [1,1,1] , [0,0,0] ] ).T

# ModelInfo.NodeMatrix=np.array([ [1,2] , [0,6] , [0,0] , [0,0] ] ).T
# ModelInfo.ElementMatrix=np.array([ [10] , [0] , [1] , [1] ] ).T
# ModelInfo.e2mat=np.array([ [10] , [0] , [1] , [0] ] ).T

ModelInfo.DofLabel=numtools.genlabel(ModelInfo.NodeMatrix[:,0],'all')

ModelInfo.DofExclude=['1_U1' , '1_U2' , '1_U3' , '1_UR1' , '1_UR2' , '1_UR3' ]

P_loadstep=[np.zeros(len(ModelInfo.DofLabel))]
P_loadstep[0][-4]=1000

ModelInfo.A=[0.1,0.1]
ModelInfo.Iy=[10e-6,10e-6]
ModelInfo.Iz=[10e-6,10e-6]
ModelInfo.It=[10e-6,10e-6]
ModelInfo.E=[210e9,210e9]
ModelInfo.G=[81e9,81e9]
ModelInfo.rho=[7850,7850]

ModelInfo=ProcessModel(ModelInfo)

delta=1000*6**3/(3*210e9*1e-6)


#%%


(r,KT,K_add,RHS,N)=NonLinearSolver(ModelInfo,P_loadstep,LoadIncrements=1)




