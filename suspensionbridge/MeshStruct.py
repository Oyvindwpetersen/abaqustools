
# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""

#__all__ = ["InitiateMeshStruct", ]


#%% 

from ypstruct import *
import numpy as np
import putools
from .. import gen

#%% 

def InitiateMeshStruct():
    
    mesh_struct=struct()
    
    mesh_struct['NodeMatrix']=[]
    mesh_struct['NodeMatrixName']=[]
    
    mesh_struct['ElementMatrix']=[]
    mesh_struct['ElementMatrixName']=[]
    mesh_struct['ElementType']=[]
    
    mesh_struct['NodeSet']=[]
    mesh_struct['NodeSetName']=[]
    
    mesh_struct['ElementSet']=[]
    mesh_struct['ElementSetName']=[]
    
    mesh_struct['NodeMatrixGenLogic']=[]
    mesh_struct['ElementMatrixGenLogic']=[]
    
    mesh_struct['NodeSetGenLogic']=[]
    mesh_struct['ElementSetGenLogic']=[]
    
    return mesh_struct


#%% 


def GenerateMeshStruct(fid,mesh_struct):

#%% Check

    if len(mesh_struct['NodeMatrix'])!=len(mesh_struct['NodeMatrixName']):
        raise Exception('***** Length of node matrix and name do not match');

    if len(mesh_struct['ElementMatrix'])!=len(mesh_struct['ElementMatrixName']):
        raise Exception('***** Length of ElementMatrix and ElementMatrixName do not match')
    
    if len(mesh_struct['ElementMatrixName'])!=len(mesh_struct['ElementType']):
        print(mesh_struct['ElementMatrixName'])
        print(mesh_struct['ElementType'])
        raise Exception('***** Length of ElementMatrixName and ElementType do not match')

    if len(mesh_struct['NodeSet'])!=len(mesh_struct['NodeSetName']):
        print(mesh_struct['NodeSet'])
        print(mesh_struct['NodeSetName'])
        raise Exception('***** Length of NodeSet and NodeSetName do not match')
    
    if len(mesh_struct['ElementSet'])!=len(mesh_struct['ElementSetName']):
        print(mesh_struct['ElementSet'])
        print(mesh_struct['ElementSetName'])
        raise Exception('***** Length of ElementSet and ElementSetName do not match')
        
#%% Extend logics by false
        
    D=len(mesh_struct['NodeMatrix'])-len(mesh_struct['NodeMatrixGenLogic'])
    if D>0:
        mesh_struct['NodeMatrixGenLogic'] = mesh_struct['NodeMatrixGenLogic'] + [False]*D
        
    D=len(mesh_struct['ElementMatrix'])-len(mesh_struct['ElementMatrixGenLogic'])
    if D>0:
        mesh_struct['ElementMatrixGenLogic'] = mesh_struct['ElementMatrixGenLogic'] + [False]*D
        
    D=len(mesh_struct['NodeSet'])-len(mesh_struct['NodeSetGenLogic'])
    if D>0:
        mesh_struct['NodeSetGenLogic'] = mesh_struct['NodeSetGenLogic'] + [False]*D
        
    D=len(mesh_struct['ElementSet'])-len(mesh_struct['ElementSetGenLogic'])
    if D>0:
        mesh_struct['ElementSetGenLogic'] = mesh_struct['ElementSetGenLogic'] + [False]*D
        
#%% Generate nodes

    for k in np.arange(len(mesh_struct['NodeMatrix'])):
    
        if mesh_struct['NodeMatrixGenLogic'][k]==True:
            continue
        else:
            gen.Node(fid,mesh_struct['NodeMatrix'][k],mesh_struct['NodeMatrixName'][k])
            mesh_struct['NodeMatrixGenLogic'][k]=True


#%% Generate elements

    for k in np.arange(len(mesh_struct['ElementMatrix'])):
    
        if mesh_struct['ElementMatrixGenLogic'][k]==True:
            continue
        else:
            gen.Element(fid,mesh_struct['ElementMatrix'][k],mesh_struct['ElementType'][k],mesh_struct['ElementMatrixName'][k])
            mesh_struct['ElementMatrixGenLogic'][k]=False
      
            
#%% Generate node sets

    for k in np.arange(len(mesh_struct['NodeSet'])):
    
        if mesh_struct['NodeSetGenLogic'][k]==True:
            continue
        else:
            gen.Nset(fid,mesh_struct['NodeSetName'][k],mesh_struct['NodeSet'][k])
            mesh_struct['NodeSetGenLogic'][k]=True        

    
#%% Generate element sets

    for k in np.arange(len(mesh_struct['ElementSet'])):
    
        if mesh_struct['ElementSetGenLogic'][k]==True:
            continue
        else:
            gen.Elset(fid,mesh_struct['ElementSetName'][k],mesh_struct['ElementSet'][k])
            mesh_struct['ElementSetGenLogic'][k]=True   

    
#%% 
    
    return mesh_struct