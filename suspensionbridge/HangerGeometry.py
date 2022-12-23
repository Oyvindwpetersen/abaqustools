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
from .MeshStruct import *

#%% 

def HangerGeometry(fid,meta,geo,hanger):

#%% 

    hangermesh=InitiateMeshStruct()

    ##%%  Bridge deck

    ElementNumberHangerEast=hanger.ElementNumberBase[0]+np.arange(1,len(meta.bridgedeck.NodeNumberEastHanger)+1)
    hangermesh.ElementMatrix.append(np.column_stack((ElementNumberHangerEast,meta.bridgedeck.NodeNumberEastHanger,meta.cable.NodeNumberEastHanger)))
    hangermesh.ElementMatrixName.append('Hanger_east')
    hangermesh.ElementType.append(hanger.eltype)

    ElementNumberHangerWest=hanger.ElementNumberBase[1]+np.arange(1,len(meta.bridgedeck.NodeNumberWestHanger)+1)
    hangermesh.ElementMatrix.append(np.column_stack((ElementNumberHangerWest,meta.bridgedeck.NodeNumberWestHanger,meta.cable.NodeNumberWestHanger)))
    hangermesh.ElementMatrixName.append('Hanger_west')
    hangermesh.ElementType.append(hanger.eltype)

    hangermesh.ElementSet.append(['Hanger_east' , 'Hanger_west'])
    hangermesh.ElementSetName.append('Hanger')

#%% 

    hangermesh=GenerateMeshStruct(fid,hangermesh)

    gen.BeamGeneralSection(fid,'Hanger',hanger.cs.rho,[hanger.cs.A,hanger.cs.I11,hanger.cs.I12,hanger.cs.I22,hanger.cs.It],hanger.normaldir,[hanger.cs.E,hanger.cs.G])

    gen.Release(fid,'Hanger',['S1' , 'S2'],'M1-M2')

#%% 

    return (meta,hangermesh)