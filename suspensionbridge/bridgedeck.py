# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""
    
#%%

import numpy as np
from numpy import matlib
import putools
from .. import gen
from .mesh import *


def bridgedeckgeometry(fid,meta,geo,bridgedeck):
#%% 
    
    bridgemesh=mesh_node_el()
    
#%%  Mesh size
    
    N_element_pr_hanger=(geo.dx_hanger/bridgedeck.meshsize)
    
    # Set as integer
    if np.abs(N_element_pr_hanger-round(N_element_pr_hanger)) > 1e-2:
        print('***** Ratio geo.dx_hanger/bridgedeck.meshsize = '  + putools.num.num2strf(N_element_pr_hanger,5))
        raise Exception('***** The hanger distance and bridge deck mesh size must divide into an integer')
    else:
        N_element_pr_hanger=round(N_element_pr_hanger)


#%%  Bridge deck geometry
    
    # Nodes from first to last hanger
    x_node_mid=np.arange(meta.x_hanger[0],meta.x_hanger[-1]+bridgedeck.meshsize,bridgedeck.meshsize)
    
    x_node_endpiece=np.arange(bridgedeck.meshsize,(np.ceil(meta.bridgedeck.dx_endpiece/bridgedeck.meshsize)+1)*bridgedeck.meshsize,bridgedeck.meshsize)
   
    if np.abs(x_node_endpiece[-1]-meta.bridgedeck.dx_endpiece)>1e-3:
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
        
        nodenum_temp=bridgedeck.nodenum_base[0]+np.arange(1,len(x_bridgedeck_cog)+1).astype(int)    
        bridgemesh.addnode(np.column_stack((nodenum_temp,x_bridgedeck_cog,y_bridgedeck_cog,z_bridgedeck_cog)),'Bridgedeck_cog')
        
        elnum_temp=bridgedeck.elnum_base[0]+np.arange(1,len(x_bridgedeck_cog)).astype(int)
        bridgemesh.addel(np.column_stack((elnum_temp,nodenum_temp[:-1],nodenum_temp[1:])),'Bridgedeck_cog',bridgedeck.eltype)
        
        meta.bridgedeck.nodenum_bridgedeck=[nodenum_temp]
        
        meta.bridgedeck.nodecoord_end_box1=[None]*2
        meta.bridgedeck.nodecoord_end_box1[0]=np.array([x_bridgedeck_cog[0],y_bridgedeck_cog[0],z_bridgedeck_cog[0]])
        meta.bridgedeck.nodecoord_end_box1[1]=np.array([x_bridgedeck_cog[-1],y_bridgedeck_cog[-1],z_bridgedeck_cog[-1]]) 

#%%  Twin box
    
    if bridgedeck.N_box==2:
        
        meta.bridgedeck.nodenum_bridgedeck=[None]*5
        meta.bridgedeck.nodecoord_end_box1=[None]*2
        meta.bridgedeck.nodecoord_end_box2=[None]*2
        
        for n in np.arange(5):
            
            x_node=x_bridgedeck_cog
        
            if n==0:
                y_node=-geo.gap/2*np.ones(np.shape(x_node))
                z_node=z_bridgedeck_cog
                node_name='Bridgedeck' + str(n+1) + '_cog'
            elif n==1:
                y_node=geo.gap/2*np.ones(np.shape(x_node))
                z_node=z_bridgedeck_cog
                node_name='Bridgedeck' + str(n+1) + '_cog'
            elif n==2:
                y_node=(-geo.gap/2+geo.dy_cog_inner)*np.ones(np.shape(x_node))
                z_node=z_bridgedeck_cog+geo.dz_cog_inner
                node_name='Bridgedeck' + '_inner_east'
            elif n==3:
                y_node=(geo.gap/2-geo.dy_cog_inner)*np.ones(np.shape(x_node))
                z_node=z_bridgedeck_cog+geo.dz_cog_inner
                node_name='Bridgedeck' + '_inner_west'
            elif n==4:
                y_node=np.zeros(np.shape(x_node))
                z_node=z_bridgedeck_cog+geo.dz_cog_inner
                node_name='Bridgedeck' + '_gapmid'
        
            nodenum_temp=bridgedeck.nodenum_base[n]+np.arange(1,len(x_node)+1).astype(int)
            bridgemesh.addnode(np.column_stack((nodenum_temp,x_node,y_node,z_node)),node_name)

            
            if n==0 or n==1:
                elnum_temp=bridgedeck.elnum_base[n]+np.arange(1,len(x_bridgedeck_cog)).astype(int)
                bridgemesh.addel(np.column_stack((elnum_temp,nodenum_temp[:-1],nodenum_temp[1:])),'Bridgedeck' + str(n+1) + '_cog',bridgedeck.eltype)
                
            if n==0:
                meta.bridgedeck.nodecoord_end_box1[0]=np.array([x_node[0],y_node[0],z_node[0]])
                meta.bridgedeck.nodecoord_end_box1[1]=np.array([x_node[-1],y_node[-1],z_node[-1]])
            elif n==1:    
                meta.bridgedeck.nodecoord_end_box2[0]=np.array([x_node[0],y_node[0],z_node[0]])
                meta.bridgedeck.nodecoord_end_box2[1]=np.array([x_node[-1],y_node[-1],z_node[-1]])
        
        
            meta.bridgedeck.nodenum_bridgedeck[n]=nodenum_temp

        bridgemesh.addelset(['Bridgedeck1_cog' , 'Bridgedeck2_cog'],'Bridgedeck_cog')


