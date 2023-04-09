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


def sadlegeometry(fid,meta,geo,sadle):
    
#%% 
    
    sadlemesh=mesh_node_el()

#%% 
    
    dir_xyz=['X' , 'Y' , 'Z']
    
    DOF=[1,2,3]
    
    for idx_dof in np.arange(len(DOF)):
        
        el_node_matrix=np.zeros((4,3))
        for k in np.arange(4):
            
            el_node_matrix[k,0]=sadle.elnum_base+idx_dof*1e3+k
            el_node_matrix[k,1]=meta.tower.nodenum_top[k]
            el_node_matrix[k,2]=meta.cable.nodenum_top[k]
     

        gen.Spring(fid,'SADLESPRING_' + dir_xyz[idx_dof],el_node_matrix,DOF[idx_dof],sadle.stiffness)
    
    
    gen.Elset(fid,'SADLESPRING',['SADLESPRING_X' , 'SADLESPRING_Y' , 'SADLESPRING_Z'])
    
    
#%% 

    return (meta,sadlemesh)