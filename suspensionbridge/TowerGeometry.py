# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""
    
#%%

import numpy as np
import putools
from .. import gen
import warnings
from .MeshStruct import *

def TowerGeometry(fid,meta,geo,tower):

#%% 

    towermesh=InitiateMeshStruct()

#%%  Meshing elevation

    if not np.isnan(tower.N_element):
        
        z_south_east=np.linspace(geo.z_tower_base_south,geo.z_tower_top_south,tower.N_element+1)
        z_north_east=np.linspace(geo.z_tower_base_north,geo.z_tower_top_north,tower.N_element+1)
        
    elif not np.isnan(tower.meshsize):
        
        z_south_east=np.arange(geo.z_tower_base_south,geo.z_tower_top_south,tower.meshsize)
        z_north_east=np.arange(geo.z_tower_base_south,geo.z_tower_top_north,tower.meshsize)
        
        if z_south_east[-1]!=geo.z_tower_top_south:
            z_south_east=np.append(z_south_east,geo.z_tower_top_south)
        
        if z_north_east[-1]!=geo.z_tower_top_north:
            z_north_east=np.append(z_north_east,geo.z_tower_top_north)        
        
        

#%%  Nodes and elements

    x_south_east=np.ones(np.shape(z_south_east))*geo.x_tower_south
    y_south_east=np.interp(z_south_east,[geo.z_tower_base_south , geo.z_tower_top_south],[-geo.dy_tower_base_south/2 , -geo.dy_tower_top_south/2])
    
    x_south_west=x_south_east
    y_south_west=-y_south_east
    z_south_west=z_south_east
    
    x_north_east=np.ones(len(z_north_east))*geo.x_tower_north
    y_north_east=np.interp(z_north_east,[geo.z_tower_base_north , geo.z_tower_top_north],[-geo.dy_tower_base_north/2 , -geo.dy_tower_top_north/2])

    x_north_west=x_north_east
    y_north_west=-y_north_east
    z_north_west=z_north_east
    
    NodeNumber_south_east=tower.NodeNumberBase[0]+np.arange(1,len(x_south_east)+1).astype(int)
    NodeNumber_south_west=tower.NodeNumberBase[1]+np.arange(1,len(x_south_west)+1).astype(int)
    NodeNumber_north_east=tower.NodeNumberBase[2]+np.arange(1,len(x_north_east)+1).astype(int)
    NodeNumber_north_west=tower.NodeNumberBase[3]+np.arange(1,len(x_north_west)+1).astype(int)

    ElementNumber_south_east=tower.ElementNumberBase[0]+np.arange(1,len(x_south_east)).astype(int)
    ElementNumber_south_west=tower.ElementNumberBase[1]+np.arange(1,len(x_south_west)).astype(int)
    ElementNumber_north_east=tower.ElementNumberBase[2]+np.arange(1,len(x_north_east)).astype(int)
    ElementNumber_north_west=tower.ElementNumberBase[3]+np.arange(1,len(x_north_west)).astype(int)

    towermesh.NodeMatrix.append(np.column_stack((NodeNumber_south_east,x_south_east,y_south_east,z_south_east)))
    towermesh.ElementMatrix.append(np.column_stack((ElementNumber_south_east,NodeNumber_south_east[:-1],NodeNumber_south_east[1:])))
    towermesh.NodeMatrixName.append('Tower_leg_south_east')
    towermesh.ElementMatrixName.append('Tower_leg_south_east')
    towermesh.ElementType.append(tower.eltype)

    towermesh.NodeMatrix.append(np.column_stack((NodeNumber_south_west,x_south_west,y_south_west,z_south_west)))
    towermesh.ElementMatrix.append(np.column_stack((ElementNumber_south_west,NodeNumber_south_west[:-1],NodeNumber_south_west[1:])))
    towermesh.NodeMatrixName.append('Tower_leg_south_west')
    towermesh.ElementMatrixName.append('Tower_leg_south_west')
    towermesh.ElementType.append(tower.eltype)
    
    towermesh.NodeMatrix.append(np.column_stack((NodeNumber_north_east,x_north_east,y_north_east,z_north_east)))
    towermesh.ElementMatrix.append(np.column_stack((ElementNumber_north_east,NodeNumber_north_east[:-1],NodeNumber_north_east[1:])))
    towermesh.NodeMatrixName.append('Tower_leg_north_east')
    towermesh.ElementMatrixName.append('Tower_leg_north_east')
    towermesh.ElementType.append(tower.eltype)
    
    towermesh.NodeMatrix.append(np.column_stack((NodeNumber_north_west,x_north_west,y_north_west,z_north_west)))
    towermesh.ElementMatrix.append(np.column_stack((ElementNumber_north_west,NodeNumber_north_west[:-1],NodeNumber_north_west[1:])))
    towermesh.NodeMatrixName.append('Tower_leg_north_west')
    towermesh.ElementMatrixName.append('Tower_leg_north_west')
    towermesh.ElementType.append(tower.eltype)

    meta.tower.NodeNumberTop=[NodeNumber_south_east[-1],NodeNumber_south_west[-1],NodeNumber_north_east[-1],NodeNumber_north_west[-1]]
        