#%%  Nodes for outer

    x_outer_east=x_bridgedeck_cog
    z_outer_east=z_bridgedeck_cog+geo.dz_cog_hanger

    if bridgedeck.N_box==1:
        y_outer_east=-geo.dy_cog_hanger*np.ones(np.shape(x_outer_east))
    elif bridgedeck.N_box==2:
        y_outer_east=(-geo.dy_cog_hanger-geo.gap/2)*np.ones(np.shape(x_outer_east))

    # Select only nodes where hangers are (and start/end)
    idx_latconn=putools.num.argmin(x_bridgedeck_cog,meta.x_hanger)
    idx_latconn=np.hstack((0,idx_latconn,-1))

    nodenum_outer_east=bridgedeck.nodenum_base_outer[0]+np.arange(1,len(x_outer_east)+1).astype(int)
    bridgemesh.addnode(np.column_stack((nodenum_outer_east[idx_latconn],x_outer_east[idx_latconn],y_outer_east[idx_latconn],z_outer_east[idx_latconn])),'Bridgeouter_east')

    x_outer_west=x_outer_east
    y_outer_west=-y_outer_east
    z_outer_west=z_outer_east

    nodenum_outer_west=bridgedeck.nodenum_base_outer[1]+np.arange(1,len(x_outer_west)+1).astype(int)
    bridgemesh.addnode(np.column_stack((nodenum_outer_west[idx_latconn],x_outer_east[idx_latconn],y_outer_west[idx_latconn],z_outer_west[idx_latconn])),'Bridgeouter_west')

#%%  Connective elements lateral

    N_latconn=len(idx_latconn)

    # From hanger to bridge deck(s) cog
    if bridgedeck.N_box==1:
        meta.bridgedeck.nodenum_cog_conn_1=meta.bridgedeck.nodenum_bridgedeck[0][idx_latconn]
        meta.bridgedeck.nodenum_cog_conn_2=meta.bridgedeck.nodenum_bridgedeck[0][idx_latconn]
    elif bridgedeck.N_box==2:
        meta.bridgedeck.nodenum_cog_conn_1=meta.bridgedeck.nodenum_bridgedeck[0][idx_latconn]
        meta.bridgedeck.nodenum_cog_conn_2=meta.bridgedeck.nodenum_bridgedeck[1][idx_latconn]
        meta.bridgedeck.nodenum_inner_conn_1=meta.bridgedeck.nodenum_bridgedeck[2][idx_latconn]
        meta.bridgedeck.nodenum_inner_conn_2=meta.bridgedeck.nodenum_bridgedeck[3][idx_latconn]
        meta.bridgedeck.nodenum_mid_conn=meta.bridgedeck.nodenum_bridgedeck[4][idx_latconn]


    meta.bridgedeck.nodenum_conn_outer_east=nodenum_outer_east[idx_latconn]
    meta.bridgedeck.nodenum_conn_outer_west=nodenum_outer_west[idx_latconn]

    # meta.bridgedeck.NodeNumberCogHanger=NodeNumberBridgeDeck(ind(2:-1]]
    meta.bridgedeck.nodenum_hanger_east=nodenum_outer_east[idx_latconn[1:-1]]
    meta.bridgedeck.nodenum_hanger_west=nodenum_outer_west[idx_latconn[1:-1]]


    elnum_latconn_outer_east=bridgedeck.elnum_base_connlat[0]+np.arange(1,N_latconn+1).astype(int)
    bridgemesh.addel(np.column_stack((elnum_latconn_outer_east,meta.bridgedeck.nodenum_cog_conn_1,meta.bridgedeck.nodenum_conn_outer_east)),'LatConnOuterEast','B31')

    elnum_latconn_outer_west=bridgedeck.elnum_base_connlat[1]+np.arange(1,N_latconn+1).astype(int)
    bridgemesh.addel(np.column_stack((elnum_latconn_outer_west,meta.bridgedeck.nodenum_cog_conn_2,meta.bridgedeck.nodenum_conn_outer_west)),'LatConnOuterWest','B31')

    bridgemesh.addelset(['LatConnOuterEast' , 'LatConnOuterWest'],'LatConnOuter')

    # From cog to inner
    if bridgedeck.N_box==2:

        elnum_latconn_inner_east=bridgedeck.elnum_base_connlat[2]+np.arange(1,N_latconn+1).astype(int)
        bridgemesh.addel(np.column_stack((elnum_latconn_inner_east,meta.bridgedeck.nodenum_cog_conn_1,meta.bridgedeck.nodenum_inner_conn_1)),'LatConnInnerEast','B31')
        
        elnum_latconn_inner_west=bridgedeck.elnum_base_connlat[3]+np.arange(1,N_latconn+1).astype(int)
        bridgemesh.addel(np.column_stack((elnum_latconn_inner_west,meta.bridgedeck.nodenum_cog_conn_2,meta.bridgedeck.nodenum_inner_conn_2)),'LatConnInnerWest','B31')

        bridgemesh.addelset(['LatConnInnerEast' , 'LatConnInnerWest'],'LatConnInner')

    # From gapmid to inner
    if bridgedeck.N_box==2:

        elnum_temp=bridgedeck.elnum_base_connlat[4]+np.arange(1,N_latconn+1).astype(int)
        bridgemesh.addel(np.column_stack((elnum_temp,meta.bridgedeck.nodenum_mid_conn,meta.bridgedeck.nodenum_inner_conn_1)),'LatConnGapEast','B31')

        elnum_temp=bridgedeck.elnum_base_connlat[5]+np.arange(1,N_latconn+1).astype(int)
        bridgemesh.addel(np.column_stack((elnum_temp,meta.bridgedeck.nodenum_mid_conn,meta.bridgedeck.nodenum_inner_conn_2)),'LatConnGapWest','B31')
        
        bridgemesh.addelset(['LatConnGapWest' , 'LatConnGapEast'],'LatConnGap')
