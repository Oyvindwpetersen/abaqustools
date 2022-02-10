# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""
    
#%%

import numpy as np
import numtools
import gen
from .MeshStruct import *

#%%

def CableGeometry(fid,meta,geo,cable):
   
    cablemesh=InitiateMeshStruct()
    
#%% Mesh size of size spans

    # if cable.N_element is not given, then find number of elements from mesh size
    if np.isnan(cable.N_element):
            
        dx=geo.x_tower_south-geo.dx_tower_anch_south    -   geo.x_tower_south+geo.dx_pullback_south
        dy=geo.dy_cable_anch_south/2    -   geo.dy_cable_top_south/2
        dz=geo.z_anch_south     -   geo.z_cable_top_south
    
        L_sidespan_south=np.sqrt(dx**2+dy**2+dz**2)
        N_el_sidespan_south=np.ceil(L_sidespan_south/cable.meshsize_approx).astype(int)
    
        dx=geo.x_tower_north-geo.dx_tower_anch_north    -   geo.x_tower_north+geo.dx_pullback_north
        dy=geo.dy_cable_anch_north/2    -    geo.dy_cable_top_north/2
        dz=geo.z_anch_north    -    geo.z_cable_top_north
        
        L_sidespan_north=np.sqrt(dx**2+dy**2+dz**2) 
        N_el_sidespan_north=np.ceil(L_sidespan_north/cable.meshsize_approx).astype(int)
    
    else:
        N_el_sidespan_south=cable.N_element
        N_el_sidespan_north=cable.N_element

#%% Geometry sidespan

    x_sidespan_south=np.linspace(geo.x_tower_south-geo.dx_tower_anch_south,geo.x_tower_south+geo.dx_pullback_south,N_el_sidespan_south+1)
    y_sidespan_south=-np.linspace(geo.dy_cable_anch_south/2,geo.dy_cable_top_south/2,N_el_sidespan_south+1)
    z_sidespan_south=np.linspace(geo.z_anch_south,geo.z_cable_top_south,N_el_sidespan_south+1)
    
    x_sidespan_north=np.linspace(geo.x_tower_north+geo.dx_pullback_north,geo.x_tower_north+geo.dx_tower_anch_south,N_el_sidespan_north+1)
    y_sidespan_north=-np.linspace(geo.dy_cable_top_north/2,geo.dy_cable_anch_north/2,N_el_sidespan_north+1)
    z_sidespan_north=np.linspace(geo.z_cable_top_north,geo.z_anch_north,N_el_sidespan_north+1)

#%% Geometry span

    # Add hangers until exceeding limit
    x_hanger=np.array([0.0])
    for k in np.arange(1000):
       
       if np.abs(x_hanger[-1]-geo.L_bridgedeck/2)>geo.dx_endpiece_max:
           x_hanger=np.hstack((x_hanger[0]-geo.dx_hanger , x_hanger , x_hanger[-1]+geo.dx_hanger))
       else:

          meta.bridgedeck.dx_endpiece=geo.L_bridgedeck/2-x_hanger[-1]
          break
      
    # Adjustment of hanger nodes due to deflection in x-direction
    # Nodes are moved by polynomial function shift
    if np.isnan(cable.polycoeff_hanger_adjust).any():
        x_hanger_eff=x_hanger
    else:
        x_hat=x_hanger/(geo.L_bridgedeck/2) # axis from -1 to 1 along bridge deck
        dx_hanger_eff=np.polyval(cable.polycoeff_hanger_adjust,x_hat)
        x_hanger_eff=x_hanger-dx_hanger_eff;
    
    x_mainspan=np.hstack((x_sidespan_south[-1] , x_hanger_eff , x_sidespan_north[0]))

    # Parabolic
    geo.z_cable_midspan_eff=geo.z_cable_midspan+geo.dz_cable_deflection
    
    abc_coeff=np.polyfit([x_mainspan[0],0,x_mainspan[-1]],[geo.z_cable_top_south,geo.z_cable_midspan_eff,geo.z_cable_top_north],2)
    z_mainspan=np.polyval(abc_coeff,x_mainspan)
    
    abc_coeff=np.polyfit([x_mainspan[0],0,x_mainspan[-1]],[-geo.dy_cable_top_south/2,-geo.dy_cable_midspan/2,-geo.dy_cable_top_north/2],2)
    y_mainspan=np.polyval(abc_coeff,x_mainspan)

