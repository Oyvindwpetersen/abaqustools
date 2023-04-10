
# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""
    
#%%

import os
import numpy as np
import warnings
import putools
import time
from ypstruct import *

#%% Check user parameter file

def processpar(UserParameterFile):

    # Extension
    if not UserParameterFile.endswith('.py'):
        UserParameterFile=UserParameterFile + '.py'

    # Check if file exists
    if not os.path.isfile(UserParameterFile):
        raise Exception(' ***** The user parameter file ' + UserParameterFile + ' not found' '')


    #(abaqus,bearing,bridgedeck,cable,geo,hanger,modal,sadle,step,tower,time)=(['Dummy'])*11
    
    # Run file
    exec(open(UserParameterFile).read(), globals())
    # execfile(UserParameterFile)
    
    time.sleep(0.1)
    
            
#%%  Check that inputs are provided (not exhaustive)

#%%% Abaqus
    fieldnames=[]
    fieldtypes=[]
    
    fieldnames.append('foldername')
    fieldtypes.append('str')
    
    fieldnames.append('inputname')
    fieldtypes.append('str')
    
    fieldnames.append('jobname')
    fieldtypes.append('str')
    
    fieldnames.append('partname')
    fieldtypes.append('str')
        
    fieldnames.append('assemblyname')
    fieldtypes.append('str')
        
    fieldnames.append('runjob')
    fieldtypes.append('log')
        
    fieldnames.append('cmd')
    fieldtypes.append('str')
        
    fieldnames.append('cpus')
    fieldtypes.append('num')
        
    fieldnames.append('restart')
    fieldtypes.append('log')
        
    fieldnames.append('halt_error')
    fieldtypes.append('log')

    CheckField(abaqus,'abaqus',fieldnames,fieldtypes)

#%%% Bearing

    fieldnames=[]
    fieldtypes=[]
    
    fieldnames.append('type')
    fieldtypes.append('str')
    
    fieldnames.append('stiffness_south')
    fieldtypes.append('num')
    
    fieldnames.append('stiffness_north')
    fieldtypes.append('num')
    
    fieldnames.append('nodenum_base')
    fieldtypes.append('num')
        
    fieldnames.append('elnum_base')
    fieldtypes.append('num')

    CheckField(bearing,'bearing',fieldnames,fieldtypes)

#%%% Bridgedeck

    fieldnames=[]
    fieldtypes=[]
    
    fieldnames.append('normaldir')
    fieldtypes.append('num')
    
    fieldnames.append('meshsize')
    fieldtypes.append('num')
    
    fieldnames.append('N_box')
    fieldtypes.append('num')
    
    fieldnames.append('shell')
    fieldtypes.append('log')
        
    fieldnames.append('nodenum_base')
    fieldtypes.append('num')
    
    fieldnames.append('elnum_base')
    fieldtypes.append('num')
    
    fieldnames.append('nodenum_base_outer')
    fieldtypes.append('num')
        
    fieldnames.append('elnum_base_connlat')
    fieldtypes.append('num')
    
    CheckField(bridgedeck,'bridgedeck',fieldnames,fieldtypes)

    fieldnames=['A' , 'I11' , 'I22' , 'I12' , 'It' , 'rho' , 'E' , 'G' , 'sc1' , 'sc2']
    fieldtypes=['num']*len(fieldnames)
    CheckField(bridgedeck.cs,'bridgedeck.cs',fieldnames,fieldtypes)
    
    fieldnames=['m' , 'x1' , 'x2' , 'alpha' , 'I11' , 'I22' , 'I12']
    fieldtypes=['num']*len(fieldnames)
    CheckField(bridgedeck.inertia,'bridgedeck.inertia',fieldnames,fieldtypes)

#%%% Cables

    fieldnames=[]
    fieldtypes=[]
    
    fieldnames.append('normaldir')
    fieldtypes.append('num')
    
    fieldnames.append('nodenum_base')
    fieldtypes.append('num')
    
    fieldnames.append('elnum_base')
    fieldtypes.append('num')
    
    fieldnames.append('meshsize_approx')
    fieldtypes.append('num')
    
    fieldnames.append('N_element')
    fieldtypes.append('num')
    
    fieldnames.append('tempsupport')
    fieldtypes.append('log')
    
    fieldnames.append('N_tempsupport')
    fieldtypes.append('num')
    
    fieldnames.append('clamp')
    fieldtypes.append('log')
    
    fieldnames.append('N_clamp')
    fieldtypes.append('num')
    
    fieldnames.append('F_clamp')
    fieldtypes.append('num')    
    
    fieldnames.append('polycoeff_hanger_adjust')
    fieldtypes.append('num')
    
    fieldnames.append('nsmass')
    fieldtypes.append('num')
    
    CheckField(cable,'cable',fieldnames,fieldtypes)
    
    fieldnames=['A' , 'I11' , 'I22' , 'I12' , 'It' , 'rho' , 'E' , 'G' , 'sigma_target']
    fieldtypes=['num']*len(fieldnames)
    CheckField(cable.cs,'cable.cs',fieldnames,fieldtypes)

 
