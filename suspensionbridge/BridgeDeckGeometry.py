# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""
    
#%%

import numpy as np
from numpy import matlib
import numtools
import gen
from .MeshStruct import *


def BridgeDeckGeometry(fid,meta,geo,bridgedeck):
#%% [meta,bridgemesh]=
    
    bridgemesh=InitiateMeshStruct()
    
#%%  Mesh size
    
    N_element_pr_hanger=(geo.dx_hanger/bridgedeck.meshsize)
          
    # Set as integer
    if np.abs(N_element_pr_hanger-round(N_element_pr_hanger)) > 1e-3:
        print('***** Ratio geo.dx_hanger/bridgedeck.meshsize = '  + numtools.num2strf(N_element_pr_hanger,5))
        raise Exception('***** The hanger distance and bridge deck mesh size must divide into an integer')
    else:
        N_element_pr_hanger=round(N_element_pr_hanger)


#%%  Bridge deck
    
    # Nodes from first to last hanger
    x_node_mid=np.arange(meta.x_hanger[0],meta.x_hanger[-1]+bridgedeck.meshsize,bridgedeck.meshsize)
    
    # Nodes beyond hangers
    #np.arange(0,(np.ceil(10/1.25)+1)*1.25,1.25)
    x_node_endpiece=np.arange(bridgedeck.meshsize,(np.ceil(meta.bridgedeck.dx_endpiece/bridgedeck.meshsize)+1)*bridgedeck.meshsize,bridgedeck.meshsize)
    x_node_endpiece[-1]=meta.bridgedeck.dx_endpiece
            
    # Merge all nodes
    x_bridgedeck_cog=np.hstack((x_node_mid[0]-np.flip(x_node_endpiece),x_node_mid,x_node_mid[-1]+x_node_endpiece))
    
    # Adjustment due to deflection
    geo.z_cog_midspan_eff=geo.z_cog_midspan+geo.dz_cog_midspan_deflection
    geo.z_cog_south_eff=geo.z_cog_south+geo.dz_cog_south_deflection
    geo.z_cog_north_eff=geo.z_cog_north+geo.dz_cog_north_deflection
    
    # Parabolic curvaturve of bridge deck
    curve_coeff=np.polyfit([x_bridgedeck_cog[0],0,x_bridgedeck_cog[-1]],[geo.z_cog_south_eff,geo.z_cog_midspan_eff,geo.z_cog_north_eff],2)
    z_bridgedeck_cog=np.polyval(curve_coeff,x_bridgedeck_cog)

#%%  Single box

    if bridgedeck.N_box==1:
        
        y_bridgedeck_cog=np.zeros(np.shape(x_bridgedeck_cog))
        
        NodeNumberBridgeDeck=bridgedeck.NodeNumberBase[0]+np.arange(1,len(x_bridgedeck_cog)+1).astype(int)    
        bridgemesh.NodeMatrix.append(np.column_stack((NodeNumberBridgeDeck,x_bridgedeck_cog,y_bridgedeck_cog,z_bridgedeck_cog)))
        bridgemesh.NodeMatrixName.append('Bridgedeck_cog')
        
        ElementNumberBridgeDeck=bridgedeck.ElementNumberBase[0]+np.arange(1,len(x_bridgedeck_cog)).astype(int)
        bridgemesh.ElementMatrix.append(np.column_stack((ElementNumberBridgeDeck,NodeNumberBridgeDeck[:-1],NodeNumberBridgeDeck[1:])))
        bridgemesh.ElementMatrixName.append('Bridgedeck_cog')
        bridgemesh.ElementType.append(bridgedeck.eltype)
        
        meta.bridgedeck.NodeNumberBridgeDeck=[NodeNumberBridgeDeck]
        
        meta.bridgedeck.NodeCoordBearing=[[None]*2]
        meta.bridgedeck.NodeCoordBearing[0][0]=np.matlib.repmat([x_bridgedeck_cog[0],y_bridgedeck_cog[0],z_bridgedeck_cog[0],],3,1).T
        meta.bridgedeck.NodeCoordBearing[0][1]=np.matlib.repmat([x_bridgedeck_cog[-1],y_bridgedeck_cog[-1],z_bridgedeck_cog[-1],],3,1).T
        

