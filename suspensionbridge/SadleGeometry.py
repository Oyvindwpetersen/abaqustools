# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""
    
#%%

import numpy as np
import putools
from .. import gen
from . MeshStruct import *


def SadleGeometry(fid,meta,geo,sadle):
    
#%% 
    
    sadlemesh=InitiateMeshStruct()

#%% 
    
    Direction_xyz=['X' , 'Y' , 'Z']
    
    DOF=[1,2,3]
    
    for IndexDof in np.arange(len(DOF)):
        
        MatrixElNode=np.zeros((4,3))
        for k in np.arange(4):
            
            MatrixElNode[k,0]=sadle.ElementNumberBase+IndexDof*1e3+k
            MatrixElNode[k,1]=meta.tower.NodeNumberTop[k]
            MatrixElNode[k,2]=meta.cable.NodeNumberTop[k]
     

        gen.Spring(fid,'SADLESPRING_' + Direction_xyz[IndexDof],MatrixElNode,DOF[IndexDof],sadle.stiffness)
    
    
    gen.Elset(fid,'SADLESPRING',['SADLESPRING_X' , 'SADLESPRING_Y' , 'SADLESPRING_Z'])
    
    
#%% 

    return (meta,sadlemesh)