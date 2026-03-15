
# -*- coding: utf-8 -*-
"""
Created on 

"""

#%%

import numpy as np
import sys
sys.path.append('C:/Cloud/OD_OWP/Work/Python/Github')

from abaqustools import kw
from abaqustools import abq

#%%  Open file

foldername=r'C:\Cloud\OD_OWP\Work\Python\Github\abaqustools\example\frame'
input_filename='frame_structure.inp'
jobname='frame_structure'

fid=open(input_filename,'w')

#%%  Geometry

kw.material(fid,'CONCRETE',10e3*1e6,0.3,2000)

kw.part(fid,'part_frame')


kw.beammember(fid,np.array([0.0,0.0,0.0]),np.array([6.0,0.0,0.0]),'AB','AB',1000,1000,n_el=20)

kw.beammember(fid,np.array([6.0,0.0,0.0]),np.array([6.0,0.0,-6.0]),'BC','BC',2000,2000,n_el=20)


kw.beamsection(fid,'AB','CONCRETE','RECTANGULAR',[0.12,0.12],[0,1,0])

kw.beamsection(fid,'BC','CONCRETE','RECTANGULAR',[0.12,0.12],[0,1,0])

kw.mpc(fid,'TIE',[2001,1021])

kw.nset(fid,'support_A',[1001])
kw.nset(fid,'support_B',[1021])
kw.nset(fid,'support_C',[2021])

#%% 

kw.partend(fid)
    
kw.comment(fid,'ASSEMBLY',True)
    
kw.assembly(fid,'assembly_frame')
    
kw.instance(fid,'part_frame','part_frame')
    
kw.instanceend(fid)
    
kw.assemblyend(fid)


#%%  Step modal analysis

kw.step(fid,'NAME=STEP_MODAL','')
kw.frequency(fid,20,'displacement')

kw.boundary(fid,'new','SUPPORT_A',[1,4,0],'part_frame')

kw.boundary(fid,'new','SUPPORT_B',[2,4,0],'part_frame')

kw.boundary(fid,'new','SUPPORT_C',[1,2,0],'part_frame')

kw.boundary(fid,'new','SUPPORT_C',[4,4,0],'part_frame')

kw.boundary(fid,'new','AB',[2,2,0],'part_frame')
kw.boundary(fid,'new','BC',[2,2,0],'part_frame')
    
kw.fieldoutput(fid,'NODE',['U' , 'COORD'],'','')
kw.fieldoutput(fid,'ELEMENT',['SF'],'','')

kw.stepend(fid)



#%%  Step

kw.step(fid,'NLGEO=NO, NAME=STEP_STATIC','Dead load')

kw.static(fid,'1e-3, 1, 1e-6, 1')

kw.boundary(fid,'new','SUPPORT_A',[1,4,0],'part_frame')

kw.boundary(fid,'new','SUPPORT_B',[2,4,0],'part_frame')

kw.boundary(fid,'new','SUPPORT_C',[1,2,0],'part_frame')

kw.boundary(fid,'new','SUPPORT_C',[4,4,0],'part_frame')

kw.boundary(fid,'new','AB',[2,2,0],'part_frame')
kw.boundary(fid,'new','BC',[2,2,0],'part_frame')
    

# %%
kw.dload(fid,'NEW','part_frame.BC','PX',-7000/1e6)


kw.fieldoutput(fid,'NODE',['U' , 'RF' , 'COORD'],'','FREQUENCY=100')
kw.fieldoutput(fid,'ELEMENT',['SF'],'','FREQUENCY=100')
    
kw.stepend(fid)

#%%

kw.line(fid,'*Step, name=BUCKLING, perturbation')
kw.line(fid,'*Buckle, eigensolver=Lanczos')
kw.line(fid,'10')


kw.dload(fid,'NEW','part_frame.BC','PX',-7000)

kw.fieldoutput(fid,'NODE',['U' , 'RF' , 'COORD'],'','FREQUENCY=100')
kw.fieldoutput(fid,'ELEMENT',['SF'],'','FREQUENCY=100')
    

kw.line(fid,'*End Step')



#%%  Close file

fid.close()

#%%  Run job
    
# Check input file for duplicate node or element numbers
abq.checkduplicate(input_filename)
    
abq.runjob(foldername,input_filename,jobname)



