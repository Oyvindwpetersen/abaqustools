
# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""

#__all__ = ["InitiateMeshStruct", ]


#%% 

#from ypstruct import *
import numpy as np
import putools
from .. import gen

#%% 

class mesh_node_el:

    def __init__(self):
    
        self.node_matrix=[]
        self.node_matrix_name=[]
        self.node_matrix_isgen=[]
        
        self.el_matrix=[]
        self.el_matrix_name=[]
        self.el_matrix_type=[]
        self.el_matrix_isgen=[]
        
        self.node_set=[]
        self.node_set_name=[]
        self.node_set_isgen=[]
        
        self.el_set=[]
        self.el_set_name=[]
        self.el_set_isgen=[]

    def addnode(self,matrix,name):
        
        #if np.shape(matrix,1) != 4:
            #error
            
        self.node_matrix.append(matrix)
        self.node_matrix_name.append(name)
        self.node_matrix_isgen.append(False)
    
    def addel(self,matrix,name,eltype):
 
        self.el_matrix.append(matrix)
        self.el_matrix_name.append(name)
        self.el_matrix_type.append(eltype)
        self.el_matrix_isgen.append(False)
    
    def addnset(self,nset,name):
 
        self.node_set.append(nset)
        self.node_set_name.append(name)
        self.node_set_isgen.append(False)
    
    
    def addelset(self,elset,name):
        
        self.el_set.append(elset)
        self.el_set_name.append(name)
        self.el_set_isgen.append(False)
        
    def generate(self,fid):
    
        # Nodes
        for k in np.arange(len(self.node_matrix)):
        
            if self.node_matrix_isgen[k]==False:             
                gen.Node(fid,self.node_matrix[k],self.node_matrix_name[k])
                self.node_matrix_isgen[k]=True
        
        # Elements
        for k in np.arange(len(self.el_matrix)):
        
            if self.el_matrix_isgen[k]==False:
                print(self.el_matrix_name[k])
                gen.Element(fid,self.el_matrix[k],self.el_matrix_type[k],self.el_matrix_name[k])
                self.el_matrix_isgen[k]=True
        
        # Node sets
        for k in np.arange(len(self.node_set)):
        
            if self.node_set_isgen[k]==False:
                gen.Nset(fid,self.node_set_name[k],self.node_set[k])
                self.node_set_isgen[k]=True
        
        # Element sets            
        for k in np.arange(len(self.el_set)):
        
            if self.el_set_isgen[k]==False:
                gen.Elset(fid,self.el_set_name[k],self.el_set[k])
                self.el_set_isgen[k]=True 
            

