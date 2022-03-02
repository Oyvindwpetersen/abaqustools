# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""
    
#%%

import numpy as np
from .. import numtools
from .. import gen

from .MeshStruct import *

#%%

def BearingGeometry(fid,meta,geo,bearing):

#%% 

    bearingmesh=InitiateMeshStruct()

#%% 

    if bearing.type.upper()!='TRI':
        raise Exception('Only tri supported')

    if np.isnan(geo.gap):
        N_bridgedeck=1
    else:
        N_bridgedeck=2
        
    for n in np.arange(N_bridgedeck):
    
        S_or_N=['SOUTH','NORTH']
    
        for j in [0,1]:
            
            # New nodes and elements in bearing
            NodeNumber=bearing.NodeNumberBase+j*1e3+n*1e2+np.arange(1,3+1).astype('int')
            ElementNumber=bearing.ElementNumberBase+j*1e3+n*1e2+np.arange(1,5+1).astype('int')
            
            # Node number of bridge deck left, cog, right
            NodeNumber_Bridge=meta.bridgedeck.NodeNumberBearing[n][j][0:3]
             
            # dz is distance between center crossbeam to
            
            dz=meta.bridgedeck.NodeCoordBearing[n][j][2,0]-meta.crossbeamlow.NodeCoordBearing[n][j][2,0]
    
            x_node=np.zeros(3)
            y_node=np.zeros(3)
            z_node=np.zeros(3)

            # New node below hanger (pendulum insertion point)
            x_node[0]=meta.bridgedeck.NodeCoordBearing[n][j][0,0]
            y_node[0]=geo.y_bearing[n][0]
            z_node[0]=meta.bridgedeck.NodeCoordBearing[n][j][2,0]
            
            # New node below bridge cog
            x_node[1]=meta.bridgedeck.NodeCoordBearing[n][j][0,1]
            y_node[1]=geo.y_bearing[n][1]
            z_node[1]=meta.bridgedeck.NodeCoordBearing[n][j][2,1]+geo.dz_slider
               
            # New node below hanger (pendulum insertion point)
            x_node[2]=meta.bridgedeck.NodeCoordBearing[n][j][0,2]
            y_node[2]=geo.y_bearing[n][2]
            z_node[2]=meta.bridgedeck.NodeCoordBearing[n][j][2,2]
    
    
            bearingmesh.NodeMatrix.append(np.column_stack((NodeNumber,x_node,y_node,z_node)))
                        
            Node_start=[NodeNumber_Bridge[0],NodeNumber[0],NodeNumber[1],NodeNumber[2],NodeNumber_Bridge[1]]
            Node_end=[NodeNumber[0],NodeNumber[1],NodeNumber[2],NodeNumber_Bridge[2],NodeNumber[1]]
            
            bearingmesh.ElementMatrix.append(np.column_stack((ElementNumber,Node_start,Node_end)))
        
            bearingmesh.NodeMatrixName.append('BEARINGTOP' + str(n+1) + '_' + S_or_N[j] )
            bearingmesh.ElementMatrixName.append('BEARINGTOP' + str(n+1) + '_' + S_or_N[j] )
            bearingmesh.ElementType.append('B31')
            
    
            NodeNumber=NodeNumber[-1]+np.arange(1,3+1).astype('int')
            ElementNumber=ElementNumber[-1]+np.arange(1,3+1).astype('int')
            NodeNumber_Crossbeam=meta.crossbeamlow.NodeNumberBearings[n][j][0:3]
    
            x_node=np.zeros(3)
            y_node=np.zeros(3)
            z_node=np.zeros(3)
            
            dx_bearing_base=geo.dx_bearing_base*(j==0)-geo.dx_bearing_base*(j==1)
            
            # New node above
            x_node[0]=meta.crossbeamlow.NodeCoordBearing[n][j][0,0]+dx_bearing_base
            y_node[0]=meta.crossbeamlow.NodeCoordBearing[n][j][1,0]
            z_node[0]=meta.crossbeamlow.NodeCoordBearing[n][j][2,0]+meta.bearing.H_stiffbeam
            
            # New node above
            x_node[1]=meta.crossbeamlow.NodeCoordBearing[n][j][0,1]+dx_bearing_base
            y_node[1]=meta.crossbeamlow.NodeCoordBearing[n][j][1,1]
            z_node[1]=meta.crossbeamlow.NodeCoordBearing[n][j][2,1]+(dz+geo.dz_slider)
               
            # New node above
            x_node[2]=meta.crossbeamlow.NodeCoordBearing[n][j][0,2]+dx_bearing_base
            y_node[2]=meta.crossbeamlow.NodeCoordBearing[n][j][1,2]
            z_node[2]=meta.crossbeamlow.NodeCoordBearing[n][j][2,2]+meta.bearing.H_stiffbeam
            
            
            z_node[1]=z_node[1]-geo.dz_cog_south_deflection*(j==0)-geo.dz_cog_north_deflection*(j==1)
    
            bearingmesh.NodeMatrix.append(np.column_stack((NodeNumber,x_node,y_node,z_node)))

            Node_start=[NodeNumber_Crossbeam[0],NodeNumber_Crossbeam[1],NodeNumber_Crossbeam[2]]
            Node_end=[NodeNumber[0],NodeNumber[1],NodeNumber[2]]
            bearingmesh.ElementMatrix.append(np.column_stack((ElementNumber,Node_start,Node_end)))

            bearingmesh.NodeMatrixName.append('BEARINGLOW' + str(n+1) + '_' + S_or_N[j])
            bearingmesh.ElementMatrixName.append('BEARINGLOW' + str(n+1) + '_' + S_or_N[j])
            bearingmesh.ElementType.append('B31')
        
        
            # Add pendulum
            ElementNumber=ElementNumber[-1]+[1,2]
            NodeNumber=bearing.NodeNumberBase+j*1e3+n*1e2+[1,3,1+3,3+3]
            
            Node_start=[NodeNumber[0],NodeNumber[1]]
            Node_end=[NodeNumber[2],NodeNumber[3]]
            bearingmesh.ElementMatrix.append(np.column_stack((ElementNumber,Node_start,Node_end)))            
            
            bearingmesh.ElementMatrixName.append('BEARINGPENDULUM' + str(n+1) + '_' + S_or_N[j])
            bearingmesh.ElementType.append('B31')

            # Add springs
            DirectionCell=['X' , 'Y' , 'Z' , 'RX' , 'RY' , 'RZ']
            ElsetBearingDof=[None]*6
            for IndexDof in np.arange(6):

                Nodes=bearing.NodeNumberBase+j*1e3+n*1e2+[2,2+3]
                ElementNumber=bearing.ElementNumberBase+j*1e3+n*1e2+[IndexDof]+10e3;
                ElementNodeMatrix=np.hstack((ElementNumber,Nodes))

                if j==0:
                    k_spring=bearing.stiffness_south[IndexDof]
                elif j==1:
                    k_spring=bearing.stiffness_north[IndexDof]

                ElSetNameTemp='BEARINGSPRING' + str(n+1) + '_' + S_or_N[j] + '_' + DirectionCell[IndexDof]
                gen.Spring(fid,ElSetNameTemp,ElementNodeMatrix,IndexDof+1,k_spring)
                ElsetBearingDof[IndexDof]=ElSetNameTemp

            bearingmesh.ElementSet.append(ElsetBearingDof)
            bearingmesh.ElementSetName.append('BEARINGSPRING' + str(n+1) + '_' + S_or_N[j])
        
    