#%%  Twin box
    
    if bridgedeck.N_box==2:
        
        meta.bridgedeck.NodeNumberBridgeDeck=[None]*5
        meta.bridgedeck.NodeCoordBearing=[[None]*2 for i in range(2)]
        
        for n in np.arange(5):
            
            x_node=x_bridgedeck_cog
        
            if n==0:
                y_node=-geo.gap/2*np.ones(np.shape(x_node))
                z_node=z_bridgedeck_cog
                NodeName='Bridgedeck' + str(n+1) + '_cog'
            elif n==1:
                y_node=geo.gap/2*np.ones(np.shape(x_node))
                z_node=z_bridgedeck_cog
                NodeName='Bridgedeck' + str(n+1) + '_cog'
            elif n==2:
                y_node=(-geo.gap/2+geo.dy_cog_inner)*np.ones(np.shape(x_node))
                z_node=z_bridgedeck_cog+geo.dz_cog_inner
                NodeName='Bridgedeck' + '_inner_east'
            elif n==3:
                y_node=(geo.gap/2-geo.dy_cog_inner)*np.ones(np.shape(x_node))
                z_node=z_bridgedeck_cog+geo.dz_cog_inner
                NodeName='Bridgedeck' + '_inner_west'
            elif n==4:
                y_node=np.zeros(np.shape(x_node))
                z_node=z_bridgedeck_cog+geo.dz_cog_inner
                NodeName='Bridgedeck' + '_gapmid'
        
            bridgemesh.NodeMatrixName.append(NodeName)
            NodeNumberBridgeDeck=bridgedeck.NodeNumberBase[n]+np.arange(1,len(x_node)+1).astype(int)
            bridgemesh.NodeMatrix.append(np.column_stack((NodeNumberBridgeDeck,x_node,y_node,z_node)))
            
            if n==0 or n==1:
                
                ElementNumberBridgeDeck=bridgedeck.ElementNumberBase[n]+np.arange(1,len(x_bridgedeck_cog)).astype(int)
            
                bridgemesh.ElementMatrix.append(np.column_stack((ElementNumberBridgeDeck,NodeNumberBridgeDeck[:-1],NodeNumberBridgeDeck[1:])))
                bridgemesh.ElementMatrixName.append('Bridgedeck' + str(n+1) + '_cog')
                bridgemesh.ElementType.append(bridgedeck.eltype)
                
                meta.bridgedeck.NodeCoordBearing[n][0]=np.matlib.repmat([x_node[0],y_node[0],z_node[0],],3,1).T
                meta.bridgedeck.NodeCoordBearing[n][1]=np.matlib.repmat([x_node[-1],y_node[-1],z_node[-1],],3,1).T
        
        
            meta.bridgedeck.NodeNumberBridgeDeck[n]=NodeNumberBridgeDeck
        
        bridgemesh.ElementSet.append(['Bridgedeck1_cog' , 'Bridgedeck2_cog'])
        bridgemesh.ElementSetName.append('Bridgedeck_cog')