#%% Assemble

    x_east=np.hstack((x_sidespan_south,x_mainspan[1:-1],x_sidespan_north))
    y_east=np.hstack((y_sidespan_south,y_mainspan[1:-1],y_sidespan_north))
    z_east=np.hstack((z_sidespan_south,z_mainspan[1:-1],z_sidespan_north))
    
    x_west=x_east
    y_west=-y_east
    z_west=z_east

#%% Nodes and elements

    NodeNumber_east=cable.NodeNumberBase[0]+np.arange(1,len(x_east)+1).astype(int)
    ElementNumber_east=cable.ElementNumberBase[0]+np.arange(1,len(x_east)).astype(int)
    
    NodeNumber_west=cable.NodeNumberBase[1]+np.arange(1,len(x_west)+1).astype(int)
    ElementNumber_west=cable.ElementNumberBase[1]+np.arange(1,len(x_west)).astype(int)
    
    cablemesh.NodeMatrix.append(np.column_stack((NodeNumber_east,x_east,y_east,z_east)))
    cablemesh.ElementMatrix.append(np.column_stack((ElementNumber_east,NodeNumber_east[:-1],NodeNumber_east[1:])))
    cablemesh.NodeMatrixName.append('Cable_main_east')
    cablemesh.ElementMatrixName.append('Cable_main_east')
    cablemesh.ElementType.append(cable.eltype)
    
    cablemesh.NodeMatrix.append(np.column_stack((NodeNumber_west,x_west,y_west,z_west)))
    cablemesh.ElementMatrix.append(np.column_stack((ElementNumber_west,NodeNumber_west[:-1],NodeNumber_west[1:])))
    cablemesh.NodeMatrixName.append('Cable_main_west')
    cablemesh.ElementMatrixName.append('Cable_main_west')
    cablemesh.ElementType.append(cable.eltype)

