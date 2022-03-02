# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 11:39:19 2021

@author: OWP
"""

#%%

import os
import numpy as np

from ypstruct import *

from .CableGeometry import *

from .. import numtools

from ..fem_corot.NonLinearSolver import *
from ..fem_corot.ProcessModel import *
from ..fem_corot.Assembly import *
from ..fem_corot.Corot import *


function [F_pullback_south,F_pullback_north,K_south,K_north,K_est]=
def EstimatePullbackForce(tower,geo,abaqus):

#%%  Function to run pullback of towers to estimate the force neccessary to reach the desired dx

    # Simulations are non-linear so this is just an approximation
    # One can always check the final abaqus model


#%%  Estimate approx pullback force based on cantilever model, tapered cross section

    L_num=geo.z_tower_top_south-geo.z_tower_base_south
    I_num=1/12*(tower.cs.h_vec**3*tower.cs.b_vec-(tower.cs.h_vec-2*tower.cs.t_vec)**3*(tower.cs.b_vec-2*tower.cs.t_vec))
    E_num=tower.cs.E;

    c=np.polyfit(tower.cs.z_vec,I_num,1) I_0_num=np.polyval(c,tower.cs.z_vec[1]) I_end_num=np.polyval(c,tower.cs.z_vec[-1]))

    if abs(I_0_num./I_end_num-1)<1e-3:
        I_0_num=1.001*I_end_num
        
    K_num=K_cantilever(L_num,I_0_num,I_end_num,E_num)

    delta=abs(geo.dx_pullback_south)
    F=delta*K_num
    K_est=K_num


    #%%  Assume 20% reduction due to nonlinear effects

    UnitLoadSouth=-F*0.8
    UnitLoadNorth=F*0.8

    #%%  Abaqus info

    abaqus.FolderNameModel='C:\Temp';
    abaqus.InputName='SB_TempJob_1';
    abaqus.JobName=abaqus.InputName;
    abaqus.PartName='PartTower';
    abaqus.AssemblyName='AssemblyTower';
    abaqus.RunJob=False;

    #%%  Open file

    InputFileName=abaqus.FolderNameModel + '/' + abaqus.InputName + '.inp'
    
    fid=open(InputFileName,'w')
    

    #%%  Materials

    gen.Comment(fid,'MATERIALS',False)

    gen.Material(fid,'CONCRETE',tower.cs.E,tower.cs.v,tower.cs.rho)

    #%%  Part

    gen.Part(fid,abaqus.PartName)

    #%%  Tower

    meta=struct()
    [meta,towermesh]=TowerGeometry(fid,meta,geo,tower)

    #%%  Part, instance, assembly

    gen.PartEnd(fid)

    gen.Comment(fid,'ASSEMBLY',False)

    gen.Assembly(fid,abaqus.AssemblyName)

    gen.Instance(fid,abaqus.PartName '',abaqus.PartName)

    gen.InstanceEnd(fid)

    gen.AssemblyEnd(fid)

    #%%  Step

    gen.Step(fid,['NLGEO=YES, NAME=STEP0'],'')
    gen.Static(fid,['1e-2, 1, 1e-6, 1'])

    gen.Cload(fid,'NEW',['Tower_top_south_east','Tower_top_south_west'],1,UnitLoadSouth,abaqus.PartName)
    gen.Cload(fid,'NEW',['Tower_top_north_east','Tower_top_north_west'],1,UnitLoadNorth,abaqus.PartName)
    
    gen.Gravload(fid,'new',[''],9.81)
    
    gen.Boundary(fid,'new','Tower_base',[1,6,0],abaqus.PartName)

    gen.FieldOutput(fid,'NODE',['U' , 'RF' , 'COORD'],'','FREQUENCY=100')
    gen.FieldOutput(fid,'ELEMENT',['SF'],'','FREQUENCY=100')
    
    gen.StepEnd(fid)

    #%%  Run job

    # Check input file for duplicate node/element numbers
    abq.CheckDuplicateNumbers(InputFileName)
    
    # Run
    if abaqus.RunJob==True:
        abq.RunJob(abaqus.cmd,abaqus.FolderNameModel,abaqus.InputName,abaqus.JobName,abaqus.cpus,True,True)

    #%%  Export data

    dir_odb=abaqus.FolderNameModel;
    dir_export=abaqus.FolderNameModel;
    dir_python='C:\Cloud\OD_OWP\Work\Abaqus\Python\exportmodal\';
    FrequencyStepNumber=-1;
    ExportFileName=[abaqus.JobName '_export']

    AbaqusExportModal(dir_odb,dir_export,dir_python,abaqus.JobName,FrequencyStepNumber,ExportFileName,'AssemblyName','notrelevant','ShowText',false)

    #%% 

    StaticResults=load([dir_export '\' ExportFileName '.mat'])

    NodeSouth=towermesh.NodeMatrix{1}(end,1) 
    u_south=getSubsetRow(StaticResults.phi,[num2str(NodeSouth) '_U1'],StaticResults.phi_label)
    u_south=u_south(end)

    NodeNorth=towermesh.NodeMatrix{3}(end,1)
    u_north=getSubsetRow(StaticResults.phi,[num2str(NodeNorth) '_U1'],StaticResults.phi_label)
    u_north=u_north(end)

    K_south=UnitLoadSouth/u_south;
    K_north=UnitLoadNorth/u_north;

    F_pullback_south=K_south*geo.dx_pullback_south;
    F_pullback_north=K_north*geo.dx_pullback_north;

    numtools.starprint({['F_pullback_south=' + num2str(F_pullback_south,'%0.3e') ' N'] ['F_pullback_north=' + num2str(F_pullback_north,'%0.3e') ' N']},1)

    return
#%% 
    def K_cantilever(L,I_0,I_end,E)

        K_val=
        (2*(E*I_0**3 - 3*E*I_0**2*I_end + 3*E*I_0*I_end**2 - E*I_end**3))
        /(I_0**2*L**3 + 3*I_end**2*L**3 + 2*I_end**2*L**3*log(I_0*L) - 2*I_end**2*L**3*log(I_end*L) - 4*I_0*I_end*L**3)

        return K_val