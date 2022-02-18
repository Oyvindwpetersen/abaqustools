# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 12:35:26 2022

@author: oyvinpet
"""



import numpy as np
import numtools
from Corot import *
from Assembly import Assembly

#%%
def NonLinearSolver(ModelInfo,P_loadstep,LoadIncrements=10,IterationMax=100,norm_tol=1e-8,LinearStiffness=np.nan):

    # Load step scaling
    f_scale=np.logspace(-6,0,LoadIncrements)
    
    # p=0.5
    # c=np.exp(np.log(1e-6)/(1-1.0/LoadIncrements**p))
    # b=1/np.log(1e-6/c)
    # r_axis=np.arange(1,LoadIncrements+1)
    # f_scale=c*np.exp(r_axis**p/b)
    
    if LoadIncrements==1:
        f_scale=[1]

    # Multiple load cases (propagating analysis)
    LoadSteps=len(P_loadstep)

    # Direct additions to stiffness matrix
    K_add=np.nan
    # if not np.isnan(LinearStiffness).any():
        # K_add=sparse(LinearStiffness{1}(:,1),LinearStiffness{1}(:,2),LinearStiffness{2},ModelInfo.N_DOF,ModelInfo.N_DOF)
    # else:
        # K_add=sparse(ModelInfo.N_DOF,ModelInfo.N_DOF)
        
    # Initialization
    RT=np.zeros((3,3,ModelInfo.N_DOF))
    for n in np.arange(ModelInfo.N_DOF):
        RT[:,:,n]=np.eye(3)
        
    r=np.zeros(ModelInfo.N_DOF)
    
    # Iterative calculations
    norm_dr=[None]*LoadSteps
    norm_dr_iter=[None]*LoadSteps
    
    r_step=[None]*LoadSteps

    t0=numtools.tic()

    leadingzero2="{:02d}"    
    for j in np.arange(LoadSteps):
    
        numtools.starprint('Load step ' + leadingzero2.format(j+1) + '/' + leadingzero2.format(LoadSteps) ,1)
            
        if j==0:
            P_prev_loadstep=np.zeros(np.shape(P_loadstep[j]))
            P_add=P_loadstep[j]
        else:
            P_prev_loadstep=P_loadstep[j-1]
            P_add=P_loadstep[j]-P_prev_loadstep

        norm_dr[j]=[None]*LoadIncrements
        norm_dr_iter[j]=[None]*LoadIncrements

        for l in np.arange(LoadIncrements):

            numtools.starprint('Load increment ' + leadingzero2.format(l+1) + '/' + leadingzero2.format(LoadIncrements) ,1)
            
            # Load for this step
            fn=P_prev_loadstep+f_scale[l]*P_add # Add load: from previos load step plus difference*scalefactor, where scale factor [0,1]
            
            # Some initial for convergence check
            norm_dr[j][l]=[np.nan]
            norm_dr_iter[j][l]=[np.nan]
            
            n=0
            LoadIncrementConv=False
            while n<IterationMax and LoadIncrementConv==False:
                
                t_it=numtools.tic()
                
                n=n+1
                numtools.starprint('Iteration ' + leadingzero2.format(n),0)
                
                
                # Build model
                (RHS,KT,N)=Assembly(r,RT,ModelInfo)
                
                
                # Added stiffness
                # if np.isnan(LinearStiffness).any():
                    # KT=KT+K_add
                
                # Residual
                Rn=fn-RHS
                
                # Increment calculation
                (dr,KT_red)=CalculateDisplacements(KT,Rn,ModelInfo)
                RT=IncrementalRotation(dr,RT)
                
                # If norm of dr is too large, decrease
                scale_iter=1
                if n>1:
                    if numtools.norm_fast(dr)>np.nanmax(norm_dr_iter[j][l]):
                        numtools.starprint('norm(dr) large, dr scaled down')
                        scale_iter=0.5

                # Update response
                r=r+dr*scale_iter
            
                # Check if converged
                if numtools.norm_fast(dr)/(ModelInfo.N_DOF)<norm_tol:
                    LoadIncrementConv=True

                # Save norms
                norm_dr[j][l].append(numtools.norm_fast(dr))
                norm_dr_iter[j][l].append(numtools.norm_fast(dr*scale_iter))
                
                if LoadIncrementConv==True:
                    numtools.starprint('Converged at iteration n=' + str(n))
                    
                    
                # numtools.starprint('Iter time ' + numtools.num2strf(t_it,0))
            if LoadIncrementConv==False:
                numtools.starprint('Break simulation at load increment ' + leadingzero2.format(l+1) + '/' + leadingzero2.format(LoadIncrements) + ', applied load ratio ' + numtools.num2strf(f_scale[l]) )
                numtools.starprint('Not converged',4)
                #DoBreak=True
                            
        r_step[j]=r

    t1=numtools.tocs(t0)
    
    numtools.starprint('Calculation time ' + numtools.num2strf(t1,2))
    
    
    return r,r_step,N,KT,RHS
# Outputs

