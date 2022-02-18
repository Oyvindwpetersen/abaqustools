# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 11:39:19 2021

@author: OWP
"""

#%%

import os
import numpy as np
import warnings
import numtools

from ypstruct import *

import abq
import gen
from ProcessModel import *
from NonLinearSolver import *

from .ElementNormal import *


#%%

def EstimateCableDeflectionMain(meta,cable,bridgedeck,tower,geo):

    r_u3_mid_initial=geo.dz_cable_deflection
    r_u1_top_south_initial=geo.dx_pullback_south
    r_u1_top_north_initial=geo.dx_pullback_north

    cable.N_def_iter=3
    
    for iter in np.arange(cable.N_def_iter):

        (r_step,
         IndexSpan1_U1,IndexSpan2_U1,
         IndexSpan1_U2,IndexSpan2_U2,
         IndexSpan1_U3,IndexSpan2_U3,
         Nx)=EstimateCableDeflectionSub(meta,cable,bridgedeck,geo)
        
        r_u1_top=r[1][IndexTop_U1]
        geo.dx_pullback_south=-r_u1_top[1]
        geo.dx_pullback_north=-r_u1_top[2]

        r_u3_mid=abs(r{2}(IndexMid_U3));
        geo.dz_cable_deflection=r_u3_mid;

        r_u1_top_all(:,iter)=r_u1_top;
        r_u3_mid_all(iter)=r_u3_mid;
        
        if not np.isnan(cable.cs.sigma_target)
            cable.cs.A=max(Nx)/(cable.cs.sigma_target)
        
        
    numtools.starprint({['Initialized dz_cable_deflection=' + num2str(r_u3_mid_initial,'%0.3f') ' m'] ['Iterated dz_cable_deflection=' + num2str(r_u3_mid,'%0.3f') ' m']},1);

    #%%  Displacement in x-dir

    r_u1_hanger=r{2}(IndexMainspan_U1).';

    x_hat=meta.x_hanger./(geo.L_bridgedeck/2);
    polycoeff=np.polyfit(x_hat,r_u1_hanger,3);
    polycoeff=round(polycoeff,3);

    cable.polycoeff_hanger_adjust=polycoeff;

    #%%  Tower 

    geo.dx_pullback_south=-r_u1_top_all(1,end);
    geo.dx_pullback_north=-r_u1_top_all(2,end);

    tower.F_pullback_south=geo.dx_pullback_south*tower.K_south;
    tower.F_pullback_north=geo.dx_pullback_north*tower.K_north;

    numtools.starprint({['Initialized dx_pullback_south=' + num2str(r_u1_top_south_initial,'%0.3f') ' m'] ['Iterated dx_pullback_south=' + num2str(geo.dx_pullback_south,'%0.3f') ' m']},1);
    numtools.starprint({['Initialized dx_pullback_north=' + num2str(r_u1_top_north_initial,'%0.3f') ' m'] ['Iterated dx_pullback_north=' + num2str(geo.dx_pullback_north,'%0.3f') ' m']},1);

    #%%  Displacement under cable load only

    r_u3_temp2=abs(r{1}(IndexMid_U3));

    dz_cog_midspan_deflection_temp=geo.dz_cog_midspan_deflection;

    geo.dz_cog_midspan_deflection=r_u3_mid-r_u3_temp2;

    numtools.starprint({['Initialized dz_cog_midspan_deflection=' + num2str(dz_cog_midspan_deflection_temp,'%0.3f') ' m'] ['Iterated dz_cog_midspan_deflection=' + num2str(geo.dz_cog_midspan_deflection,'%0.3f') ' m']},1);



#%% 

def EstimateCableDeflectionSub(meta,cable,bridgedeck,geo):

    [meta_,cablemesh_temp]=CableGeometry(None,meta,geo,cable)
    
    NodeMatrix=np.vstack((cablemesh_temp.NodeMatrix[0],cablemesh_temp.NodeMatrix[1]))
    ElementMatrix=np.vstack((cablemesh_temp.ElementMatrix)).astype(int)
    
    for k in np.arange(np.shape(ElementMatrix)[0]):
        
        Index1=np.nonzero(NodeMatrix[:,0]==ElementMatrix[k,1])[0]
        Index2=np.nonzero(NodeMatrix[:,0]==ElementMatrix[k,2])[0]
    
        ElementMatrix[k,1]=Index1
        ElementMatrix[k,2]=Index2

    ElementType=np.zeros((np.shape(ElementMatrix)[0],1)).astype(int)
    ElementType[ElementMatrix[:,0]<100e3]=2
    ElementType[ElementMatrix[:,0]>100e3]=10
    
    ElementMatrix=np.hstack((ElementMatrix,ElementType))
    
    (e2mat,e3mat)=ElementNormal(ElementMatrix,NodeMatrix)
        
    ModelInfo=struct()
    ModelInfo.NodeMatrix=NodeMatrix
    ModelInfo.ElementMatrix=ElementMatrix
    
    ModelInfo.e2mat=e2mat
    
    ModelInfo.A=[ cable.cs.A,1]
    ModelInfo.Iz=[ cable.cs.I11,1]
    ModelInfo.Iy=[ cable.cs.I22,1]
    ModelInfo.It=[ cable.cs.It,1]
    ModelInfo.E=[ cable.cs.E,210e9]
    ModelInfo.G=[ cable.cs.G,80e9]
    ModelInfo.rho=[ cable.cs.rho,0]

#%% 
    
    NodeSetNameTop=['Cable_main_top_south_east', 'Cable_main_top_south_west', 'Cable_main_top_north_east', 'Cable_main_top_north_west']

    NodeSetNameAnch=['Cable_main_anchorage']
        
    NodeNoTop=np.zeros(4)
    for k in np.arange(4):
        NodeNoTop[k]=cablemesh_temp.NodeSet[ numtools.listindex(cablemesh_temp.NodeSetName,NodeSetNameTop[k])[0] ]
        
    NodeNoAnch=cablemesh_temp.NodeSet[ numtools.listindex(cablemesh_temp.NodeSetName,NodeSetNameAnch)[0] ]
    
    ModelInfo.DofLabel=numtools.genlabel(ModelInfo.NodeMatrix[:,0],'all')
    ModelInfo.DofExclude= numtools.genlabel(NodeNoAnch,['U1' , 'U2' , 'U3']) + numtools.genlabel(NodeNoTop,['U2' , 'U3']) 
    
    ModelInfo=ProcessModel(ModelInfo)
    
#%%  
    
    NodeNoSpan=cablemesh_temp.NodeSet[ numtools.listindex(cablemesh_temp.NodeSetName,'Cable_main_span')[0] ]
    

#%% 
    
    P_cable=GravityLoad2(ModelInfo)
    
    # Load for both bridgedecks (if two) 
    pz=-np.sum(bridgedeck.inertia.m)*9.81
    
    ElementBridgeLoad=cablemesh_temp.ElementSet[numtools.listindex(cablemesh_temp.ElementSetName,'Cable_main_span')[0]]
    
    IndexElementBridgeLoad=numtools.argmin(ElementMatrix[:,0],ElementBridgeLoad)
    
    P_bridgedeck=DistLoadProjXY(ModelInfo,pz/2,IndexElementBridgeLoad)
    
    P_loadstep=[None]*2
    P_loadstep[0]=P_cable
    P_loadstep[1]=P_cable+P_bridgedeck
    
#%% 
        
    (r,r_step,Nx,KT,RHS)=NonLinearSolver(ModelInfo,P_loadstep,LoadIncrements=6,norm_tol=1e-6)

#%% 

    NodeNoSpan1=NodeNoSpan[NodeNoSpan<15e3]
    NodeNoSpan2=NodeNoSpan[NodeNoSpan>15e3]
    
    IndexSpan1_U1=numtools.listindex(ModelInfo.DofLabel,numtools.genlabel(NodeNoSpan1,['U1']))
    IndexSpan2_U1=numtools.listindex(ModelInfo.DofLabel,numtools.genlabel(NodeNoSpan2,['U1']))
        
    IndexSpan1_U2=numtools.listindex(ModelInfo.DofLabel,numtools.genlabel(NodeNoSpan1,['U2']))
    IndexSpan2_U2=numtools.listindex(ModelInfo.DofLabel,numtools.genlabel(NodeNoSpan2,['U2']))
        
    IndexSpan1_U3=numtools.listindex(ModelInfo.DofLabel,numtools.genlabel(NodeNoSpan1,['U3']))
    IndexSpan2_U3=numtools.listindex(ModelInfo.DofLabel,numtools.genlabel(NodeNoSpan2,['U3']))
    
    return r_step,IndexSpan1_U1,IndexSpan2_U1,IndexSpan1_U2,IndexSpan2_U2,IndexSpan1_U3,IndexSpan2_U3,Nx
    
#%% 


    import matplotlib.pyplot as plt
    plt.plot(r_step[0][IndexSpan1_U3])
    plt.plot(r_step[1][IndexSpan1_U3])
    
    plt.ylabel('some numbers')
    plt.show()

    plt.plot(r_step[0][IndexSpan1_U2])
    plt.plot(r_step[0][IndexSpan2_U2])
  
    
    plt.plot(r_step[0][IndexSpan1_U1])
    plt.plot(r_step[1][IndexSpan1_U1])
    
    plt.ylabel('some numbers')
    plt.show()


    
    