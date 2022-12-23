
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

def ProcessUserParameters(UserParameterFile):

    # Extension
    if UserParameterFile[-3:]!='.py':
        UserParameterFile=UserParameterFile + '.py'

    # Check if file exists
    if not os.path.isfile(UserParameterFile):
        raise Exception(' ***** The user parameter file ' + UserParameterFile + ' not found' '')


    #(abaqus,bearing,bridgedeck,cable,geo,hanger,modal,sadle,step,tower,time)=(['Dummy'])*11
    
    # Run file
    exec(open(UserParameterFile).read(), globals())
    # execfile(UserParameterFile)
    
    time.sleep(0.1)
    
    print(abaqus.cpus)

        
#%%  Check that inputs are provided (not exhaustive)

    fieldnames=['FolderNameModel' , 'InputName' , 'JobName' , 'PartName' , 'AssemblyName' , 'RunJob' , 'cmd' , 'cpus' , 'restart' , 'halt_error']
    CheckField(abaqus,'abaqus',fieldnames)
        
    fieldnames=['type' , 'stiffness_south' , 'stiffness_north' , 'NodeNumberBase' , 'ElementNumberBase' ]
    CheckField(bearing,'bearing',fieldnames)
    
    fieldnames=['normaldir' , 'meshsize' , 'N_box' , 'shell' , 'NodeNumberBase' , 'ElementNumberBase' , 'NodeNumberBaseOuter' , 'ElementNumberBaseConnLat' ]
    CheckField(bridgedeck,'bridgedeck',fieldnames)
    
    fieldnames=['A' , 'I11' , 'I22' , 'I12' , 'It' , 'rho' , 'E' , 'G' , 'sc1' , 'sc2']
    CheckField(bridgedeck.cs,'bridgedeck.cs',fieldnames)
    
    fieldnames=['m' , 'x1' , 'x2' , 'alpha' , 'I11' , 'I22' , 'I12']
    CheckField(bridgedeck.inertia,'bridgedeck.inertia',fieldnames)

    fieldnames=['normaldir' , 'NodeNumberBase' , 'ElementNumberBase' , 'meshsize_approx' , 'N_element' , 'tempsupport' , 'polycoeff_hanger_adjust']
    CheckField(cable,'cable',fieldnames)
    
    fieldnames=['A' , 'I11' , 'I22' , 'I12' , 'It' , 'rho' , 'E' , 'G' , 'sigma_target']
    CheckField(cable.cs,'cable.cs',fieldnames)    
    
    fieldnames=[
    
    'L_bridgedeck',
    
    'gap',
    
    'dx_hanger',
    'dx_hanger',

    'dx_pullback_south',
    'dx_endpiece_max',
    
    'dx_endpiece_max',
    
    'z_cog_south',
    'z_cog_north',
    'z_cog_midspan',
    'dz_cog_midspan_deflection',
    'dz_cog_south_deflection',
    'dz_cog_north_deflection',
    
    'z_cable_top_south',
    'z_cable_top_north',
    'z_cable_midspan',
    'dz_cable_deflection',
    
    'dy_cable_anch_south',
    'dy_cable_top_south',
    'dy_cable_midspan',
    'dy_cable_top_north',
    'dy_cable_anch_north',
    
    'dy_cog_hanger',
    'dz_cog_hanger',
    'dz_cog_inner',
    'dy_cog_inner',
    
    'dy_pendulum',
    'dz_slider',
    'dx_bearing_base',
    
    'z_tower_base_south',
    'z_tower_base_north',
    
    'z_tower_top_south',
    'z_tower_top_north',
    
    'dy_tower_base_south',
    'dy_tower_base_north',
    
    'dy_tower_top_south',
    'dy_tower_top_north',
    
    'dx_tower_anch_south',
    'dx_tower_anch_north',
    
    'z_anch_south',
    'z_anch_north',
    
    'x_tower_south',
    'x_tower_north'
    
    ]
    
    CheckField(geo,'geo',fieldnames)
    
    fieldnames=['normaldir' , 'ElementNumberBase']
    CheckField(hanger,'hanger',fieldnames)
    
    fieldnames=['A' , 'I11' , 'I22' , 'I12' , 'It' , 'rho' , 'E' , 'G']
    CheckField(hanger.cs,'hanger.cs',fieldnames)
        
    fieldnames=['N_modes' , 'normalization' ]
    CheckField(modal,'modal',fieldnames)

    fieldnames=['stiffness' , 'ElementNumberBase' ]
    CheckField(sadle,'sadle',fieldnames)
    
    fieldnames=['normaldir' , 'F_pullback_south' , 'F_pullback_north' , 'z_crossbeam_south' , 'z_crossbeam_north' , 'h_crossbeam' , 'b_crossbeam' , 't_crossbeam']
    CheckField(tower,'tower',fieldnames)
    
    fieldnames=['type' , 'h_vec' , 'b_vec' , 'b_vec' , 'z_vec' , 'rho' , 'E' , 'v']
    CheckField(tower.cs,'tower.cs',fieldnames)