#%% 

    meta.bridgedeck.nodenum_end_box1=[None]*2
    meta.bridgedeck.nodenum_end_box2=[None]*2
    if bridgedeck.N_box==1:
        
        meta.bridgedeck.nodenum_end_box1[0]=[ nodenum_outer_east[0],meta.bridgedeck.nodenum_bridgedeck[0][0],nodenum_outer_west[0], ]
        meta.bridgedeck.nodenum_end_box1[1]=[ nodenum_outer_east[-1],meta.bridgedeck.nodenum_bridgedeck[0][-1],nodenum_outer_west[-1] ]
    
    elif bridgedeck.N_box==2:
    
        # Outer east, deck 1, inner east
        meta.bridgedeck.nodenum_end_box1[0]=[ nodenum_outer_east[0] , meta.bridgedeck.nodenum_bridgedeck[0][0] , meta.bridgedeck.nodenum_bridgedeck[2][0] ]
        meta.bridgedeck.nodenum_end_box1[1]=[ meta.bridgedeck.nodenum_bridgedeck[0][-1] , meta.bridgedeck.nodenum_bridgedeck[1][0] , nodenum_outer_west[0] ]
        
        # Inner west, deck 2, outer west
        meta.bridgedeck.nodenum_end_box2[0]=[ nodenum_outer_east[-1] , meta.bridgedeck.nodenum_bridgedeck[0][-1] , meta.bridgedeck.nodenum_bridgedeck[2][-1] ]
        meta.bridgedeck.nodenum_end_box2[1]=[ meta.bridgedeck.nodenum_bridgedeck[3][-1] , meta.bridgedeck.nodenum_bridgedeck[1][-1] , nodenum_outer_west[-1] ]
        

#%%  Shell elements

    if bridgedeck.shell==True and bridgedeck.N_box==1:
    
        elnum_shell_east=910e3+np.arange(1,N_latconn).astype(int)
        elnum_shell_west=920e3+np.arange(1,N_latconn).astype(int)
    
        ShellMatrix1=np.column_stack((
                                elnum_shell_east,
                               nodenum_outer_east[idx_latconn[:-1]],
                               meta.bridgedeck.nodenum_cog_conn_1[:-1],
                               meta.bridgedeck.nodenum_cog_conn_1[1:],
                               nodenum_outer_east[idx_latconn[1:]],
                                ))

        ShellMatrix2=np.column_stack((
                                elnum_shell_west,
                               nodenum_outer_west[idx_latconn[:-1]],
                               meta.bridgedeck.nodenum_cog_conn_2[:-1],
                               meta.bridgedeck.nodenum_cog_conn_2[1:],
                               nodenum_outer_west[idx_latconn[1:]],
                                ))
                                
        bridgemesh.addel(np.vstack((ShellMatrix1,ShellMatrix2)),'Bridgedeck_shell','S4R')