#%%% Geometry

    fieldnames=[]
    fieldtypes=[]
    
    fieldnames.append('L_bridgedeck')
    fieldtypes.append('num')
    
    fieldnames.append('gap')
    fieldtypes.append('num')
    
    fieldnames.append('dx_hanger')
    fieldtypes.append('num')
    
    fieldnames.append('dx_pullback_south')
    fieldtypes.append('num')
    
    fieldnames.append('dx_pullback_north')
    fieldtypes.append('num')
    
    fieldnames.append('dx_endpiece_max')
    fieldtypes.append('num')
    
    fieldnames.append('z_cog_south')
    fieldtypes.append('num')
    
    fieldnames.append('z_cog_north')
    fieldtypes.append('num')
    
    fieldnames.append('z_cog_midspan')
    fieldtypes.append('num')
    
    fieldnames.append('dz_cog_midspan_deflection')
    fieldtypes.append('num')
    
    fieldnames.append('dz_cog_south_deflection')
    fieldtypes.append('num')
    
    fieldnames.append('dz_cog_north_deflection')
    fieldtypes.append('num')
    
    fieldnames.append('z_cable_top_south')
    fieldtypes.append('num')
    
    fieldnames.append('z_cable_top_north')
    fieldtypes.append('num')
    
    fieldnames.append('z_cable_midspan')
    fieldtypes.append('num')
    
    fieldnames.append('dz_cable_deflection')
    fieldtypes.append('num')
    
    fieldnames.append('dy_cable_anch_south')
    fieldtypes.append('num')
    
    fieldnames.append('dy_cable_top_south')
    fieldtypes.append('num')
        
    fieldnames.append('dy_cable_midspan')
    fieldtypes.append('num')
        
    fieldnames.append('dy_cable_top_north')
    fieldtypes.append('num')
        
    fieldnames.append('dy_cable_anch_north')
    fieldtypes.append('num')
        
    fieldnames.append('dy_cog_hanger')
    fieldtypes.append('num')
        
    fieldnames.append('dz_cog_hanger')
    fieldtypes.append('num')   
        
    fieldnames.append('dz_cog_inner')
    fieldtypes.append('num')   
        
    fieldnames.append('dy_cog_inner')
    fieldtypes.append('num')   
        
    fieldnames.append('dy_pendulum')
    fieldtypes.append('num')   
        
    fieldnames.append('dz_slider')
    fieldtypes.append('num')   
        
    fieldnames.append('dx_bearing_base')
    fieldtypes.append('num')   
            
    fieldnames.append('z_tower_base_south')
    fieldtypes.append('num')   
            
    fieldnames.append('z_tower_base_north')
    fieldtypes.append('num')   
            
    fieldnames.append('z_tower_top_south')
    fieldtypes.append('num')   
            
    fieldnames.append('z_tower_top_north')
    fieldtypes.append('num')   
            
    fieldnames.append('dy_tower_base_south')
    fieldtypes.append('num')   
            
    fieldnames.append('dy_tower_base_north')
    fieldtypes.append('num')   
            
    fieldnames.append('dy_tower_top_south')
    fieldtypes.append('num')   
            
    fieldnames.append('dy_tower_top_north')
    fieldtypes.append('num')   
            
    fieldnames.append('dx_tower_anch_south')
    fieldtypes.append('num')   
            
    fieldnames.append('dx_tower_anch_north')
    fieldtypes.append('num')   
            
    fieldnames.append('z_anch_south')
    fieldtypes.append('num')   
            
    fieldnames.append('z_anch_north')
    fieldtypes.append('num')   
            
    fieldnames.append('x_tower_south')
    fieldtypes.append('num')   
            
    fieldnames.append('x_tower_north')
    fieldtypes.append('num')   
    

    CheckField(geo,'geo',fieldnames,fieldtypes)
 
 
#%%% Hanger

    fieldnames=[]
    fieldtypes=[]
    
    fieldnames.append('normaldir')
    fieldtypes.append('num')

    fieldnames.append('elnum_base')
    fieldtypes.append('num')

    fieldnames=['A' , 'I11' , 'I22' , 'I12' , 'It' , 'rho' , 'E' , 'G']
    fieldtypes=['num']*len(fieldnames)
    CheckField(hanger.cs,'hanger.cs',fieldnames,fieldtypes)

#%%% Modal

    fieldnames=[]
    fieldtypes=[]
    
    fieldnames.append('N_modes')
    fieldtypes.append('num')

    fieldnames.append('normalization')
    fieldtypes.append('str')
  
    CheckField(modal,'modal',fieldnames,fieldtypes)
  
