
# -*- coding: utf-8 -*-
"""
Created on 

"""

#%%

import numpy as np
import sys
sys.path.append('C:/Cloud/OD_OWP/Work/Python/Github')

from abaqustools import gen
from abaqustools import abq

#%%  Open file

foldername=r'C:\Cloud\OD_OWP\Work\Python\Github\abaqustools\example\truss'
input_filename='simple_truss.inp'
jobname='simple_truss'

fid=open(input_filename,'w')

#%%  Geometry

gen.part(fid,'part_truss')

# Lower nodes
x1=np.array([0,5,10,15,20])
y1=x1*0
z1=x1*0

nodenumber1=np.arange(1,len(x1)+1)

gen.node(fid,np.column_stack((nodenumber1,x1,y1,z1)),'NODES_BOTTOM')

# Upper nodes
x2=np.array([2.5,7.5,12.5,17.5])
y2=x2*0
z2=5*np.ones(np.shape(x2))

nodenumber2=np.arange(1,len(x2)+1)+10

gen.node(fid,np.column_stack((nodenumber2,x2,y2,z2)),'NODES_TOP')

# Elements and nodes
nodes_el=np.array([
    [100,1,2],
    [101,2,3],
    [102,3,4],
    [103,4,5],
    [201,11,12],
    [202,12,13],
    [203,13,14],
    [301,1,11],
    [302,11,2],
    [303,2,12],
    [304,12,3],
    [305,3,13],
    [306,13,4],
    [307,4,14],
    [308,14,5],
])

gen.element(fid,nodes_el,'B31','Truss_elements')

gen.beamgeneralsection(fid, 'Truss_elements', 7850, [1e-4,1e-6,0,1e-6,1e-6], [0,1,0], [210e9,81e9])

gen.release(fid, [301,302,303,304,305,306,307,308], ['S1','S2'], ['M1','M2'])

gen.nset(fid,'support',[1,5])

#%% 

gen.partend(fid)
    
gen.comment(fid,'ASSEMBLY',True)
    
gen.assembly(fid,'assembly_truss')
    
gen.instance(fid,'part_truss','part_truss')
    
gen.instanceend(fid)
    
gen.assemblyend(fid)
    
#%%  Step static

gen.step(fid,'NLGEO=NO, NAME=STEP_STATIC','Dead load')

gen.static(fid,'1e-3, 1, 1e-6, 1')

gen.gravload(fid,'new',[''],9.81)
    
gen.boundary(fid,'new','support',[1,6,0],'part_truss')

gen.boundary(fid,'new','NODES_BOTTOM',[2,2,0],'part_truss')
gen.boundary(fid,'new','NODES_TOP',[2,2,0],'part_truss')


gen.fieldoutput(fid,'NODE',['U' , 'RF' , 'COORD'],'','FREQUENCY=100')
gen.fieldoutput(fid,'ELEMENT',['SF'],'','FREQUENCY=100')
    
gen.stepend(fid)

#%%  Step modal analysis

gen.step(fid,'NAME=STEP_MODAL','')
gen.frequency(fid,50,'displacement')
    
gen.fieldoutput(fid,'NODE',['U' , 'COORD'],'','')
gen.fieldoutput(fid,'ELEMENT',['SF'],'','')

gen.stepend(fid)

#%%  Close file

fid.close()

#%%  Run job
    
# Check input file for duplicate node or element numbers
abq.checkduplicate(input_filename)
    
abq.runjob(foldername,input_filename,jobname)



