
# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""

#%%

import numpy as np
import time

from .. import numtools
from .. import gen
from .. import abq

from .MeshStruct import *
from .ProcessUserParameters import *
from .GenerateIntro import *
from .CableGeometry import *
from .TowerGeometry import *
from .SadleGeometry import *
from .BridgeDeckGeometry import *
from .HangerGeometry import *
from .BearingGeometry import *
from .ElementNormal import *
from .EstimateCableDeflection import *
from .EstimatePullbackForce import *

#%%

def MainSuspensionBridge(UserParameterFileName,UserParameterFolder,IterateDeflection=False,UpdateGeometry=False):

#%%  User parameters

    UserParameterFile=UserParameterFolder + '\\' + UserParameterFileName

    (abaqus,bearing,bridgedeck,cable,geo,hanger,modal,sadle,step,tower)=ProcessUserParameters(UserParameterFile)

#%%  Generate some structures

    meta=struct()
    meta.bridgedeck=struct()
    meta.cable=struct()
    meta.bearing=struct()
    meta.crossbeamlow=struct()
    meta.tower=struct()
    
#%%  Estimate pullback force

    if np.isnan(tower.F_pullback_south) and np.isnan(tower.F_pullback_north):
        
        # dummy=np.nan
        numtools.starprint(['Estimating force for retraction of towers'],1)
        (tower.F_pullback_south,tower.F_pullback_north,tower.K_south,tower.K_north,tower.K_est)=EstimatePullbackForce(tower,geo,abaqus)

#%%  Estimate cable deflection

    if IterateDeflection==True:
        
        numtools.starprint(['Estimating cable deflection'],1)
                
        (cable,geo)=EstimateCableDeflectionMain(meta,cable,bridgedeck,tower,geo)
                
        if 'K_south' in tower.fields():
            tower.F_pullback_south=tower.K_south*geo.dx_pullback_south
            
        if 'K_north' in tower.fields():
            tower.F_pullback_north=tower.K_north*geo.dx_pullback_north
            
#%%  Open file

    InputFileName=abaqus.FolderNameModel + '/' + abaqus.InputName + '.inp'
    
    fid=open(InputFileName,'w')
    
    GenerateIntro(fid,abaqus,bearing,bridgedeck,cable,geo,hanger,modal,sadle,step,tower,time)

#%%  Materials
    gen.Comment(fid,'MATERIALS',True)
    
    gen.Material(fid,'CONCRETE',tower.cs.E,tower.cs.v,tower.cs.rho)
    gen.Material(fid,'SOFT',1e-6,0.3,1e-12)
    gen.Material(fid,'STEEL',210e9,0.3,7850)

#%%  Part
    
    gen.Part(fid,abaqus.PartName)

#%%  Cable Main

    gen.Comment(fid,'CABLE',True)

    (meta,cablemesh)=CableGeometry(fid,meta,geo,cable)
    
#%%  Tower
    
    gen.Comment(fid,'TOWER',True)
    
    (meta,towermesh)=TowerGeometry(fid,meta,geo,tower)
    
#%%  Sadle springs
    
    gen.Comment(fid,'SADLE',True)
    
    (meta,sadlemesh)=SadleGeometry(fid,meta,geo,sadle)
    
#%%  Bridge deck
    
    gen.Comment(fid,'BRIDGE DECK',True)
    
    (meta,bridgemesh)=BridgeDeckGeometry(fid,meta,geo,bridgedeck)
    
#%%  Hanger
    
    gen.Comment(fid,'HANGER',True)
    
    (meta,hangermesh)=HangerGeometry(fid,meta,geo,hanger)
    
#%%  Bearings
    
    gen.Comment(fid,'BEARINGS',True)
    
    (meta,bearingmesh)=BearingGeometry(fid,meta,geo,bearing)
    
#%%  Part, instance, assembly
    
    gen.PartEnd(fid)
    
    gen.Comment(fid,'ASSEMBLY',True)
    
    gen.Assembly(fid,abaqus.AssemblyName)
    
    gen.Instance(fid,abaqus.PartName,abaqus.PartName)
    
    gen.InstanceEnd(fid)
    
    gen.AssemblyEnd(fid)
    
