# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""
    
#%%

import numpy as np
from .. import gen
from .mesh import *

#%%

def bearinggeometry(fid,meta,geo,bearing):

#%% 

    bearingmesh=mesh_node_el()
#%% 

    if bearing.type.upper()!='TRI':
        raise Exception('Only tri supported')

    if np.isnan(geo.gap):
        N_box=1
    else:
        N_box=2
        
    for n in np.arange(N_box):
    
        S_or_N=['SOUTH','NORTH']
    
        for j in [0,1]:
            
            # Top part of bearing
            
            # New nodes and elements in bearing
            nodenum_bearing_top=bearing.nodenum_base+n*1e3+j*1e2+np.arange(1,3+1).astype('int')
            elnum_bearing_top=bearing.elnum_base+n*1e3+j*1e2+np.arange(1,5+1).astype('int')
            
            if n==0:
                nodenum_bridge=meta.bridgedeck.nodenum_end_box1[j]
                nodecoord_bridge=meta.bridgedeck.nodecoord_end_box1[j]
                nodenum_crossbeamlow=meta.crossbeamlow.nodenum_bearing_box1[j]
                nodecoord_crossbeamlow=meta.crossbeamlow.nodecoord_bearing_box1[j]
                y_bearing=geo.y_bearing_box1
            elif n==1:
                nodenum_bridge=meta.bridgedeck.nodenum_end_box2[j]
                nodecoord_bridge=meta.bridgedeck.nodecoord_end_box2[j]
                nodenum_crossbeamlow=meta.crossbeamlow.nodenum_bearing_box2[j]
                nodecoord_crossbeamlow=meta.crossbeamlow.nodecoord_bearing_box2[j]
                y_bearing=geo.y_bearing_box2
                
            # dz is distance between center crossbeam to cog bridge
            dz=nodecoord_bridge[2]-nodecoord_crossbeamlow[2,1]
    
            x_node=np.zeros(3)
            y_node=np.zeros(3)
            z_node=np.zeros(3)

            # New node upper pendulum insertion (left)
            x_node[0]=nodecoord_bridge[0]
            y_node[0]=y_bearing[0]
            z_node[0]=nodecoord_bridge[2]
            
            # New node below bridge cog (upper slider)
            x_node[1]=nodecoord_bridge[0]
            y_node[1]=y_bearing[1]
            z_node[1]=nodecoord_bridge[2]+geo.dz_slider
               
            # New node upper pendulum insertion (right)
            x_node[2]=nodecoord_bridge[0]
            y_node[2]=y_bearing[2]
            z_node[2]=nodecoord_bridge[2]
    
            bearingmesh.addnode(np.column_stack((nodenum_bearing_top,x_node,y_node,z_node)),'BEARINGTOP' + str(n+1) + '_' + S_or_N[j] )
            
            el_node_matrix_temp=np.array( [    
                    [elnum_bearing_top[0] , nodenum_bridge[0] , nodenum_bearing_top[0] ], # Bridge deck (left) to upper pendulum insertion (left)
                    [elnum_bearing_top[1] , nodenum_bearing_top[0] , nodenum_bearing_top[1] ], # Upper pendulum insertion (left) to upper slider
                    [elnum_bearing_top[2] , nodenum_bearing_top[1] , nodenum_bearing_top[2] ], # Upper slider to upper pendulum insertion (right)
                    [elnum_bearing_top[3] , nodenum_bearing_top[2] , nodenum_bridge[2] ], # Upper pendulum insertion (right) to bridge deck (right)
                    [elnum_bearing_top[4] , nodenum_bridge[1] , nodenum_bearing_top[1] ], # Bridge deck (mid) to upper slider
                    ])
            
            bearingmesh.addel(el_node_matrix_temp,'BEARINGTOP' + str(n+1) + '_' + S_or_N[j],'B31')
            
            # Low part of bearing
            nodenum_bearing_low=nodenum_bearing_top[-1]+np.arange(1,3+1).astype('int')
            elnum_bearing_low=elnum_bearing_top[-1]+np.arange(1,3+1).astype('int')
    
            x_node=np.zeros(3)
            y_node=np.zeros(3)
            z_node=np.zeros(3)
            
            dx_bearing_base=geo.dx_bearing_base*(j==0)-geo.dx_bearing_base*(j==1)
            
            # New node lower pendulum insertion (left)
            x_node[0]=nodecoord_crossbeamlow[0,0]+dx_bearing_base
            y_node[0]=y_bearing[0]
            z_node[0]=nodecoord_crossbeamlow[2,0]+meta.bearing.H_stiffbeam
            
            # New node below bridge cog (upper slider)
            x_node[1]=nodecoord_crossbeamlow[0,1]
            y_node[1]=y_bearing[1]
            z_node[1]=nodecoord_crossbeamlow[2,1]+(dz+geo.dz_slider)
               
            # New node lower pendulum insertion (right)
            x_node[2]=nodecoord_crossbeamlow[0,2]+dx_bearing_base
            y_node[2]=y_bearing[2]
            z_node[2]=nodecoord_crossbeamlow[2,2]+meta.bearing.H_stiffbeam
            
            z_node[1]=z_node[1]-geo.dz_cog_south_deflection*(j==0)-geo.dz_cog_north_deflection*(j==1)
            
            bearingmesh.addnode(np.column_stack((nodenum_bearing_low,x_node,y_node,z_node)),'BEARINGLOW' + str(n+1) + '_' + S_or_N[j])
            
            el_node_matrix_temp=np.array( [    
                    [elnum_bearing_low[0] , nodenum_crossbeamlow[0] , nodenum_bearing_low[0] ], # Crossbeam (left) to lower pendulum insertion (left)
                    [elnum_bearing_low[1] , nodenum_crossbeamlow[1] , nodenum_bearing_low[1] ], # Crossbeam (middle) to lower slider
                    [elnum_bearing_low[2] , nodenum_crossbeamlow[2] , nodenum_bearing_low[2] ], # Crossbeam (right) to lower pendulum insertion (right)
                    ])
            
            bearingmesh.addel(el_node_matrix_temp,'BEARINGLOW' + str(n+1) + '_' + S_or_N[j],'B31')
            
            # Add pendulum
            elnum_bearing_pend=elnum_bearing_low[-1]+[1,2]
            
            el_node_matrix_temp=np.array( [    
                    [elnum_bearing_pend[0] , nodenum_bearing_low[0] , nodenum_bearing_top[0] ], # Pendulum (left)
                    [elnum_bearing_pend[1] , nodenum_bearing_low[2] , nodenum_bearing_top[2] ], # Pendulum (right)
                    ])
                    
            bearingmesh.addel(el_node_matrix_temp,'BEARINGPENDULUM' + str(n+1) + '_' + S_or_N[j],'B31')

            # Add springs
            spring_dof=['X' , 'Y' , 'Z' , 'RX' , 'RY' , 'RZ']
            elset_bearing_dof=[None]*6
            for idx_dof in np.arange(6):

                dof_number=idx_dof+1
                elnum_spring=bearing.elnum_base+1e4+n*1e3+j*1e2+dof_number
                
                el_node_matrix_temp=np.array( [    
                        [elnum_spring[0] , nodenum_bearing_low[1] , nodenum_bearing_top[1] ], #
                        ])
                    
                if j==0:
                    k_spring=bearing.stiffness_south[idx_dof]
                elif j==1:
                    k_spring=bearing.stiffness_north[idx_dof]

                elset_temp='BEARINGSPRING' + str(n+1) + '_' + S_or_N[j] + '_' + spring_dof[idx_dof]
                
                gen.Spring(fid,elset_temp,el_node_matrix_temp,dof_number,k_spring)
                elset_bearing_dof[idx_dof]=elset_temp


            # Collect all dofs in one set
            bearingmesh.addelset(elset_bearing_dof,'BEARINGSPRING' + str(n+1) + '_' + S_or_N[j])
        
    