#%% Sets

    # Node set anchorage

    cablemesh.NodeSet.append(np.array([NodeNumber_east[0],NodeNumber_east[-1],NodeNumber_west[0],NodeNumber_west[-1]]))
    cablemesh.NodeSetName.append('Cable_main_anchorage')
    
    meta.cable.NodeNumberTop=[]
    
    # Node set cable top
    LogicSouth=x_east<0
    LogicNorth=x_east>0
    
    IndexSub=np.argmax(z_east[LogicSouth])
    IndexParent=np.arange(z_east.shape[0])[LogicSouth][IndexSub]
    cablemesh.NodeSet.append(NodeNumber_east[IndexParent])
    cablemesh.NodeSetName.append('Cable_main_top_south_east')
    meta.cable.NodeNumberTop.append(cablemesh.NodeSet[-1])
    
    IndexSub=np.argmax(z_west[LogicSouth])
    IndexParent=np.arange(z_west.shape[0])[LogicSouth][IndexSub]
    cablemesh.NodeSet.append(NodeNumber_west[IndexParent])
    cablemesh.NodeSetName.append('Cable_main_top_south_west')
    meta.cable.NodeNumberTop.append(cablemesh.NodeSet[-1])
    
    IndexSub=np.argmax(z_east[LogicNorth])
    IndexParent=np.arange(z_east.shape[0])[LogicNorth][IndexSub]
    cablemesh.NodeSet.append(NodeNumber_east[IndexParent])
    cablemesh.NodeSetName.append('Cable_main_top_north_east')
    meta.cable.NodeNumberTop.append(cablemesh.NodeSet[-1])
    
    IndexSub=np.argmax(z_west[LogicNorth])
    IndexParent=np.arange(z_west.shape[0])[LogicNorth][IndexSub]
    cablemesh.NodeSet.append(NodeNumber_west[IndexParent])
    cablemesh.NodeSetName.append('Cable_main_top_north_west')
    meta.cable.NodeNumberTop.append(cablemesh.NodeSet[-1])
    
    cablemesh.NodeSet.append(['Cable_main_top_south_east' , 'Cable_main_top_south_west' , 'Cable_main_top_north_east' , 'Cable_main_top_north_west'])
    cablemesh.NodeSetName.append('Cable_main_top')

    # Elset cable
    cablemesh.ElementSet.append(['Cable_main_east' , 'Cable_main_west'])
    cablemesh.ElementSetName.append('Cable_main')
    
    # Node set mainspan
    IndexMainEast=np.flatnonzero(np.abs(x_east)<geo.L_bridgedeck/2)
    IndexMainWest=np.flatnonzero(np.abs(x_west)<geo.L_bridgedeck/2)
    
    cablemesh.NodeSet.append(np.hstack((NodeNumber_east[IndexMainEast],NodeNumber_west[IndexMainWest])))
    cablemesh.NodeSetName.append('Cable_main_span')
    
    # El set mainspan
    IndexMainEast2=[IndexMainEast[0]-1]+IndexMainEast
    cablemesh.ElementSet.append(np.hstack((ElementNumber_east[IndexMainEast2],ElementNumber_west[IndexMainEast2])))
    cablemesh.ElementSetName.append('Cable_main_span')


#%% Meta

    meta.cable.NodeNumberEastHanger=NodeNumber_east[IndexMainEast]
    meta.cable.NodeNumberWestHanger=NodeNumber_west[IndexMainWest]
    
    meta.x_hanger=x_hanger

#%% Temp support

    if cable.tempsupport==True:
        
        ElementNumberTempSupport=510e3+np.arange(1,cable.N_tempsupport+1)
        
        n_hanger_space=np.floor(len(x_hanger)/(cable.N_tempsupport+1)).astype(int)
        
        if np.mod(cable.N_tempsupport,2)!=1:
            cable.N_tempsupport
            raise Exception('***** Number of temp cable support must be odd')
        
        
        n_per_side=(cable.N_tempsupport-1)/2;
        ind_temp=np.arange(1,n_per_side+1)*n_hanger_space;
        index_tempsupport=np.hstack((-np.flip(ind_temp),0,ind_temp))+(len(x_hanger)+1)/2
        index_tempsupport=index_tempsupport.astype('int')
        
        cablemesh.ElementMatrix.append(np.column_stack((ElementNumberTempSupport,meta.cable.NodeNumberWestHanger[index_tempsupport],meta.cable.NodeNumberEastHanger[index_tempsupport])))
        
        cablemesh.ElementMatrixName.append('CABLE_TEMPSUPPORT')
        cablemesh.ElementType.append('B31')
    

#%% Return if only mesh is needed without writing to file

    if fid==None:
        return (meta,cablemesh)
    
#%% Section
    # raise Exception('*************************************')
    cablemesh=GenerateMeshStruct(fid,cablemesh)
    
    gen.BeamGeneralSection(fid,'Cable_main',cable.cs.rho,[cable.cs.A , cable.cs.I11 , cable.cs.I12 , cable.cs.I22 , cable.cs.It],cable.normaldir,[cable.cs.E,cable.cs.G])
    
    if cable.tempsupport==True:
        gen.BeamGeneralSection(fid,'CABLE_TEMPSUPPORT',0,[0.1 , 1 , 0 , 1 , 1],[1,0,0],[210e9*100,81e9*100])


#%% 

    return (meta,cablemesh)