#%%  Nodes for outer

    x_outer_east=x_bridgedeck_cog
    z_outer_east=z_bridgedeck_cog+geo.dz_cog_hanger

    if bridgedeck.N_box==1:
        y_outer_east=-geo.dy_cog_hanger*np.ones(np.shape(x_outer_east))
    elif bridgedeck.N_box==2:
        y_outer_east=(-geo.dy_cog_hanger-geo.gap/2)*np.ones(np.shape(x_outer_east))

    # Select only nodes where hangers are (and start/end)
    IndexLatConn=numtools.argmin(x_bridgedeck_cog,meta.x_hanger)
    IndexLatConn=np.hstack((0,IndexLatConn,-1))

    NodeNumberOuterEast=bridgedeck.NodeNumberBaseOuter[0]+np.arange(1,len(x_outer_east)+1).astype(int)
    bridgemesh.NodeMatrix.append(np.column_stack((NodeNumberOuterEast[IndexLatConn],x_outer_east[IndexLatConn],y_outer_east[IndexLatConn],z_outer_east[IndexLatConn])))
    bridgemesh.NodeMatrixName.append('Bridgeouter_east')

    x_outer_west=x_outer_east
    y_outer_west=-y_outer_east
    z_outer_west=z_outer_east

    NodeNumberOuterWest=bridgedeck.NodeNumberBaseOuter[1]+np.arange(1,len(x_outer_west)+1).astype(int)
    bridgemesh.NodeMatrix.append(np.column_stack((NodeNumberOuterWest[IndexLatConn],x_outer_east[IndexLatConn],y_outer_west[IndexLatConn],z_outer_west[IndexLatConn])))
    bridgemesh.NodeMatrixName.append('Bridgeouter_west')

