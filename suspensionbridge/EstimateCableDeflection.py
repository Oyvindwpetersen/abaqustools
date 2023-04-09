# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 11:39:19 2021

@author: OWP
"""

#%%

import os
import numpy as np

from ypstruct import *

from .cable import *

import putools

from ..fem_corot.NonLinearSolver import *
from ..fem_corot.ProcessModel import *
from ..fem_corot.Assembly import *
from ..fem_corot.Corot import *


#%%

def EstimateCableDeflectionMain(meta,cable,bridgedeck,tower,geo):

    cable.N_def_iter=3
    
    dx_pullback_south_iter=np.zeros(cable.N_def_iter)*np.nan
    dx_pullback_north_iter=np.zeros(cable.N_def_iter)*np.nan
    dz_cable_deflection_iter=np.zeros(cable.N_def_iter)*np.nan
    
    dx_pullback_south_initial=geo.dx_pullback_south
    dx_pullback_north_initial=geo.dx_pullback_north

    for iter in np.arange(cable.N_def_iter):
  
        (r_step,Nx,IndexSpan1_U1,IndexSpan2_U1,IndexSpan1_U2,IndexSpan2_U2,IndexSpan1_U3,IndexSpan2_U3,IndexSpan1TopSouth_U1,IndexSpan1TopNorth_U1)=EstimateCableDeflectionSub(meta,cable,bridgedeck,geo)
        
        geo.dx_pullback_south=-r_step[-1][IndexSpan1TopSouth_U1]
        geo.dx_pullback_north=-r_step[-1][IndexSpan1TopNorth_U1]
        geo.dz_cable_deflection=-np.min(r_step[-1][IndexSpan1_U3])
        
        dx_pullback_south_iter[iter]=geo.dx_pullback_south
        dx_pullback_north_iter[iter]=geo.dx_pullback_north
        dz_cable_deflection_iter[iter]=geo.dz_cable_deflection
        
        if not np.isnan(cable.cs.sigma_target):
            cable.cs.A=np.max(Nx)/(cable.cs.sigma_target)
    
    putools.txt.starprint([
    'Initial dz_cable_deflection=' + putools.num.num2strf(dz_cable_deflection_iter[0],3) + ' m' ,
    'Iterated dz_cable_deflection=' + putools.num.num2strf(dz_cable_deflection_iter[-1],3) + ' m'])

    putools.txt.starprint(['Initial dx_pullback_south=' + putools.num.num2strf(dx_pullback_south_initial,3) + ' m' ,
    'Iterated dx_pullback_south=' + putools.num.num2strf(dx_pullback_south_iter[-1],3) + ' m'])
    
    putools.txt.starprint(['Initial dx_pullback_north=' + putools.num.num2strf(dx_pullback_north_initial[0],3) + ' m' ,
    'Iterated dx_pullback_north=' + putools.num.num2strf(dx_pullback_north_iter,3) + ' m'])

    #%%  Displacement in x-dir

    U1_hanger=r_step[-1][IndexSpan1_U1[1:-1]]
    x_hat=meta.x_hanger/(geo.L_bridgedeck/2)
    cable.polycoeff_hanger_adjust=np.polyfit(x_hat,U1_hanger,3)

    #%%  Tower 

    geo.dx_pullback_south=dx_pullback_south_iter[-1]
    geo.dx_pullback_north=dx_pullback_north_iter[-1]
    
    # tower.F_pullback_south=geo.dx_pullback_south*tower.K_south
    # tower.F_pullback_north=geo.dx_pullback_north*tower.K_north
    
    #%%  Displacement of bridge deck
    
    
    dz_cog_midspan_deflection_initial=geo.dz_cog_midspan_deflection
    
    (r_step2,Nx,IndexSpan1_U1,IndexSpan2_U1,IndexSpan1_U2,IndexSpan2_U2,IndexSpan1_U3,IndexSpan2_U3,IndexSpan1TopSouth_U1,IndexSpan1TopNorth_U1)=EstimateCableDeflectionSub(meta,cable,bridgedeck,geo,cableonly=True)
   
    U3_temp1=dz_cable_deflection_iter[-1]-(-np.min(r_step2[0][IndexSpan1_U3]))

    geo.dz_cog_midspan_deflection=U3_temp1

    putools.txt.starprint(['Initial dz_cog_midspan_deflection=' + putools.num.num2strf(dz_cog_midspan_deflection_initial,3) + ' m' , 
    'Iterated dz_cog_midspan_deflection=' + putools.num.num2strf(geo.dz_cog_midspan_deflection,3) + ' m'])

    return (cable,geo)

#%% 

def EstimateCableDeflectionSub(meta,cable,bridgedeck,geo,cableonly=False):
    
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
        NodeNoTop[k]=cablemesh_temp.NodeSet[ putools.num.listindex(cablemesh_temp.NodeSetName,NodeSetNameTop[k])[0] ]
        
    NodeNoAnch=cablemesh_temp.NodeSet[ putools.num.listindex(cablemesh_temp.NodeSetName,NodeSetNameAnch)[0] ]
    
    ModelInfo.DofLabel=putools.num.genlabel(ModelInfo.NodeMatrix[:,0],'all')
    ModelInfo.DofExclude= putools.num.genlabel(NodeNoAnch,['U1' , 'U2' , 'U3']) + putools.num.genlabel(NodeNoTop,['U2' , 'U3']) 
    
    ModelInfo=ProcessModel(ModelInfo)
    
#%%  
    
    NodeNoSpan=cablemesh_temp.NodeSet[ putools.num.listindex(cablemesh_temp.NodeSetName,'Cable_main_span')[0] ]
    
#%% 
    
    P_cable=GravityLoad2(ModelInfo)
    
    # Load for both bridgedecks (if two) 
    pz=-np.sum(bridgedeck.inertia.m)*9.81
    
    ElementBridgeLoad=cablemesh_temp.ElementSet[putools.num.listindex(cablemesh_temp.ElementSetName,'Cable_main_span')[0]]
    
    IndexElementBridgeLoad=putools.num.argmin(ElementMatrix[:,0],ElementBridgeLoad)
    
    P_bridgedeck=DistLoadProjXY(ModelInfo,pz/2,IndexElementBridgeLoad)
    
    if cableonly==False:
        P_loadstep=[None]*1
        P_loadstep[0]=P_cable+P_bridgedeck
    else:
        P_loadstep=[None]*1
        P_loadstep[0]=P_cable
    
#%% 
        
    (r,r_step,Nx,KT,RHS)=NonLinearSolver(ModelInfo,P_loadstep,LoadIncrements=6,norm_tol=1e-8)

#%% 
    
    NodeNoSpan1=NodeNoSpan[NodeNoSpan<15e3]
    NodeNoSpan2=NodeNoSpan[NodeNoSpan>15e3]
    
    IndexSpan1_U1=putools.num.listindex(ModelInfo.DofLabel,putools.num.genlabel(NodeNoSpan1,['U1']))
    IndexSpan2_U1=putools.num.listindex(ModelInfo.DofLabel,putools.num.genlabel(NodeNoSpan2,['U1']))
    
    IndexSpan1_U2=putools.num.listindex(ModelInfo.DofLabel,putools.num.genlabel(NodeNoSpan1,['U2']))
    IndexSpan2_U2=putools.num.listindex(ModelInfo.DofLabel,putools.num.genlabel(NodeNoSpan2,['U2']))
    
    IndexSpan1_U3=putools.num.listindex(ModelInfo.DofLabel,putools.num.genlabel(NodeNoSpan1,['U3']))
    IndexSpan2_U3=putools.num.listindex(ModelInfo.DofLabel,putools.num.genlabel(NodeNoSpan2,['U3']))
    
    IndexSpan1TopSouth_U1=putools.num.listindex(ModelInfo.DofLabel,putools.num.genlabel(NodeNoTop[0],['U1']))[0]
    IndexSpan1TopNorth_U1=putools.num.listindex(ModelInfo.DofLabel,putools.num.genlabel(NodeNoTop[2],['U1']))[0]
    
    return r_step,Nx,IndexSpan1_U1,IndexSpan2_U1,IndexSpan1_U2,IndexSpan2_U2,IndexSpan1_U3,IndexSpan2_U3,IndexSpan1TopSouth_U1,IndexSpan1TopNorth_U1
    
#%% 

    # import matplotlib.pyplot as plt
    
    # plt.figure()
    # plt.plot(r_step[0][IndexSpan1_U3])
    # plt.plot(r_step[1][IndexSpan1_U3])
    # plt.show()
    
    # plt.figure()
    # plt.plot(r_step[0][IndexSpan1_U2])
    # plt.plot(r_step[0][IndexSpan2_U2])
    # plt.show()
    
    # plt.figure()
    # plt.plot(r_step[0][IndexSpan1_U1])
    # plt.plot(r_step[1][IndexSpan1_U1])
    # plt.show()
    
    # plt.ylabel('some numbers')
    # plt.show()

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
        e1=e1/putools.num.norm_fast(e1)
        e3_guess=np.array([0,0,1])

        e2=putools.num.cross_fast(e3_guess,e1)
        e2=e2/putools.num.norm_fast(e2)

        e3=putools.num.cross_fast(e1,e2)
        e3=e3/putools.num.norm_fast(e3)

        e2mat[k,1:4]=e2
        e3mat[k,1:4]=e3

        e2mat[k,0]=ElementMatrix[k,0]
        e3mat[k,0]=ElementMatrix[k,0]

    return (e2mat,e3mat)
    