#%% Sets

    set_cell=['BEARINGTOP1_SOUTH' , 'BEARINGTOP1_NORTH' ]
    if N_bridgedeck==2:
        set_cell=set_cell + ['BEARINGTOP2_SOUTH' , 'BEARINGTOP2_NORTH']
    bearingmesh.ElementSet.append(set_cell)
    bearingmesh.ElementSetName.append('BEARINGTOP')
    
    set_cell=['BEARINGLOW1_SOUTH' , 'BEARINGLOW1_NORTH' ]
    if N_bridgedeck==2:
        set_cell=set_cell + ['BEARINGLOW2_SOUTH' , 'BEARINGLOW2_NORTH']
    bearingmesh.ElementSet.append(set_cell)
    bearingmesh.ElementSetName.append('BEARINGLOW')
    
    set_cell=['BEARINGPENDULUM1_SOUTH' , 'BEARINGPENDULUM1_NORTH' ]
    if N_bridgedeck==2:
        set_cell=set_cell + ['BEARINGPENDULUM2_SOUTH' , 'BEARINGPENDULUM2_NORTH']
    bearingmesh.ElementSet.append(set_cell)
    bearingmesh.ElementSetName.append('BEARINGPENDULUM')
    
    set_cell=['BEARINGSPRING1_SOUTH' , 'BEARINGSPRING1_NORTH' ]
    if N_bridgedeck==2:
        set_cell=set_cell + ['BEARINGSPRING2_SOUTH' , 'BEARINGSPRING2_NORTH']
    bearingmesh.ElementSet.append(set_cell)
    bearingmesh.ElementSetName.append('BEARINGSPRING')
    
    bearingmesh.ElementSet.append(['BEARINGLOW' , 'BEARINGTOP' , 'BEARINGPENDULUM' , 'BEARINGSPRING'])
    bearingmesh.ElementSetName.append('BEARING')
    
#%%  Mesh and sections

    bearingmesh=GenerateMeshStruct(fid,bearingmesh)
    
    gen.BeamGeneralSection(fid,'BEARINGTOP',0,[0.1,1,0,1,1],[1,0,0],[210e9*100,81e9*100])
    gen.BeamGeneralSection(fid,'BEARINGLOW',0,[0.1,1,0,1,1],[1,0,0],[210e9*100,81e9*100])
    
    gen.BeamSection(fid,'BEARINGPENDULUM','STEEL','BOX',[0.2,0.2,0.02,0.02,0.02,0.02],[0,1,0])

    gen.Release(fid,'BEARINGPENDULUM',['S1' , 'S2'],'M1-M2')



#%% 

    return (meta,bearingmesh)