#%%  Connective elements lateral

    N_LatConn=len(IndexLatConn)

    # From hanger to bridge deck(s) cog
    if bridgedeck.N_box==1:
        meta.bridgedeck.NodeNumberCogConn1=meta.bridgedeck.NodeNumberBridgeDeck[0][IndexLatConn]
        meta.bridgedeck.NodeNumberCogConn2=meta.bridgedeck.NodeNumberBridgeDeck[0][IndexLatConn]
    elif bridgedeck.N_box==2:
        meta.bridgedeck.NodeNumberCogConn1=meta.bridgedeck.NodeNumberBridgeDeck[0][IndexLatConn]
        meta.bridgedeck.NodeNumberCogConn2=meta.bridgedeck.NodeNumberBridgeDeck[1][IndexLatConn]
        meta.bridgedeck.NodeNumberInnerConn1=meta.bridgedeck.NodeNumberBridgeDeck[2][IndexLatConn]
        meta.bridgedeck.NodeNumberInnerConn2=meta.bridgedeck.NodeNumberBridgeDeck[3][IndexLatConn]
        meta.bridgedeck.NodeNumberMidConn=meta.bridgedeck.NodeNumberBridgeDeck[4][IndexLatConn]


    meta.bridgedeck.NodeNumberConnOuterEast=NodeNumberOuterEast[IndexLatConn]
    meta.bridgedeck.NodeNumberConnOuterWest=NodeNumberOuterWest[IndexLatConn]

    # meta.bridgedeck.NodeNumberCogHanger=NodeNumberBridgeDeck(ind(2:-1]]
    meta.bridgedeck.NodeNumberEastHanger=NodeNumberOuterEast[IndexLatConn[1:-1]]
    meta.bridgedeck.NodeNumberWestHanger=NodeNumberOuterWest[IndexLatConn[1:-1]]


    ElementNumberLatConnOuterEast=bridgedeck.ElementNumberBaseConnLat[0]+np.arange(1,N_LatConn+1).astype(int)
    bridgemesh.ElementMatrix.append(np.column_stack((ElementNumberLatConnOuterEast,meta.bridgedeck.NodeNumberCogConn1,meta.bridgedeck.NodeNumberConnOuterEast)))
    bridgemesh.ElementMatrixName.append('LatConnOuterEast')
    bridgemesh.ElementType.append('B31')

    ElementNumberLatConnOuterWest=bridgedeck.ElementNumberBaseConnLat[1]+np.arange(1,N_LatConn+1).astype(int)
    bridgemesh.ElementMatrix.append(np.column_stack((ElementNumberLatConnOuterWest,meta.bridgedeck.NodeNumberCogConn2,meta.bridgedeck.NodeNumberConnOuterWest)))
    bridgemesh.ElementMatrixName.append('LatConnOuterWest')
    bridgemesh.ElementType.append('B31')

    bridgemesh.ElementSet.append(['LatConnOuterEast' , 'LatConnOuterWest'])
    bridgemesh.ElementSetName.append('LatConnOuter')

    # From cog to inner
    if bridgedeck.N_box==2:

        ElementNumberLatConnInnerEast=bridgedeck.ElementNumberBaseConnLat[2]+np.arange(1,N_LatConn+1).astype(int)
        bridgemesh.ElementMatrix.append(np.column_stack((ElementNumberLatConnInnerEast,meta.bridgedeck.NodeNumberCogConn1,meta.bridgedeck.NodeNumberInnerConn1)))
        bridgemesh.ElementMatrixName.append('LatConnInnerEast')
        bridgemesh.ElementType.append('B31')

        ElementNumberLatConnInnerWest=bridgedeck.ElementNumberBaseConnLat[3]+np.arange(1,N_LatConn+1).astype(int)
        bridgemesh.ElementMatrix.append(np.column_stack((ElementNumberLatConnInnerWest,meta.bridgedeck.NodeNumberCogConn2,meta.bridgedeck.NodeNumberInnerConn2)))
        bridgemesh.ElementMatrixName.append('LatConnInnerWest')
        bridgemesh.ElementType.append('B31')

        bridgemesh.ElementSet.append(['LatConnInnerEast' , 'LatConnInnerWest'])
        bridgemesh.ElementSetName.append('LatConnInner')


    # From gapmid to inner
    if bridgedeck.N_box==2:

        ElementNumberLatConnGapEast=bridgedeck.ElementNumberBaseConnLat[4]+np.arange(1,N_LatConn+1).astype(int)
        bridgemesh.ElementMatrix.append(np.column_stack((ElementNumberLatConnGapEast,meta.bridgedeck.NodeNumberMidConn,meta.bridgedeck.NodeNumberInnerConn1)))
        bridgemesh.ElementMatrixName.append('LatConnGapEast')
        bridgemesh.ElementType.append('B31')

        ElementNumberLatConnGapWest=bridgedeck.ElementNumberBaseConnLat[5]+np.arange(1,N_LatConn+1).astype(int)
        bridgemesh.ElementMatrix.append(np.column_stack((ElementNumberLatConnGapWest,meta.bridgedeck.NodeNumberMidConn,meta.bridgedeck.NodeNumberInnerConn2)))
        bridgemesh.ElementMatrixName.append('LatConnGapWest')
        bridgemesh.ElementType.append('B31')

        bridgemesh.ElementSet.append(['LatConnGapWest' , 'LatConnGapEast'])
        bridgemesh.ElementSetName.append('LatConnGap')


#%% 

    meta.bridgedeck.NodeNumberBearing=[[None]*2 for i in range(bridgedeck.N_box)]
    if bridgedeck.N_box==1:
        
        meta.bridgedeck.NodeNumberBearing[0][0]=[ NodeNumberOuterEast[0],meta.bridgedeck.NodeNumberBridgeDeck[0][0],NodeNumberOuterWest[0], ]
        meta.bridgedeck.NodeNumberBearing[0][1]=[ NodeNumberOuterEast[-1],meta.bridgedeck.NodeNumberBridgeDeck[0][-1],NodeNumberOuterWest[-1] ]
    
    if bridgedeck.N_box==2:
    
        # Outer east, deck 1, inner east
        meta.bridgedeck.NodeNumberBearing[0][0]=[ NodeNumberOuterEast[0] , meta.bridgedeck.NodeNumberBridgeDeck[0][0] , meta.bridgedeck.NodeNumberBridgeDeck[2][0] ]
        meta.bridgedeck.NodeNumberBearing[1][0]=[ meta.bridgedeck.NodeNumberBridgeDeck[3][0] , meta.bridgedeck.NodeNumberBridgeDeck[1][0] , NodeNumberOuterWest[0] ]
        
        # Inner west, deck 2, outer west
        meta.bridgedeck.NodeNumberBearing[0][1]=[ NodeNumberOuterEast[-1] , meta.bridgedeck.NodeNumberBridgeDeck[0][-1] , meta.bridgedeck.NodeNumberBridgeDeck[2][-1] ]
        meta.bridgedeck.NodeNumberBearing[1][1]=[ meta.bridgedeck.NodeNumberBridgeDeck[3][-1] , meta.bridgedeck.NodeNumberBridgeDeck[1][-1] , NodeNumberOuterWest[-1] ]
        

