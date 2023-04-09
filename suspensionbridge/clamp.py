# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""
    
#%%

import numpy as np
import putools
from .. import gen
from .mesh import *

#%%

def clampgeometry(fid,meta,cable):
   
    clampmesh=mesh_node_el()
    
#%% Mesh size of size spans

    N_hanger=len(meta.bridgedeck.nodenum_hanger_east)
    
    idx_mid=int((N_hanger+1)/2)
    
    E_or_W=['EAST' , 'WEST']
    
    nset_temp=np.array([])
    
    for j in [0,1]:
    
        if j==0:
            nodenum_bridgedeck=meta.bridgedeck.nodenum_hanger_east
            nodenum_cable=meta.cable.nodenum_hanger_east
        elif j==1:
            nodenum_bridgedeck=meta.bridgedeck.nodenum_hanger_west
            nodenum_cable=meta.cable.nodenum_hanger_west
    
        elnum_cable_clamp=3e6+j*1e3+np.arange(1,2+1).astype('int')
            
        el_node_matrix_temp=np.array( [    
                        [elnum_cable_clamp[0] , nodenum_cable[idx_mid] , nodenum_bridgedeck[idx_mid-1] ],
                        [elnum_cable_clamp[1] , nodenum_cable[idx_mid] , nodenum_bridgedeck[idx_mid+1] ],
                        ])
        
        nset_temp=np.append(nset_temp,nodenum_cable[[idx_mid]])                
                        
        if cable.N_clamp>=3:
            elnum_cable_clamp=elnum_cable_clamp[-1]+np.arange(1,4+1).astype('int')
            el_node_matrix_temp3=np.array( [    
                            [elnum_cable_clamp[0] , nodenum_cable[idx_mid-2] , nodenum_bridgedeck[idx_mid-3] ],
                            [elnum_cable_clamp[1] , nodenum_cable[idx_mid-2] , nodenum_bridgedeck[idx_mid-1] ],
                            [elnum_cable_clamp[2] , nodenum_cable[idx_mid+2] , nodenum_bridgedeck[idx_mid+1] ],
                            [elnum_cable_clamp[3] , nodenum_cable[idx_mid+2] , nodenum_bridgedeck[idx_mid+3] ],
                            ])
                                    
            el_node_matrix_temp=np.vstack((el_node_matrix_temp,el_node_matrix_temp3))
            nset_temp=np.append(nset_temp,nodenum_cable[[idx_mid-2,idx_mid+2]])
        
        if cable.N_clamp>=5:
            elnum_cable_clamp=elnum_cable_clamp[-1]+np.arange(1,4+1).astype('int')
            el_node_matrix_temp5=np.array( [    
                            [elnum_cable_clamp[0] , nodenum_cable[idx_mid-4] , nodenum_bridgedeck[idx_mid-5] ],
                            [elnum_cable_clamp[1] , nodenum_cable[idx_mid-4] , nodenum_bridgedeck[idx_mid-3] ],
                            [elnum_cable_clamp[2] , nodenum_cable[idx_mid+4] , nodenum_bridgedeck[idx_mid+3] ],
                            [elnum_cable_clamp[3] , nodenum_cable[idx_mid+4] , nodenum_bridgedeck[idx_mid+5] ],
                            ])
                                    
            el_node_matrix_temp=np.vstack((el_node_matrix_temp,el_node_matrix_temp5))
            nset_temp=np.append(nset_temp,nodenum_cable[[idx_mid-4,idx_mid+4]])
            
        clampmesh.addel(el_node_matrix_temp,'CABLE_CLAMP' + '_' + E_or_W[j],'B31')

    clampmesh.addelset(['CABLE_CLAMP_EAST' , 'CABLE_CLAMP_WEST' ],'CABLE_CLAMP')
    clampmesh.addnset(nset_temp,'CABLE_CLAMP_TEMPERATURE')
    
#%% Section

    clampmesh.generate(fid)
    
    gen.BeamGeneralSection(fid,'CABLE_CLAMP',7850,[4e-3 , 1e-7 , 0 , 1e-7 , 1e-7],[0, 1, 0],[210e9,81e9,1e-5])
    
        
#%% 

    return (meta,clampmesh)