#%%  Shell elements

    if bridgedeck.shell==True and bridgedeck.N_box==2:
        
        elnum_shell_east=910e3+np.arange(1,N_latconn).astype(int)
        elnum_shell_west=920e3+np.arange(1,N_latconn).astype(int)
    
        ShellMatrix1=np.column_stack((
                                elnum_shell_east,
                               nodenum_outer_east[idx_latconn[:-1]],
                               meta.bridgedeck.nodenum_cog_conn_1[:-1],
                               meta.bridgedeck.nodenum_cog_conn_1[1:],
                               nodenum_outer_east[idx_latconn[1:]],
                                ))
        
        ShellMatrix2=np.column_stack((
                                elnum_shell_east+1e3,
                               meta.bridgedeck.nodenum_inner_conn_1[:-1],
                               meta.bridgedeck.nodenum_cog_conn_1[:-1],
                               meta.bridgedeck.nodenum_cog_conn_1[1:],
                               meta.bridgedeck.nodenum_inner_conn_1[1:],
                                ))
        
        ShellMatrix3=np.column_stack((
                                elnum_shell_west,
                               nodenum_outer_west[idx_latconn[:-1]],
                               meta.bridgedeck.nodenum_cog_conn_2[:-1],
                               meta.bridgedeck.nodenum_cog_conn_2[1:],
                               nodenum_outer_west[idx_latconn[1:]],
                                ))
    
        ShellMatrix4=np.column_stack((
                                elnum_shell_west+1e3,
                               meta.bridgedeck.nodenum_inner_conn_2[:-1],
                               meta.bridgedeck.nodenum_cog_conn_2[:-1],
                               meta.bridgedeck.nodenum_cog_conn_2[1:],
                               meta.bridgedeck.nodenum_inner_conn_2[1:],
                                ))
        
        bridgemesh.addel(np.vstack((ShellMatrix1,ShellMatrix2,ShellMatrix3,ShellMatrix4)),'Bridgedeck_shell','S4R')

        
#%%  

    if bridgedeck.N_box==1:
        bridgemesh.addelset(['Bridgedeck_cog' , 'LatConnOuter'],'Bridgedeck')
    elif bridgedeck.N_box==2:
        bridgemesh.addelset(['Bridgedeck_cog' , 'LatConnOuter' , 'LatConnInner' , 'LatConnGap'],'Bridgedeck')

#%%  Mesh and sections

    bridgemesh.generate(fid)
    
    if bridgedeck.N_box==1:
        ElementName=['Bridgedeck_cog']
        
    elif bridgedeck.N_box==2:
        ElementName=['Bridgedeck1_cog' , 'Bridgedeck2_cog']

    gen.BeamGeneralSection(fid,'LatConnOuter',0,[0.1,1,0,1,1],[1,0,0],[210e9*10,81e9*10])
            
    for n in np.arange(bridgedeck.N_box):

            gen.BeamGeneralSection(fid,ElementName[n],bridgedeck.cs.rho[n],[bridgedeck.cs.A[n],bridgedeck.cs.I11[n],bridgedeck.cs.I12[n],bridgedeck.cs.I22[n],bridgedeck.cs.It[n]],bridgedeck.normaldir,[bridgedeck.cs.E[n],bridgedeck.cs.G[n]])
            gen.BeamAddedInertia(fid,bridgedeck.inertia.m[n],bridgedeck.inertia.x1[n],bridgedeck.inertia.x2[n],bridgedeck.inertia.alpha[n],bridgedeck.inertia.I11[n],bridgedeck.inertia.I22[n],bridgedeck.inertia.I12[n])
            gen.ShearCenter(fid,bridgedeck.cs.sc1[n],bridgedeck.cs.sc2[n])
            
            
    if bridgedeck.N_box==2:
        
        gen.BeamGeneralSection(fid,'LatConnInner',0,[0.1,1,0,1,1],[1,0,0],[210e9*10,81e9*10])

        if bridgedeck.gapbeam.type.upper()=='BOX':
            gen.BeamSection(fid,'LatConnGap','Steel','BOX',[bridgedeck.gapbeam.b , bridgedeck.gapbeam.h , bridgedeck.gapbeam.t , bridgedeck.gapbeam.t , bridgedeck.gapbeam.t , bridgedeck.gapbeam.t],[1,0,0])
        elif bridgedeck.gapbeam.type.upper()=='STIFF':
            gen.BeamGeneralSection(fid,'LatConnGap',0,[0.1,1,0,1,1],[1,0,0],[210e9*10,81e9*10])

    
    gen.ShellSection(fid,'Bridgedeck_shell','SOFT','OFFSET=SNEG',[0.01 , 3])

    

#%% 

    return (meta,bridgemesh)