#%%  Shell elements

    if bridgedeck.shell==True and bridgedeck.N_box==1:
    
        ElementNumberShellEast=910e3+np.arange(1,N_LatConn).astype(int)
        ElementNumberShellWest=920e3+np.arange(1,N_LatConn).astype(int)
    
        bridgemesh.ElementMatrix.append(np.column_stack((
                                ElementNumberShellEast,
                               NodeNumberOuterEast[IndexLatConn[:-1]],
                               meta.bridgedeck.NodeNumberCogConn1[:-1],
                               meta.bridgedeck.NodeNumberCogConn1[1:],
                               NodeNumberOuterEast[IndexLatConn[1:]],
                                )))
        bridgemesh.ElementMatrixName.append('Bridgedeck_shell_east')
        bridgemesh.ElementType.append('S4R')
    
        bridgemesh.ElementMatrix.append(np.column_stack((
                                ElementNumberShellWest,
                               NodeNumberOuterWest[IndexLatConn[:-1]],
                               meta.bridgedeck.NodeNumberCogConn2[:-1],
                               meta.bridgedeck.NodeNumberCogConn2[1:],
                               NodeNumberOuterWest[IndexLatConn[1:]],
                                )))
        bridgemesh.ElementMatrixName.append('Bridgedeck_shell_west')
        bridgemesh.ElementType.append('S4R')
    
        bridgemesh.ElementSet.append(['Bridgedeck_shell_east' , 'Bridgedeck_shell_west'])
        bridgemesh.ElementSetName.append('Bridgedeck_shell')


#%%  Shell elements

    if bridgedeck.shell==True and bridgedeck.N_box==2:
        
        ElementNumberShellEast=910e3+np.arange(1,N_LatConn).astype(int)
        ElementNumberShellWest=920e3+np.arange(1,N_LatConn).astype(int)
    
        bridgemesh.ElementMatrix.append(np.column_stack((
                                ElementNumberShellEast,
                               NodeNumberOuterEast[IndexLatConn[:-1]],
                               meta.bridgedeck.NodeNumberCogConn1[:-1],
                               meta.bridgedeck.NodeNumberCogConn1[1:],
                               NodeNumberOuterEast[IndexLatConn[1:]],
                                )))
        bridgemesh.ElementMatrixName.append('Bridgedeck_shell_east1')
        bridgemesh.ElementType.append('S4R')
        
        bridgemesh.ElementMatrix.append(np.column_stack((
                                ElementNumberShellEast+1e3,
                               meta.bridgedeck.NodeNumberInnerConn1[:-1],
                               meta.bridgedeck.NodeNumberCogConn1[:-1],
                               meta.bridgedeck.NodeNumberCogConn1[1:],
                               meta.bridgedeck.NodeNumberInnerConn1[1:],
                                )))
        bridgemesh.ElementMatrixName.append('Bridgedeck_shell_east2')
        bridgemesh.ElementType.append('S4R')
        
        bridgemesh.ElementMatrix.append(np.column_stack((
                                ElementNumberShellWest,
                               NodeNumberOuterWest[IndexLatConn[:-1]],
                               meta.bridgedeck.NodeNumberCogConn2[:-1],
                               meta.bridgedeck.NodeNumberCogConn2[1:],
                               NodeNumberOuterWest[IndexLatConn[1:]],
                                )))
        bridgemesh.ElementMatrixName.append('Bridgedeck_shell_west1')
        bridgemesh.ElementType.append('S4R')
    
        bridgemesh.ElementMatrix.append(np.column_stack((
                                ElementNumberShellWest+1e3,
                               meta.bridgedeck.NodeNumberInnerConn2[:-1],
                               meta.bridgedeck.NodeNumberCogConn2[:-1],
                               meta.bridgedeck.NodeNumberCogConn2[1:],
                               meta.bridgedeck.NodeNumberInnerConn2[1:],
                                )))
        bridgemesh.ElementMatrixName.append('Bridgedeck_shell_west2')
        bridgemesh.ElementType.append('S4R')
        
    
        bridgemesh.ElementSet.append(['Bridgedeck_shell_east1' , 'Bridgedeck_shell_east2' , 'Bridgedeck_shell_west1' , 'Bridgedeck_shell_west2'])
        bridgemesh.ElementSetName.append('Bridgedeck_shell')


