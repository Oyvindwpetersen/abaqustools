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
from .mesh import *

def towergeometry(fid,meta,geo,tower):

#%% 

    towermesh=mesh_node_el()

#%%  Meshing elevation

    if not np.isnan(tower.N_element):
        
        z_south_east=np.linspace(geo.z_tower_base_south,geo.z_tower_top_south,tower.N_element+1)
        z_north_east=np.linspace(geo.z_tower_base_north,geo.z_tower_top_north,tower.N_element+1)
        
    elif not np.isnan(tower.meshsize):
        
        z_south_east=np.arange(geo.z_tower_base_south,geo.z_tower_top_south,tower.meshsize)
        z_north_east=np.arange(geo.z_tower_base_south,geo.z_tower_top_north,tower.meshsize)
        
        # Add shorter element to reach top elevation
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
    
    nodenum_south_east=tower.nodenum_base[0]+np.arange(1,len(x_south_east)+1).astype(int)
    nodenum_south_west=tower.nodenum_base[1]+np.arange(1,len(x_south_west)+1).astype(int)
    nodenum_north_east=tower.nodenum_base[2]+np.arange(1,len(x_north_east)+1).astype(int)
    nodenum_north_west=tower.nodenum_base[3]+np.arange(1,len(x_north_west)+1).astype(int)

    elnum_south_east=tower.elnum_base[0]+np.arange(1,len(x_south_east)).astype(int)
    elnum_south_west=tower.elnum_base[1]+np.arange(1,len(x_south_west)).astype(int)
    elnum_north_east=tower.elnum_base[2]+np.arange(1,len(x_north_east)).astype(int)
    elnum_north_west=tower.elnum_base[3]+np.arange(1,len(x_north_west)).astype(int)


    towermesh.addnode(np.column_stack((nodenum_south_east,x_south_east,y_south_east,z_south_east)),'Tower_leg_south_east')
    towermesh.addel(np.column_stack((elnum_south_east,nodenum_south_east[:-1],nodenum_south_east[1:])),'Tower_leg_south_east',tower.eltype)

    towermesh.addnode(np.column_stack((nodenum_south_west,x_south_west,y_south_west,z_south_west)),'Tower_leg_south_west')
    towermesh.addel(np.column_stack((elnum_south_west,nodenum_south_west[:-1],nodenum_south_west[1:])),'Tower_leg_south_west',tower.eltype)
    
    towermesh.addnode(np.column_stack((nodenum_north_east,x_north_east,y_north_east,z_north_east)),'Tower_leg_north_east')
    towermesh.addel(np.column_stack((elnum_north_east,nodenum_north_east[:-1],nodenum_north_east[1:])),'Tower_leg_north_east',tower.eltype)
    
    towermesh.addnode(np.column_stack((nodenum_north_west,x_north_west,y_north_west,z_north_west)),'Tower_leg_north_west')
    towermesh.addel(np.column_stack((elnum_north_west,nodenum_north_west[:-1],nodenum_north_west[1:])),'Tower_leg_north_west',tower.eltype)
    
    meta.tower.nodenum_top=[nodenum_south_east[-1],nodenum_south_west[-1],nodenum_north_east[-1],nodenum_north_west[-1]]
        
#%%  Elset for each cross sections of tower

    for k in np.arange(len(elnum_south_east)):
        gen.Elset(fid,'Tower_south_cs_' + str(k+1).zfill(3),[elnum_south_east[k],elnum_south_west[k]])
    
    for k in np.arange(len(elnum_north_east)):
        gen.Elset(fid,'Tower_north_cs_' + str(k+1).zfill(3),[elnum_north_east[k],elnum_north_west[k]])
    

#%%  Sets

    # Nset 
    towermesh.addnset(['Tower_leg_south_east' , 'Tower_leg_south_west' , 'Tower_leg_north_east' , 'Tower_leg_north_west'],'Tower_leg')

    towermesh.addnset([nodenum_south_east[0],nodenum_south_west[0],nodenum_north_east[0],nodenum_north_west[0]],'Tower_base')

    towermesh.addnset(nodenum_south_east[-1],'Tower_top_south_east')
 
    towermesh.addnset(nodenum_south_west[-1],'Tower_top_south_west')

    towermesh.addnset(nodenum_north_east[-1],'Tower_top_north_east')
 
    towermesh.addnset(nodenum_north_west[-1],'Tower_top_north_west')

    # Elset 
    towermesh.addelset(['Tower_leg_south_east' , 'Tower_leg_south_west' , 'Tower_leg_north_east' , 'Tower_leg_north_west'],'Tower_leg')

