
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
from .. import abq

from .bearing import *
from .bridgedeck import *
from .cable import *
from .clamp import *
from .EstimateCableDeflection import *
from .generateintro import *
from .hanger import *
from .model import *
from .mesh import *
from .processpar import *
from .retract import *
from .sadle import *
from .tower import *

#%%

def buildinput(UserParameterFileName,UserParameterFolder,IterateDeflection=False,UpdateGeometry=False):

#%%  User parameters

    UserParameterFile=UserParameterFolder + '\\' + UserParameterFileName

    (abaqus,bearing,bridgedeck,cable,geo,hanger,modal,sadle,step,tower)=processpar(UserParameterFile)

#%%  Generate some structures

    meta=struct()
    meta.bridgedeck=struct()
    meta.cable=struct()
    meta.bearing=struct()
    meta.crossbeamlow=struct()
    meta.tower=struct()
    
#%%  Estimate pullback force

    if np.isnan(tower.F_pullback_south) and np.isnan(tower.F_pullback_north):
        
        putools.txt.starprint(['Estimating force for retraction of towers'],1)
        (tower.F_pullback_south,tower.F_pullback_north,tower.K_south,tower.K_north,tower.K_est)=estimatepullbackforce(tower,geo,abaqus)

#%%  Estimate cable deflection

    if IterateDeflection==True:
        
        putools.txt.starprint(['Estimating cable deflection'],1)
                
        (cable,geo)=EstimateCableDeflectionMain(meta,cable,bridgedeck,tower,geo)
                
        if 'K_south' in tower.fields():
            tower.F_pullback_south=tower.K_south*geo.dx_pullback_south
            
        if 'K_north' in tower.fields():
            tower.F_pullback_north=tower.K_north*geo.dx_pullback_north
            
#%%  Open file

    InputFileName=abaqus.foldername + '\\' + abaqus.inputname + '.inp'
    
    fid=open(InputFileName,'w')
    
    generateintro(fid,abaqus,bearing,bridgedeck,cable,geo,hanger,modal,sadle,step,tower,time)

#%%  Materials
    gen.Comment(fid,'MATERIALS',True)
    
    gen.Material(fid,'CONCRETE',tower.cs.E,tower.cs.v,tower.cs.rho)
    gen.Material(fid,'SOFT',1e-6,0.3,1e-12)
    gen.Material(fid,'STEEL',210e9,0.3,7850)

#%%  Part
    
    gen.Part(fid,abaqus.partname)

#%%  Cable Main

    gen.Comment(fid,'CABLE',True)

    (meta,cablemesh)=cablegeometry(fid,meta,geo,cable)
    
#%%  Tower
    
    gen.Comment(fid,'TOWER',True)
    
    (meta,towermesh)=towergeometry(fid,meta,geo,tower)
    
#%%  Sadle springs
    
    gen.Comment(fid,'SADLE',True)
    
    (meta,sadlemesh)=sadlegeometry(fid,meta,geo,sadle)
    
#%%  Bridge deck
    
    gen.Comment(fid,'BRIDGE DECK',True)
    
    (meta,bridgemesh)=bridgedeckgeometry(fid,meta,geo,bridgedeck)
    
#%%  Hanger
    
    gen.Comment(fid,'HANGER',True)
    
    (meta,hangermesh)=hangergeometry(fid,meta,geo,hanger)
    
#%%  Bearings
    
    gen.Comment(fid,'BEARINGS',True)
    
    (meta,bearingmesh)=bearinggeometry(fid,meta,geo,bearing)
    
#%%  Cable clamp
    
    if cable.clamp==True:
        
        gen.Comment(fid,'CABLE CLAMP',True)
        
        (meta,clampmesh)=clampgeometry(fid,meta,cable)
    
#%%  Part, instance, assembly
    
    gen.PartEnd(fid)
    
    gen.Comment(fid,'ASSEMBLY',True)
    
    gen.Assembly(fid,abaqus.assemblyname)
    
    gen.Instance(fid,abaqus.partname,abaqus.partname)
    
    gen.InstanceEnd(fid)
    
    gen.AssemblyEnd(fid)
    
#%%  Step

    gen.Step(fid,'NLGEO=YES, NAME=STEP1','Towers, retraction')
    
    if np.isnan(step.time[0]).any():
        Time_step='1e-3, 1, 1e-6, 1'
    else:
        Time_step=step.time[0]

    gen.Static(fid,Time_step)
    
    gen.ModelChange(fid,'REMOVE',['CABLE_MAIN' , 'SADLESPRING' , 'BRIDGEDECK' , 'HANGER' , 'BEARINGTOP' , 'BEARINGPENDULUM' , 'BEARINGSPRING'],abaqus.partname)
    
    if cable.tempsupport==True:
        gen.ModelChange(fid,'REMOVE',['CABLE_TEMPSUPPORT'],abaqus.partname)
    
    if bridgedeck.shell==True:
        gen.ModelChange(fid,'REMOVE',['Bridgedeck_shell'],abaqus.partname)
    
    if cable.clamp==True:
        gen.ModelChange(fid,'REMOVE',['Cable_clamp'],abaqus.partname)    

    gen.Cload(fid,'NEW',['Tower_top_south_east','Tower_top_south_west'],1,tower.F_pullback_south,abaqus.partname)
    gen.Cload(fid,'NEW',['Tower_top_north_east','Tower_top_north_west'],1,tower.F_pullback_north,abaqus.partname)
    
    gen.Gravload(fid,'new',[''],9.81)
    
    gen.Boundary(fid,'new','Tower_base',[1,6,0],abaqus.partname)

    gen.FieldOutput(fid,'NODE',['U' , 'RF' , 'COORD'],'','FREQUENCY=100')
    gen.FieldOutput(fid,'ELEMENT',['SF'],'','FREQUENCY=100')
    
    gen.StepEnd(fid)