#%%  

    if bridgedeck.N_box==1:
        bridgemesh.ElementSet.append(['Bridgedeck_cog' , 'LatConnOuter'])
    elif bridgedeck.N_box==2:
        bridgemesh.ElementSet.append(['Bridgedeck_cog' , 'LatConnOuter' , 'LatConnInner' , 'LatConnGap'])

    bridgemesh.ElementSetName.append('Bridgedeck')

#%%  Mesh and sections

    bridgemesh=GenerateMeshStruct(fid,bridgemesh)
    
    if bridgedeck.N_box==1:
        ElementName=['Bridgedeck_cog']
        
    elif bridgedeck.N_box==2:
            ElementName=['Bridgedeck1_cog' , 'Bridgedeck2_cog']

    gen.BeamGeneralSection(fid,'LatConnOuter',0,[0.1,1,0,1,1],[1,0,0],[210e9*100,81e9*100])
            
    for n in np.arange(bridgedeck.N_box):

            gen.BeamGeneralSection(fid,ElementName[n],bridgedeck.cs.rho[n],[bridgedeck.cs.A[n],bridgedeck.cs.I11[n],bridgedeck.cs.I12[n],bridgedeck.cs.I22[n],bridgedeck.cs.It[n]],bridgedeck.normaldir,[bridgedeck.cs.E[n],bridgedeck.cs.G[n]])
            gen.BeamAddedInertia(fid,bridgedeck.inertia.m[n],bridgedeck.inertia.x1[n],bridgedeck.inertia.x2[n],bridgedeck.inertia.alpha[n],bridgedeck.inertia.I11[n],bridgedeck.inertia.I22[n],bridgedeck.inertia.I12[n])
            gen.ShearCenter(fid,bridgedeck.cs.sc1[n],bridgedeck.cs.sc2[n])
            
            
    if bridgedeck.N_box==2:
        
        gen.BeamGeneralSection(fid,'LatConnInner',0,[0.1,1,0,1,1],[1,0,0],[210e9*100,81e9*100])

        if bridgedeck.gapbeam.type.upper()=='BOX':
            gen.BeamSection(fid,'LatConnGap','Steel','BOX',[bridgedeck.gapbeam.b , bridgedeck.gapbeam.h , bridgedeck.gapbeam.t , bridgedeck.gapbeam.t , bridgedeck.gapbeam.t , bridgedeck.gapbeam.t],[1,0,0])
        elif bridgedeck.gapbeam.type.upper()=='STIFF':
            gen.BeamGeneralSection(fid,'LatConnGap',0,[0.1,1,0,1,10],[1,0,0],[210e9*100,81e9*100])

    
    gen.ShellSection(fid,'Bridgedeck_shell','SOFT','OFFSET=SNEG',[0.01 , 2])

    

#%% 

    return (meta,bridgemesh)