#%% Sets

    set_cell=['BEARINGTOP1_SOUTH' , 'BEARINGTOP1_NORTH' ]
    if N_box==2:
        set_cell=set_cell + ['BEARINGTOP2_SOUTH' , 'BEARINGTOP2_NORTH']
        
    bearingmesh.addelset(set_cell,'BEARINGTOP')
    
    set_cell=['BEARINGLOW1_SOUTH' , 'BEARINGLOW1_NORTH' ]
    if N_box==2:
        set_cell=set_cell + ['BEARINGLOW2_SOUTH' , 'BEARINGLOW2_NORTH']
    bearingmesh.addelset(set_cell,'BEARINGLOW')
    
    set_cell=['BEARINGPENDULUM1_SOUTH' , 'BEARINGPENDULUM1_NORTH' ]
    if N_box==2:
        set_cell=set_cell + ['BEARINGPENDULUM2_SOUTH' , 'BEARINGPENDULUM2_NORTH']
    bearingmesh.addelset(set_cell,'BEARINGPENDULUM')
    
    set_cell=['BEARINGSPRING1_SOUTH' , 'BEARINGSPRING1_NORTH' ]
    if N_box==2:
        set_cell=set_cell + ['BEARINGSPRING2_SOUTH' , 'BEARINGSPRING2_NORTH']
    bearingmesh.addelset(set_cell,'BEARINGSPRING')
    
    bearingmesh.addelset(['BEARINGLOW' , 'BEARINGTOP' , 'BEARINGPENDULUM' , 'BEARINGSPRING'],'BEARING')
    
#%%  Mesh and sections

    bearingmesh.generate(fid)
    
    gen.BeamGeneralSection(fid,'BEARINGTOP',0,[0.1,1,0,1,1],[1,0,0],[210e9*10,81e9*10])
    gen.BeamGeneralSection(fid,'BEARINGLOW',0,[0.1,1,0,1,1],[1,0,0],[210e9*10,81e9*10])
    
    gen.BeamSection(fid,'BEARINGPENDULUM','STEEL','BOX',[0.2,0.2,0.02,0.02,0.02,0.02],[0,1,0])

    gen.Release(fid,'BEARINGPENDULUM',['S1' , 'S2'],'M1-M2')



#%% 

    return (meta,bearingmesh)