#%%  Some other checks

    # Delete gap parameter is single deck
    if bridgedeck.N_box==1 and not np.isnan(geo.gap):
        warnings.warn('***** Single bridge deck, geo.gap set to nan', stacklevel=2)
        geo.gap=np.nan
        
    # Stiffness non-zero
    for k in np.arange(len(bearing.stiffness_south)):
        if bearing.stiffness_south[k]==0 or bearing.stiffness_north[k]==0:
            warnings.warn('***** Zero spring stiffness in bearing, advise to set to small positive number')
            

    if bridgedeck.N_box==1:
        
        bridgedeck.gapbeam.type='NotUsed'
        bridgedeck.gapbeam.h=np.nan
        bridgedeck.gapbeam.b=np.nan
        bridgedeck.gapbeam.t=np.nan
    
        geo.dz_cog_inner=np.nan
        geo.dy_cog_inner=np.nan


    # Bridge deck properties, double if given for one bridge deck only
# =============================================================================
#     if bridgedeck.N_box==2:
#         
#         n_copied=0
#         
#         if n_copied>0:
#             warnings.warn('***** ' + str(n_copied) + ' cross section properties given only for one bridge deck, copied for the second', stacklevel=2)
#             warnings.warn('***** The above should be checked and preferably avoided', stacklevel=2)
# =============================================================================


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
    if np.abs(geo.z_cable_top_south-geo.z_tower_top_south)>3 or np.abs(geo.z_cable_top_north-geo.z_tower_top_north)>3:
        warnings.warn('***** Distance between cable top and tower top larger than 3 m', stacklevel=2)

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

    # Check if crossbeams is above tower
    if np.max(tower.z_crossbeam_south)>geo.z_tower_top_south or np.max(tower.z_crossbeam_north)>geo.z_tower_top_north:
        warnings.warn('***** Crossbeam elevation above tower top', stacklevel=2)


    # Lateral coordinate of roller and pendulum
    geo.y_bearing=[None]*bridgedeck.N_box
    if bridgedeck.N_box==1:
        geo.y_bearing[0]=[None]*3
        
        # East pendulum, roller middle, west pendulum
        geo.y_bearing[0][0]=-geo.dy_cog_hanger+geo.dy_pendulum
        geo.y_bearing[0][1]=0
        geo.y_bearing[0][2]=geo.dy_cog_hanger-geo.dy_pendulum;
    elif bridgedeck.N_box==2:
        geo.y_bearing[0]=[None]*3
        geo.y_bearing[1]=[None]*3
        
        # East pendulum outer, roller east, east pendulum inner
        geo.y_bearing[0][0]=-geo.gap/2-geo.dy_cog_hanger+geo.dy_pendulum
        geo.y_bearing[0][1]=-geo.gap/2
        geo.y_bearing[0][2]=-geo.gap/2+geo.dy_cog_inner-geo.dy_pendulum
        
        # West pendulum inner, roller west, west pendulum outer
        geo.y_bearing[1][0]=-geo.y_bearing[0][2]
        geo.y_bearing[1][1]=-geo.y_bearing[0][1]
        geo.y_bearing[1][2]=-geo.y_bearing[0][0]
    
    # Check if retraction of towers are correct sign
    if geo.dx_pullback_south>0:
        warnings.warn('***** Retraction of south tower should be negative')
        print(geo.dx_pullback_south)
        
    if geo.dx_pullback_north<0:
        warnings.warn('***** Retraction of north tower should be positive')
        print(geo.dx_pullback_north)
        
    # Replace name
    # forwardslash='/'
    # backslash='\\'
    # abaqus.FolderNameModel=abaqus.FolderNameModel.replace(forwardslash,backslash)

    # Check if folder exists
    if os.path.isdir(abaqus.FolderNameModel)==0:
        os.mkdir(abaqus.FolderNameModel);
        print('***** Creating folder ' + abaqus.FolderNameModel )


    return (abaqus,bearing,bridgedeck,cable,geo,hanger,modal,sadle,step,tower)



#%%  Function to check is struct contains fields

def CheckField(struct_obj,struct_obj_name,fieldnames,halt_error=False):
    
    for fieldnames_sub in fieldnames:
        
        if not (fieldnames_sub in struct_obj.fields()):  
            warnings.warn('***** In the struct: ' + struct_obj_name + ' , the following field is missing: ' + fieldnames_sub, stacklevel=2)
            
            if halt_error:
                raise Exception('***** ' , 'Aborted, see warning above on missing fields')
  