#%%% Sadle

    fieldnames=[]
    fieldtypes=[]
    
    fieldnames.append('stiffness')
    fieldtypes.append('num')

    fieldnames.append('elnum_base')
    fieldtypes.append('num')  
    
    CheckField(sadle,'sadle',fieldnames,fieldtypes)
    
#%%% Tower

    fieldnames=[]
    fieldtypes=[]
    
    fieldnames.append('normaldir')
    fieldtypes.append('num')

    fieldnames.append('F_pullback_south')
    fieldtypes.append('num')  

    fieldnames.append('F_pullback_north')
    fieldtypes.append('num')  

    fieldnames.append('z_crossbeam_south')
    fieldtypes.append('num')  

    fieldnames.append('z_crossbeam_north')
    fieldtypes.append('num')  

    fieldnames.append('h_crossbeam')
    fieldtypes.append('num')  

    fieldnames.append('b_crossbeam')
    fieldtypes.append('num')  

    fieldnames.append('t_crossbeam')
    fieldtypes.append('num')  
    
    CheckField(tower,'tower',fieldnames,fieldtypes)
    
    fieldnames=['type' , 'h_vec' , 'b_vec' , 'b_vec' , 'z_vec' , 'rho' , 'E' , 'v']
    fieldtypes=['str']+['num']*7
    CheckField(tower.cs,'tower.cs',fieldnames,fieldtypes)


#%%  Some other checks

    # Delete gap parameter is single deck
    if bridgedeck.N_box==1 and not np.isnan(geo.gap):
        warnings.warn('***** Single bridge deck, geo.gap set to nan', stacklevel=2)
        geo.gap=np.nan
        
    # Stiffness non-zero
    for k in np.arange(len(bearing.stiffness_south)):
        if bearing.stiffness_south[k]==0 or bearing.stiffness_north[k]==0:
            warnings.warn('***** Zero spring stiffness in bearing, advise to set to small positive number')
            
    # Remove if single box
    if bridgedeck.N_box==1:
        
        bridgedeck.gapbeam.type='NotUsed'
        bridgedeck.gapbeam.h=np.nan
        bridgedeck.gapbeam.b=np.nan
        bridgedeck.gapbeam.t=np.nan
    
        geo.dz_cog_inner=np.nan
        geo.dy_cog_inner=np.nan

    # Check if tower cross section properties is given for entire height
    if tower.cs.z_vec[-1]<geo.z_tower_top_south or tower.cs.z_vec[-1]<geo.z_tower_top_north:
        
        warnings.warn('***** Tower cross section property specified to z=' + putools.num.num2strf(tower.cs.z_vec[-1],3) + ' m', stacklevel=2)
        warnings.warn('***** Max tower elevation z=' + putools.num.num2strf(max(geo.z_tower_top_south,geo.z_tower_top_north),3) + ' m', stacklevel=2)
        warnings.warn('***** Applying constant extrapolation of cross section properties beyond last point', stacklevel=2)
        
        tower.cs.z_vec=np.hstack((tower.cs.z_vec , max(geo.z_tower_top_south,geo.z_tower_top_north)))
        tower.cs.t_vec=np.hstack((tower.cs.t_vec , tower.cs.t_vec[-1]))
        tower.cs.b_vec=np.hstack((tower.cs.b_vec , tower.cs.b_vec[-1]))
        tower.cs.h_vec=np.hstack((tower.cs.h_vec , tower.cs.h_vec[-1]))
    

    # Cross section of tower
    if tower.cs.z_vec[0]>geo.z_tower_base_south or tower.cs.z_vec[0]>geo.z_tower_base_south:
        
        warnings.warn('***** Tower cross section property specified from z=' + putools.num.num2strf(tower.cs.z_vec[0],3) + ' m', stacklevel=2)
        warnings.warn('***** Min tower elevation z=' + putools.num.num2strf(min(geo.z_tower_base_south,geo.z_tower_base_north),3) + ' m', stacklevel=2)
        warnings.warn('***** Applying constant extrapolation of cross section properties beyond first point', stacklevel=2)
    
        tower.cs.z_vec=np.hstack(( min(geo.z_tower_base_south,geo.z_tower_base_north) , tower.cs.z_vec))
        tower.cs.t_vec=np.hstack((tower.cs.t_vec[0] , tower.cs.t_vec))
        tower.cs.b_vec=np.hstack((tower.cs.b_vec[0] , tower.cs.b_vec))
        tower.cs.h_vec=np.hstack((tower.cs.h_vec[0] , tower.cs.h_vec))

    # Mass
    if any(bridgedeck.cs.rho>0):
        warnings.warn('***** Rho of bridge deck should be set to zero if beam added inertia is used (avoid double mass)', stacklevel=2)

    # Distance between cable and tower sadle
    if np.abs(geo.z_cable_top_south-geo.z_tower_top_south)>1 or np.abs(geo.z_cable_top_north-geo.z_tower_top_north)>1:
        warnings.warn('***** Distance between cable top and tower top larger than 1 m', stacklevel=2)

    # Distance between cable and and bridge
    dz_cb=(geo.z_cable_midspan+geo.dz_cable_deflection)-(geo.z_cog_midspan+geo.dz_cog_midspan_deflection)
    if dz_cb<0:
        warnings.warn('***** Main cable is below bridge deck COG at midspan', stacklevel=2)

    # Check if crossbeams are above tower
    if max(tower.z_crossbeam_south)>geo.z_tower_top_south or max(tower.z_crossbeam_north)>geo.z_tower_top_north:
        warnings.warn('***** Crossbeam elevation higher than tower top', stacklevel=2)

    # Check if cable is inclined and temp supports
    if abs(geo.dy_cable_top_south-geo.dy_cable_midspan)>10e-3 or abs(geo.dy_cable_top_north-geo.dy_cable_midspan)>10e-3:
       if cable.tempsupport==False:
            warnings.warn('***** Cable distance not equal at midspan and towers. Consider to turn on temporary cable supports (cable.tempsupport=True)', stacklevel=2)
   
   # Check if retraction of towers are correct sign
    if geo.dx_pullback_south>0:
        warnings.warn('***** Retraction of south tower should be negative')
        print(geo.dx_pullback_south)
        
    if geo.dx_pullback_north<0:
        warnings.warn('***** Retraction of north tower should be positive')
        print(geo.dx_pullback_north)
    
