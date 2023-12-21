
# -*- coding: utf-8 -*-
"""
Created on 

"""
# Example truss model where diagonals are modelled with variable (used-defined)
# stiffness in joint connections

#%%

import numpy as np
import sys
sys.path.append('C:/Cloud/OD_OWP/Work/Python/Github')

from abaqustools import kw
from abaqustools import abq

#%%  Open input file

foldername=r'C:\Cloud\OD_OWP\Work\Python\Github\abaqustools\example\trussjointc'
input_filename='simple_trussjointc.inp'
jobname='simple_trussjointc'

fid=open(input_filename,'w')

#%%  Define structure

kw.part(fid,'part_truss')

# Lower chord nodes
x1=np.array([0,6,10,14,20])
y1=x1*0
z1=x1*0
nodenumber1=np.arange(1,len(x1)+1)
node_matrix_bottom=np.column_stack((nodenumber1,x1,y1,z1))

# Upper chord nodes
x2=np.array([2,7.5,12.5,18])
y2=x2*0
z2=5*np.ones(np.shape(x2))
nodenumber2=np.arange(1,len(x2)+1)+10
node_matrix_top=np.column_stack((nodenumber2,x2,y2,z2))

node_matrix=np.vstack((node_matrix_bottom,node_matrix_top))
kw.node(fid,node_matrix,'NODES_CHORD')


# Elements and nodes for chord
nodes_el_chord=np.array([
    [100,1,2],
    [101,2,3],
    [102,3,4],
    [103,4,5],
    [201,11,12],
    [202,12,13],
    [203,13,14]
])

kw.element(fid,nodes_el_chord,'B31','Truss_chord')
kw.beamgeneralsection(fid,'Truss_chord', 7850, [1e-4,1e-6,0,1e-6,1e-6], [0,1,0], [210e9,81e9])

# Diagonals
nodes_el_dia=np.array([
    [301,1,11],
    [302,11,2],
    [303,2,12],
    [304,12,3],
    [305,3,13],
    [306,13,4],
    [307,4,14],
    [308,14,5]
])


for k in np.arange(0,8):
    
    node1=nodes_el_dia[k,1]
    node2=nodes_el_dia[k,2]
    
    idx1=np.where(node_matrix[:,0]==node1)[0][0]
    coord1=node_matrix[idx1,1:]
    
    idx2=np.where(node_matrix[:,0]==node2)[0][0]
    coord2=node_matrix[idx2,1:]
    
    setname='Dia' + str(k+1)
    
    # Stiffness for x,y,z,rx,ry,rz (local system)
    kj1=[1e12,1e12,1e12,1e10,1e10,1e10]
    kj2=[1e10,1e10,1e10,0,0,0]
    #kj2=[1e99,1e99,1e99,1e99,1e99,1e99]
       
    
    kw.elementjointc(fid, node1, node2, coord1 , coord2 , 1000+k*100, 1000+k*100,'B31',setname, [0,1,0],kj1,kj2,offset1=0.1,offset2=0.1,max_length=0.2) #

    kw.beamgeneralsection(fid, setname, 7850, [1e-5,1e-7,0,1e-7,1e-7], [0,1,0], [210e9,81e9])


kw.nset(fid,'support',[1,5])

#%% 

kw.partend(fid)

kw.comment(fid,'ASSEMBLY',True)
    
kw.assembly(fid,'as_truss')
    
kw.instance(fid,'part_truss','part_truss')
    
kw.instanceend(fid)
    
kw.assemblyend(fid)
    
#%%  Step static

# kw.step(fid,'NLGEO=NO, NAME=STEP_STATIC','Dead load')

# kw.static(fid,'1e-3, 1, 1e-6, 1')

# kw.gravload(fid,'new',[''],9.81)
    
# kw.boundary(fid,'new','support',[1,6,0],'part_truss')

# kw.boundary(fid,'new','NODES_BOTTOM',[2,2,0],'part_truss')
# kw.boundary(fid,'new','NODES_TOP',[2,2,0],'part_truss')


# kw.fieldoutput(fid,'NODE',['U' , 'RF' , 'COORD'],'','FREQUENCY=100')
# kw.fieldoutput(fid,'ELEMENT',['SF'],'','FREQUENCY=100')
    
# kw.stepend(fid)

#%%  Step modal analysis

kw.step(fid,'NAME=STEP_MODAL','')
kw.frequency(fid,50,'displacement')

kw.boundary(fid,'new','support',[1,6,0],'part_truss')

kw.boundary(fid,'new','NODES_CHORD',[2,2,0],'part_truss')
    
kw.fieldoutput(fid,'NODE',['U' , 'COORD'],'','')
kw.fieldoutput(fid,'ELEMENT',['SF','S'],'','')

kw.stepend(fid)

#%%  Close file

fid.close()

#%%  Run job
    
# Check input file for duplicate node or element numbers
abq.checkduplicate(input_filename)
    
abq.runjob(foldername,input_filename,jobname)



