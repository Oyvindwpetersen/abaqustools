# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 09:24:55 2022

@author: oyvinpet
"""

#%%

from NonLinearSolver import NonLinearSolver

(r,r_step,N,KT,RHS)=NonLinearSolver(ModelInfo,P_loadstep,LoadIncrements=6,norm_tol=1e-6)




import matplotlib.pyplot as plt
plt.plot(ModelInfo.NodeMatrix[:,1],r[0::6])
#plt.plot(ModelInfo.NodeMatrix[:,1],r[2::6])

plt.ylabel('some numbers')
plt.show()