#%%  Crossbeams
    N_box=1*np.isnan(geo.gap)+2*(not np.isnan(geo.gap))


    # TODO: Remove this syntax ?
    meta.crossbeamlow.nodenum_bearing_box1=[None]*2
    meta.crossbeamlow.nodecoord_bearing_box1=[None]*2
    meta.crossbeamlow.nodenum_bearing_box2=[None]*2
    meta.crossbeamlow.nodecoord_bearing_box2=[None]*2
    
    elset_crossbeam=[]
    
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
            
            if k==0: # Crossbeam at bridge deck level
                if np.isnan(geo.gap):
                    y_crossbeam=np.hstack([-L_crossbeam/2,geo.y_bearing_box1,L_crossbeam/2])
                else:
                    y_crossbeam=np.hstack([-L_crossbeam/2,geo.y_bearing_box1,geo.y_bearing_box2,L_crossbeam/2])
            else:
                y_crossbeam=np.array([-L_crossbeam/2,-L_crossbeam/4,0,L_crossbeam/4,L_crossbeam/2])
                
            
            # If y_crossbeam not sorted, pendulums are outside crossbeam (crashing with tower)
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
            nodenum_crossbeam=tower.nodenum_base[j*2]+1e3+1e2*k+np.arange(1,len(x_crossbeam)+1)
            
            towermesh.addnode(np.column_stack((nodenum_crossbeam,x_crossbeam,y_crossbeam,z_crossbeam)),'Tower_crossbeam_' + S_or_N[j] + '_' + str(k+1))
            towermesh.addel(np.column_stack((nodenum_crossbeam[0:-1],nodenum_crossbeam[:-1],nodenum_crossbeam[1:])),'Tower_crossbeam_' + S_or_N[j] + '_' + str(k+1),'B31')
            
            elset_crossbeam.append('Tower_crossbeam_' + S_or_N[j] + '_' + str(k+1))
            
            towermesh.addnset(nodenum_crossbeam[0],'Tower_crossbeam_' + S_or_N[j] + '_' + str(k+1) + '_start')
            towermesh.addnset(nodenum_crossbeam[-1],'Tower_crossbeam_' + S_or_N[j] + '_' + str(k+1) + '_end')
            
           # Meta to bearing
            if k==0:
                
                for n in np.arange(N_box):
                
                    if n==0:
                        meta.crossbeamlow.nodenum_bearing_box1[j]=nodenum_crossbeam[[1,2,3]]
                        meta.crossbeamlow.nodecoord_bearing_box1[j]=np.column_stack((x_crossbeam[[1,2,3]],y_crossbeam[[1,2,3]],z_crossbeam[[1,2,3]])).T
                    elif n==1:
                        meta.crossbeamlow.nodenum_bearing_box2[j]=nodenum_crossbeam[[4,5,6]]
                        meta.crossbeamlow.nodecoord_bearing_box2[j]=np.column_stack((x_crossbeam[[4,5,6]],y_crossbeam[[4,5,6]],z_crossbeam[[4,5,6]])).T
   
                        
            
    
    towermesh.addelset(elset_crossbeam,'Tower_crossbeam')
    towermesh.addelset(['Tower_leg' , 'Tower_crossbeam'],'Tower')

#%%  Generate

    towermesh.generate(fid)

#%%  Section

    if tower.cs.type.upper()=='BOX':

        for k in np.arange(len(elnum_north_east)):
            
            h_interp=np.interp(z_north_east[k],tower.cs.z_vec,tower.cs.h_vec)
            b_interp=np.interp(z_north_east[k],tower.cs.z_vec,tower.cs.b_vec)
            t_interp=np.interp(z_north_east[k],tower.cs.z_vec,tower.cs.t_vec)
            
            gen.BeamSection(fid,'Tower_south_cs_' + str(k+1).zfill(3),'CONCRETE','BOX',[b_interp,h_interp,t_interp,t_interp,t_interp,t_interp],tower.normaldir)
            gen.BeamSection(fid,'Tower_north_cs_' + str(k+1).zfill(3),'CONCRETE','BOX',[b_interp,h_interp,t_interp,t_interp,t_interp,t_interp],tower.normaldir)
            

    for k in np.arange(len(z_crossbeam_all)):
        elset=[ 'Tower_crossbeam_SOUTH' + '_' + str(k+1) , 'Tower_crossbeam_NORTH' + '_' + str(k+1)]
        gen.BeamSection(fid,elset,'CONCRETE','BOX',[tower.b_crossbeam[k],tower.h_crossbeam[k],tower.t_crossbeam[k],tower.t_crossbeam[k],tower.t_crossbeam[k],tower.t_crossbeam[k]],[1,0,0])


# Stiff beam from crossbeam center to surface
    meta.bearing.H_stiffbeam=tower.h_crossbeam[0]/2

#%%  MPC crossbeams, tie to closest node in 

    for k in np.arange(len(tower.z_crossbeam_south)):
    
        idx=np.argmin(np.abs(z_south_east-tower.z_crossbeam_south[k]))
        gen.Nset(fid,['Tower_leg_south_crossbeam_' + str(k+1) + '_start'],nodenum_south_east[idx])
        gen.MPC(fid,'BEAM',['Tower_crossbeam_south_' + str(k+1) + '_start' , 'Tower_leg_south_crossbeam_' + str(k+1) + '_start'])

        idx=np.argmin(np.abs(z_south_west-tower.z_crossbeam_south[k]))
        gen.Nset(fid,['Tower_leg_south_crossbeam_' + str(k+1) + '_end'],nodenum_south_west[idx])
        gen.MPC(fid,'BEAM',['Tower_crossbeam_south_' + str(k+1) + '_end' , 'Tower_leg_south_crossbeam_' + str(k+1) + '_end'])


    for k in np.arange(len(tower.z_crossbeam_north)):
    
        idx=np.argmin(np.abs(z_south_east-tower.z_crossbeam_north[k]))
        gen.Nset(fid,['Tower_leg_north_crossbeam_' + str(k+1) + '_start'],nodenum_north_east[idx])
        gen.MPC(fid,'BEAM',['Tower_crossbeam_north_' + str(k+1) + '_start' , 'Tower_leg_north_crossbeam_' + str(k+1) + '_start'])

        idx=np.argmin(np.abs(z_south_west-tower.z_crossbeam_north[k]))
        gen.Nset(fid,['Tower_leg_north_crossbeam_' + str(k+1) + '_end'],nodenum_north_west[idx])
        gen.MPC(fid,'BEAM',['Tower_crossbeam_north_' + str(k+1) + '_end' , 'Tower_leg_north_crossbeam_' + str(k+1) + '_end'])


#%% 

    return (meta,towermesh)