#%%  Step

    gen.Step(fid,'NLGEO=YES, NAME=STEP1','Towers, retraction')
    
    if np.isnan(step.time[0]).any():
        Time_step='1e-3, 1, 1e-6, 1'
    else:
        Time_step=step.time[0]

    gen.Static(fid,Time_step)
    
    gen.ModelChange(fid,'REMOVE',['CABLE_MAIN' , 'SADLESPRING' , 'BRIDGEDECK' , 'HANGER' , 'BEARINGTOP' , 'BEARINGPENDULUM' , 'BEARINGSPRING'],abaqus.PartName)
    
    if cable.tempsupport==True:
        gen.ModelChange(fid,'REMOVE',['CABLE_TEMPSUPPORT'],abaqus.PartName)
    
    if bridgedeck.shell==True:
        gen.ModelChange(fid,'REMOVE',['Bridgedeck_shell'],abaqus.PartName)
    

    gen.Cload(fid,'NEW',['Tower_top_south_east','Tower_top_south_west'],1,tower.F_pullback_south,abaqus.PartName)
    gen.Cload(fid,'NEW',['Tower_top_north_east','Tower_top_north_west'],1,tower.F_pullback_north,abaqus.PartName)
    
    gen.Gravload(fid,'new',[''],9.81)
    
    gen.Boundary(fid,'new','Tower_base',[1,6,0],abaqus.PartName)

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
    
    gen.ModelChange(fid,'ADD',['CABLE_MAIN' , 'SADLESPRING'],abaqus.PartName)
    
    if cable.tempsupport==True:
        gen.ModelChange(fid,'ADD',['CABLE_TEMPSUPPORT'],abaqus.PartName)
    
    gen.Cload(fid,'NEW',[],[],[])
    
    gen.Gravload(fid,'new',[''],9.81)
    
    gen.Boundary(fid,'new','Tower_base',[1,6,0],abaqus.PartName)
    gen.Boundary(fid,'new','Cable_main_anchorage',[1,4,0],abaqus.PartName)
    
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
    
    gen.ModelChange(fid,'ADD',['BRIDGEDECK' , 'HANGER' , 'BEARINGTOP'],abaqus.PartName)
    
    if cable.tempsupport==True:
        gen.ModelChange(fid,'REMOVE',['CABLE_TEMPSUPPORT'],abaqus.PartName)
    
    GravList=['TOWER','CABLE_MAIN','HANGER','BRIDGEDECK','BEARINGTOP','BEARINGLOW']
    gen.Gravload(fid,'NEW',GravList,9.81,abaqus.PartName)  
    
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
    gen.ModelChange(fid,'ADD',['BEARINGPENDULUM' , 'BEARINGSPRING'],abaqus.PartName)
    
    if bridgedeck.shell==True:
        gen.ModelChange(fid,'ADD',['Bridgedeck_shell'],abaqus.PartName)
    
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
    abq.CheckDuplicateNumbers(InputFileName)
    
    LogicCompleted=False
    # Run
    if abaqus.RunJob==True:
        LogicCompleted=abq.RunJob(abaqus.cmd,abaqus.FolderNameModel,abaqus.InputName,abaqus.JobName,abaqus.cpus,True,True)

    return LogicCompleted

#%%  Contination, update geometry