#%%  Elset for cross sections of tower

    for k in np.arange(len(ElementNumber_south_east)):
        gen.Elset(fid,'Tower_south_cs_' + str(k+1).zfill(3),[ElementNumber_south_east[k],ElementNumber_south_west[k]])
    
    for k in np.arange(len(ElementNumber_north_east)):
        gen.Elset(fid,'Tower_north_cs_' + str(k+1).zfill(3),[ElementNumber_north_east[k],ElementNumber_north_west[k]])
    

#%%  Sets

    # Nset 
    towermesh.NodeSet.append(['Tower_leg_south_east' , 'Tower_leg_south_west' , 'Tower_leg_north_east' , 'Tower_leg_north_west'])
    towermesh.NodeSetName.append('Tower_leg')
    
    towermesh.NodeSet.append([NodeNumber_south_east[0],NodeNumber_south_west[0],NodeNumber_north_east[0],NodeNumber_north_west[0]])
    towermesh.NodeSetName.append('Tower_base')

    towermesh.NodeSet.append(towermesh.NodeMatrix[0][-1,0])
    towermesh.NodeSetName.append('Tower_top_south_east')
    
    towermesh.NodeSet.append(towermesh.NodeMatrix[1][-1,0])
    towermesh.NodeSetName.append('Tower_top_south_west')
    
    towermesh.NodeSet.append(towermesh.NodeMatrix[2][-1,0])
    towermesh.NodeSetName.append('Tower_top_north_east')
    
    towermesh.NodeSet.append(towermesh.NodeMatrix[3][-1,0])
    towermesh.NodeSetName.append('Tower_top_north_west')

    # Elset 
    towermesh.ElementSet.append(['Tower_leg_south_east' , 'Tower_leg_south_west' , 'Tower_leg_north_east' , 'Tower_leg_north_west'])
    towermesh.ElementSetName.append('Tower_leg')

#%%  Crossbeams
    N_box=1*np.isnan(geo.gap)+2*(not np.isnan(geo.gap))
    
    meta.crossbeamlow.NodeNumberBearings=[[None]*2 for i in range(N_box)]
    
    # TODO: Remove this syntax
    meta.crossbeamlow.NodeCoordBearing=[[None]*2 for i in range(N_box)]
    
    ElementSetCrossbeam=[]
    
    S_or_N=['SOUTH','NORTH']

    for j in [0,1]:
    
        if j==0:
            z_crossbeam_all=tower.z_crossbeam_south
        elif j==1:
            z_crossbeam_all=tower.z_crossbeam_north
    
        for k in np.arange(len(z_crossbeam_all)):
            
            L_cc_towers=np.abs(np.interp(z_crossbeam_all[k],z_south_east,y_south_east))*2
            b_tower=np.interp(z_crossbeam_all[k],tower.cs.z_vec,tower.cs.b_vec)
            L_crossbeam=L_cc_towers-b_tower
            
            if L_crossbeam<0:
                warnings.warn('***** Cross-beam length smaller than 0.5 m. Set to 0.5 m.')
                L_crossbeam=0.5
            
            y_crossbeam=np.array([-L_crossbeam/2,-L_crossbeam/4,0,L_crossbeam/4,L_crossbeam/2])
            
            if k==0: # Crossbeam1
                if np.isnan(geo.gap):
                    y_crossbeam=np.hstack([-L_crossbeam/2,geo.y_bearing[0],L_crossbeam/2])
                else:
                    y_crossbeam=np.hstack([-L_crossbeam/2,geo.y_bearing[0],geo.y_bearing[1],L_crossbeam/2])
            
            LogicSortWarn=np.any(np.diff(y_crossbeam)<0)
            y_crossbeam=np.sort(y_crossbeam)
            
            if LogicSortWarn:
                    warnings.warn('***** Lower pendulum node appears to be outside crossbeam, consider moving inwards')
                
            if j==0:
                x_crossbeam=geo.x_tower_south*np.ones(np.shape(y_crossbeam))
            elif j==1:
                x_crossbeam=geo.x_tower_north*np.ones(np.shape(y_crossbeam))
            
            z_crossbeam=z_crossbeam_all[k]*np.ones(np.shape(y_crossbeam))
            
            # Assume this number is free
            NodeNumber_crossbeam=tower.NodeNumberBase[j*2]+1e3+1e2*k+np.arange(1,len(x_crossbeam)+1)
            
            towermesh.NodeMatrix.append(np.column_stack((NodeNumber_crossbeam,x_crossbeam,y_crossbeam,z_crossbeam)))
            towermesh.ElementMatrix.append(np.column_stack((NodeNumber_crossbeam[0:-1],NodeNumber_crossbeam[:-1],NodeNumber_crossbeam[1:])))
            towermesh.NodeMatrixName.append('Tower_crossbeam_' + S_or_N[j] + '_' + str(k+1))
            towermesh.ElementMatrixName.append('Tower_crossbeam_' + S_or_N[j] + ' _' + str(k+1))
            towermesh.ElementType.append('B31')
        
            ElementSetCrossbeam.append('Tower_crossbeam_' + S_or_N[j] + '_' + str(k+1))
            
            towermesh.NodeSet.append(NodeNumber_crossbeam[0])
            towermesh.NodeSetName.append('Tower_crossbeam_' + S_or_N[j] + '_' + str(k+1) + '_start')
            
            towermesh.NodeSet.append(NodeNumber_crossbeam[-1]);
            towermesh.NodeSetName.append('Tower_crossbeam_' + S_or_N[j] + '_' + str(k+1) + '_end')
    
           # Meta to bearing
            if k==0:
                
                for n in np.arange(N_box):
                
                    IndexBearing=[ np.array([2,3,4])-1,np.array([2,3,4])-1+3 ]
    
                    meta.crossbeamlow.NodeNumberBearings[n][j]=NodeNumber_crossbeam[IndexBearing[n]]
                    meta.crossbeamlow.NodeCoordBearing[n][j]=np.column_stack((x_crossbeam[IndexBearing[n]],y_crossbeam[IndexBearing[n]],z_crossbeam[IndexBearing[n]])).T
                    
    towermesh.ElementSet.append(ElementSetCrossbeam)
    towermesh.ElementSetName.append('Tower_crossbeam')
    
    towermesh.ElementSetName.append('Tower')
    towermesh.ElementSet.append(['Tower_leg' , 'Tower_crossbeam'])