#%%  Step

    gen.Step(fid,'NLGEO=YES, NAME=STEP2','Add main cable, release retraction')

    if np.isnan(step.time[1]).any():
        Time_step='1e-8, 1, 1e-12, 1'
    else:
        Time_step=step.time[1]
            
    gen.Static(fid,Time_step)
    
    gen.ModelChange(fid,'ADD',['CABLE_MAIN' , 'SADLESPRING'],abaqus.partname)
    
    if cable.tempsupport==True:
        gen.ModelChange(fid,'ADD',['CABLE_TEMPSUPPORT'],abaqus.partname)
        
    gen.Cload(fid,'NEW',[],[],[])
    
    gen.Gravload(fid,'new',[''],9.81)
    
    gen.Boundary(fid,'new','Tower_base',[1,6,0],abaqus.partname)
    gen.Boundary(fid,'new','Cable_main_anchorage',[1,4,0],abaqus.partname)
    
    gen.FieldOutput(fid,'NODE',['U' , 'RF' , 'COORD'],'','FREQUENCY=100')
    gen.FieldOutput(fid,'ELEMENT',['SF' , 'S'],'','FREQUENCY=100')
    
    gen.StepEnd(fid)


#%%  Step

    gen.Step(fid,'NLGEO=YES, NAME=STEP3','Add hangers and bridge deck, remove main cable temp supports')

    if np.isnan(step.time[2]).any():
        Time_step='1e-3, 1, 1e-9, 1'
    else:
        Time_step=step.time[2]
    
    gen.Static(fid,Time_step)
    
    gen.ModelChange(fid,'ADD',['BRIDGEDECK' , 'HANGER' , 'BEARINGTOP'],abaqus.partname)
    
    if cable.tempsupport==True:
        gen.ModelChange(fid,'REMOVE',['CABLE_TEMPSUPPORT'],abaqus.partname)
       
    
    GravList=['TOWER','CABLE_MAIN','HANGER','BRIDGEDECK','BEARINGTOP','BEARINGLOW']
    gen.Gravload(fid,'NEW',GravList,9.81,abaqus.partname)  
    
    gen.FieldOutput(fid,'NODE',['U' , 'RF' , 'COORD'],'','FREQUENCY=100')
    gen.FieldOutput(fid,'ELEMENT',['SF' , 'S'],'','FREQUENCY=100')
    
    gen.StepEnd(fid)

#%%  Step

    gen.Step(fid,'NLGEO=YES, NAME=STEP4','Add bearings at bridge deck ends')
    
    if np.isnan(step.time[3]).any():
        Time_step='1e-3, 1, 1e-9, 1'
    else:
        Time_step=step.time[3]
    
    gen.Static(fid,Time_step)
    gen.ModelChange(fid,'ADD',['BEARINGPENDULUM' , 'BEARINGSPRING'],abaqus.partname)
    
    if bridgedeck.shell==True:
        gen.ModelChange(fid,'ADD',['Bridgedeck_shell'],abaqus.partname)

    if cable.clamp==True:
        gen.ModelChange(fid,'ADD',['CABLE_CLAMP'],abaqus.partname)
        
        #eps=alpha*dT
        #sigma=E*eps=E*alpha*dT
        #F=A*sigma=A*E*alpha*dT
        
        temp_magnitude=-cable.F_clamp/(210e9*4e-3*1e-5)*2
        gen.Temp(fid,'MOD',['CABLE_CLAMP_TEMPERATURE'],temp_magnitude,abaqus.partname)
        
    gen.FieldOutput(fid,'NODE',['U' , 'RF' , 'COORD'],'','FREQUENCY=100')
    gen.FieldOutput(fid,'ELEMENT',['SF' , 'S'],'','FREQUENCY=100')
    
    gen.StepEnd(fid)

#%%  Step

    gen.Step(fid,'NAME=STEP_MODAL','')
    gen.Frequency(fid,modal.N_modes,modal.normalization)
    
    gen.FieldOutput(fid,'NODE',['U' , 'COORD'],'','')
    gen.FieldOutput(fid,'ELEMENT',['SF'],'','')
    
    if abaqus.restart==True:
        gen.Restart(fid,'WRITE')
    
    gen.StepEnd(fid)

#%%  Close file

    fid.close()

#%%  Run job
    
    # Check input file for duplicate node or element numbers
    abq.checkduplicate(InputFileName)
    
    LogicCompleted=False
    # Run
    if abaqus.runjob==True:
        LogicCompleted=abq.runjob(abaqus.foldername,abaqus.inputname,abaqus.jobname,abaqus.cmd,abaqus.cpus,True,True)

    return LogicCompleted




