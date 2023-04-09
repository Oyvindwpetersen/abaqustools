# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""
    
#%%

import numpy as np
import time
import putools
from .. import gen
from .mesh import *

#%% 

def hangergeometry(fid,meta,geo,hanger):

#%% 

    hangermesh=mesh_node_el()

    ##%%  Bridge deck

    elnum_east=hanger.elnum_base[0]+np.arange(1,len(meta.bridgedeck.nodenum_hanger_east)+1)
    elnum_west=hanger.elnum_base[1]+np.arange(1,len(meta.bridgedeck.nodenum_hanger_west)+1)

    hangermesh.addel(np.column_stack((elnum_east,meta.bridgedeck.nodenum_hanger_east,meta.cable.nodenum_hanger_east)),'Hanger_east',hanger.eltype)
    hangermesh.addel(np.column_stack((elnum_west,meta.bridgedeck.nodenum_hanger_west,meta.cable.nodenum_hanger_west)),'Hanger_west',hanger.eltype)

    hangermesh.addelset(['Hanger_east' , 'Hanger_west'],'Hanger')

#%% 

    hangermesh.generate(fid)

    gen.BeamGeneralSection(fid,'Hanger',hanger.cs.rho,[hanger.cs.A,hanger.cs.I11,hanger.cs.I12,hanger.cs.I22,hanger.cs.It],hanger.normaldir,[hanger.cs.E,hanger.cs.G])

    gen.Release(fid,'Hanger',['S1' , 'S2'],'M1-M2')

#%% 

    return (meta,hangermesh)