#%%  Generate

    towermesh=GenerateMeshStruct(fid,towermesh)

#%%  Section

    if tower.cs.type.upper()=='BOX':

        for k in np.arange(len(ElementNumber_north_east)):

            h_interp=np.interp(z_north_east[k],tower.cs.z_vec,tower.cs.h_vec)
            b_interp=np.interp(z_north_east[k],tower.cs.z_vec,tower.cs.b_vec)
            t_interp=np.interp(z_north_east[k],tower.cs.z_vec,tower.cs.t_vec)

            gen.BeamSection(fid,'Tower_south_cs_' + str(k+1).zfill(3),'CONCRETE','BOX',[h_interp,b_interp,t_interp,t_interp,t_interp,t_interp],tower.normaldir)
            gen.BeamSection(fid,'Tower_north_cs_' + str(k+1).zfill(3),'CONCRETE','BOX',[h_interp,b_interp,t_interp,t_interp,t_interp,t_interp],tower.normaldir)


    for k in np.arange(len(z_crossbeam_all)):
        elset=[ 'Tower_crossbeam_SOUTH' + '_' + str(k+1) , 'Tower_crossbeam_NORTH' + '_' + str(k+1)]
        gen.BeamSection(fid,elset,'CONCRETE','BOX',[tower.b_crossbeam[k],tower.h_crossbeam[k],tower.t_crossbeam[k],tower.t_crossbeam[k],tower.t_crossbeam[k],tower.t_crossbeam[k]],[1,0,0])


# Stiff beam from crossbeam center to surface
    meta.bearing.H_stiffbeam=tower.h_crossbeam[0]/2

#%%  MPC crossbeams

    for k in np.arange(len(tower.z_crossbeam_south)):
    
        ind=np.argmin(np.abs(z_south_east-tower.z_crossbeam_south[k]))
        gen.Nset(fid,['Tower_leg_south_crossbeam_' + str(k+1) + '_start'],NodeNumber_south_east[ind])
        gen.MPC(fid,'BEAM',['Tower_crossbeam_south_' + str(k+1) + '_start' , 'Tower_leg_south_crossbeam_' + str(k+1) + '_start'])

        ind=np.argmin(np.abs(z_south_west-tower.z_crossbeam_south[k]))
        gen.Nset(fid,['Tower_leg_south_crossbeam_' + str(k+1) + '_end'],NodeNumber_south_west[ind])
        gen.MPC(fid,'BEAM',['Tower_crossbeam_south_' + str(k+1) + '_end' , 'Tower_leg_south_crossbeam_' + str(k+1) + '_end'])


    for k in np.arange(len(tower.z_crossbeam_north)):
    
        ind=np.argmin(np.abs(z_south_east-tower.z_crossbeam_north[k]))
        gen.Nset(fid,['Tower_leg_north_crossbeam_' + str(k+1) + '_start'],NodeNumber_north_east[ind])
        gen.MPC(fid,'BEAM',['Tower_crossbeam_north_' + str(k+1) + '_start' , 'Tower_leg_north_crossbeam_' + str(k+1) + '_start'])

        ind=np.argmin(np.abs(z_south_west-tower.z_crossbeam_north[k]))
        gen.Nset(fid,['Tower_leg_north_crossbeam_' + str(k+1) + '_end'],NodeNumber_north_west[ind])
        gen.MPC(fid,'BEAM',['Tower_crossbeam_north_' + str(k+1) + '_end' , 'Tower_leg_north_crossbeam_' + str(k+1) + '_end'])


#%% 

    return (meta,towermesh)