# =============================================================================
# if UpdateGeometry==False
# 
# numtools.starprint(['Automatic continuation to update geometry' ],1)
# 
# # Copy file with user parameters
# UserParameterFileNameAuto=[UserParameterFileName(1:end-2) '_postupdgeo' , '.m']
# copyfile(UserParameterFileName,UserParameterFileNameAuto)
# 
# # Open
# user_data_cell=inpReadFile(UserParameterFileNameAuto)
# 
# # Add tower pullback
# index=inpFindString(user_data_cell,'tower.F_pullback_south') user_data_cell{index}=['tower.F_pullback_south=' + num2str(tower.F_pullback_south,'%0.3e') ';# automatic calcuation']
# index=inpFindString(user_data_cell,'tower.F_pullback_north') user_data_cell{index}=['tower.F_pullback_north=' + num2str(tower.F_pullback_north,'%0.3e') ';# automatic calcuation']
# 
# # Add new names
# index=inpFindString(user_data_cell,'abaqus.InputName=') user_data_cell{index}=['abaqus.InputName=' , '''' abaqus.InputName '_postupdgeo' , '''' ]
# index=inpFindString(user_data_cell,'abaqus.JobName=') user_data_cell{index}=['abaqus.JobName=' , '''' abaqus.JobName '_postupdgeo' , '''' ]
# inpWriteFile(user_data_cell,UserParameterFileNameAuto)
# 
# # Export to find deflected coordinates
# dir_odb=abaqus.FolderNameModel;
# dir_export=abaqus.FolderNameModel;
# dir_python='C:\Cloud\OD_OWP\Work\Abaqus\Python\exportmodal\';
# FrequencyStepNumber=-1;
# ExportFileName=[abaqus.JobName '_export']
# 
# AbaqusExportModal(dir_odb,dir_export,dir_python,[abaqus.JobName],FrequencyStepNumber,ExportFileName,'AssemblyName','','ShowText',false)
# StaticResults=load([dir_export '\' ExportFileName '.mat'])
# 
# # Find cable deflection
# NodeNumberCable=cablemesh.NodeMatrix{1}(:,1)
# NodeCoordCable0=cablemesh.NodeMatrix{1}(:,2:4)
# 
# [~,ind_min]=min(abs(NodeCoordCable0(:,1)))
# NodeNumberCableMid=NodeNumberCable(ind_min)
# NodeCoordCable0Mid=NodeCoordCable0(ind_min,:)
# 
# NodeCoordCableDefMid=getSubsetRow(StaticResults.nodecoord,NodeNumberCableMid,StaticResults.nodecoord_label)
# dz_cable_actual=NodeCoordCable0Mid[3]-NodeCoordCableDefMid[3]
# 
# numtools.starprint(['Initialized dz_cable_deflection=' + num2str(geo.dz_cable_deflection,'%0.3f') ' m'] ['Actual dz_cable_deflection=' + num2str(dz_cable_actual,'%0.3f') ' m']},1)
# 
# user_data_cell=inpReadFile(UserParameterFileNameAuto)
# index=inpFindString(user_data_cell,'geo.dz_cable_deflection')
# user_data_cell{index}=[ 'geo.dz_cable_deflection=' + num2str(dz_cable_actual,'%0.3e') ';# automatic calcuation']
# 
# # Find bridge cog deflection
# NodeNumberBridgeCog=bridgemesh.NodeMatrix{1}(:,1)
# NodeCoordBridgeCog0=bridgemesh.NodeMatrix{1}(:,2:4)
# 
# for k=1:3
#     
#     fieldnames=['dz_cog_midspan_deflection' , 'dz_cog_south_deflection' , 'dz_cog_north_deflection']
# 
#     if k==1
#     [~,ind_node]=min(abs(NodeCoordBridgeCog0(:,1)))
#     elif k==2
#     [~,ind_node]=min(NodeCoordBridgeCog0(:,1))
#     elif k==3
#     [~,ind_node]=max(NodeCoordBridgeCog0(:,1))
#     end
#     
#     NodeCoordBridgeCogDef=getSubsetRow(StaticResults.nodecoord,NodeNumberBridgeCog(ind_node),StaticResults.nodecoord_label)
#     dz_actual=NodeCoordBridgeCog0(ind_node,3)-NodeCoordBridgeCogDef[3]
#     
#     numtools.starprint(['Initialized ' fieldnames{k} '=' + num2str(getfield(geo,fieldnames{k}),'%0.3f') ' m'] ['Actual ' fieldnames{k} '=' + num2str(dz_actual,'%0.3f') ' m']},1)
# 
#     index=inpFindString(user_data_cell,[ 'geo.' fieldnames{k} ] )
#     user_data_cell{index}=[ 'geo.' fieldnames{k} '=' + num2str(dz_actual,'%0.3e') ';# automatic calcuation']
#     
# end
# 
# # Hanger adjustment
# NodeCoordHangerUp=getSubsetRow(StaticResults.nodecoord,meta.cable.NodeNumberWestHanger,StaticResults.nodecoord_label)
# 
# U1_hanger=NodeCoordHangerUp(:,1).'-meta.x_hanger;
# 
# x_hat=meta.x_hanger./(geo.L_bridgedeck/2)
# polycoeff=np.polyfit(x_hat,U1_hanger,3)
# polycoeff=round(polycoeff,3)
# 
# index=inpFindString(user_data_cell,'cable.polycoeff_hanger_adjust=')
# user_data_cell{index}=['cable.polycoeff_hanger_adjust=' PrintMatrix(polycoeff) ]
# 
# # Write file
# inpWriteFile(user_data_cell,UserParameterFileNameAuto)
# pause(0.1)
# 
# # Run with updated geometry
# MainSuspensionBridge(UserParameterFileNameAuto,'UpdateGeometry',false,'IterateDeflection',false)
# 
# end
# 
# 
# =============================================================================