#%% Bearing
        
    # Lateral coordinate of roller and pendulum
    
    if bridgedeck.N_box==1:
        geo.y_bearing_box1=[None]*3
        
        # East pendulum, roller middle, west pendulum
        geo.y_bearing_box1[0]=-geo.dy_cog_hanger+geo.dy_pendulum
        geo.y_bearing_box1[1]=0
        geo.y_bearing_box1[2]=geo.dy_cog_hanger-geo.dy_pendulum;
        
    elif bridgedeck.N_box==2:
        geo.y_bearing_box1=[None]*3
        geo.y_bearing_box2=[None]*3
        
        # East pendulum outer, roller east, east pendulum inner
        geo.y_bearing_box1[0]=-geo.gap/2-geo.dy_cog_hanger+geo.dy_pendulum
        geo.y_bearing_box1[1]=-geo.gap/2
        geo.y_bearing_box1[2]=-geo.gap/2+geo.dy_cog_inner-geo.dy_pendulum
        
        # West pendulum inner, roller west, west pendulum outer
        geo.y_bearing_box2[0]=-geo.y_bearing_box1[2]
        geo.y_bearing_box2[1]=-geo.y_bearing_box1[1]
        geo.y_bearing_box2[2]=-geo.y_bearing_box1[0]
    
#%% Bearing

    # Check if folder exists
    if os.path.isdir(abaqus.foldername)==0:
        os.mkdir(abaqus.foldername);
        print('***** Creating folder ' + abaqus.foldername )


    return (abaqus,bearing,bridgedeck,cable,geo,hanger,modal,sadle,step,tower)


#%%  Function to check is struct contains fields

def CheckField(struct_obj,struct_obj_name,fieldnames,fieldtypes,halt_error=True):
    
    err=False
    
    for k in np.arange(len(fieldnames)):
        
        if not (fieldnames[k] in struct_obj.fields()):  
            warnings.warn('***** For struct: ' + struct_obj_name + ' , field is missing: ' + fieldnames[k], stacklevel=2)
            err=True
            continue
            
        if fieldtypes[k]=='str':
            if not isinstance(struct_obj[fieldnames[k]],str):
                warnings.warn('***** For struct: ' + struct_obj_name + ' , field is wrong type: ' + fieldnames[k], stacklevel=2)
                err=True

        if fieldtypes[k]=='log':
            if not isinstance(struct_obj[fieldnames[k]],bool):
                warnings.warn('***** For struct: ' + struct_obj_name + ' , field is wrong type: ' + fieldnames[k], stacklevel=2)
                err=True
                
        if fieldtypes[k]=='num':
            if not putools.num.isnumeric(struct_obj[fieldnames[k]]):
                print(struct_obj[fieldnames[k]])
                warnings.warn('***** For struct: ' + struct_obj_name + ' , field is wrong type: ' + fieldnames[k], stacklevel=2)
                err=True
                
            else:
                struct_obj[fieldnames[k]]=putools.num.ensurenp(struct_obj[fieldnames[k]])
                
        if err and halt_error:
            raise Exception('***** ' , 'Aborted, see warning above on missing or wrong fields')
        
        
    return struct_obj