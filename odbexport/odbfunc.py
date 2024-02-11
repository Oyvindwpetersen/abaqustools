# -*- coding: utf-8 -*-                       
from sys import path
import numpy as np
import odbAccess
import os
from textRepr import *
from timeit import default_timer as timer

# This module is imported in Abaqus by "import odbfunc"
# The folder containing odbfunc.py must first be added to the system path

#%%

def p(pstring):
    prettyPrint(pstring)

#%%

def open_odb(folder_odb,jobname):
    
    '''
    Open ODB file

    Arguments
    ------------
    folder_odb (str): folder of odb file
    jobname (str): name of odb file

    Returns
    ------------
    odb_id (odb object): odb file identifier
    
    '''

    if jobname.endswith('.odb'):
        jobname=jobname[:-4]
    
    odb_id=odbAccess.openOdb(folder_odb + '/' + jobname + '.odb',readOnly=True)
    
    return odb_id
    
#%%

def close_odb(odb_id):

    '''
    Close ODB file

    Arguments
    ------------
    odb_id (odb object): odb file identifier

    Returns
    ------------
    None
    
    '''

    odb_id.close()

#%%

def exporthistoryoutput(odb_id,stepnumber,hist_key,assembly_name=None):
    
    '''
    Export history outputs

    Arguments
    ------------
    odb_id (odb object): odb object
    stepnumber (int): step number for export, usually -1
    hist_key (str): output to export, e.g. EIGFREQ,GM,DAMPRATIO,EIGREAL,EIGIMAG
    assembly_name (str): assembly

    Returns
    ------------
    output_vec (np array): vector with history outputs
    
    '''

    step_name=odb_id.steps.keys()[stepnumber]
    step_id=odb_id.steps[step_name]
    
    if assembly_name is None:
        assembly_keys=step_id.historyRegions.keys()
        assembly_name=assembly_keys[0]
    
    hist_output_keys=step_id.historyRegions[assembly_name].historyOutputs.keys()
    
    # If key not found, return zero
    if hist_key not in hist_output_keys:
        output_vec=np.array([0])
        return output_vec
    else:
        hist_output=step_id.historyRegions[assembly_name].historyOutputs[hist_key]
        
    output_vec=np.array([hist_output.data[j][1] for j in range(0,len(hist_output.data))])
    
    return output_vec
    
#%%

def exportdisplacement(odb_id,stepnumber,framenumber=None):

    '''
    Export displacement field (U,UR) for a single step and multiple frames

    Arguments
    ------------
    odb_id (odb object): odb file identifier
    stepnumber (int): step number for export, usually -1
    framenumber (list): frame number(s) for export; None gives all frames; 'skipfirst' gives all except 0
    
    Returns
    ------------
    disp_matrix: matrix with each frame as column (e.g. N_DOF*N_frames)
    label_vec: list with DOF labels of all N_DOF
    
    '''
    
    step_name=odb_id.steps.keys()[stepnumber]
    step_id=odb_id.steps[step_name]
    
    if framenumber is None:
        framenumber=range(len(step_id.frames))
    elif framenumber=='skipfirst':
        framenumber=range(1,len(step_id.frames))
    elif isinstance(framenumber,int):
        framenumber=np.array([framenumber])
    
    frame_id=step_id.frames[-1]
    if not frame_id.fieldOutputs.has_key('U'):
        disp_matrix=np.array([0])
        label_vec=np.array([0])
        return disp_matrix,label_vec
    
    N_node=len(frame_id.fieldOutputs['U'].values)          
    N_frame=len(framenumber)    
    
    disp_matrix=np.zeros((N_node*6,N_frame))
    
    t_start=timer()
    for z in np.arange(len(framenumber)):
        
        frame_id=step_id.frames[framenumber[z]]
        
        disp_trans=frame_id.fieldOutputs['U']
        disp_trans_val=disp_trans.values
        
        disp_rot=frame_id.fieldOutputs['UR']
        disp_rot_val=disp_rot.values
        
        U_temp=np.array([disp_trans_val[n].data for n in range(N_node) ])
        UR_temp=np.array([disp_rot_val[n].data for n in range(N_node) ])
        
        disp_matrix[:,z]=np.hstack((U_temp,UR_temp)).flatten()
    
    label_vec_temp=[ [str(disp_trans_val[n].nodeLabel) + '_' + s  for s in disp_trans.componentLabels] + [str(disp_rot_val[n].nodeLabel) + '_' + s  for s in disp_rot.componentLabels] for n in range(N_node) ]
    label_vec=[item for sublist in label_vec_temp for item in sublist]
    
    t_end=timer()
    print('Time displacement ' + str(t_end-t_start) + ' s')
    return disp_matrix,label_vec

#%%

def exportnodecoord(odb_id,stepnumber,framenumber):
    
    '''
    Export node coordinates for a single step and a single frame

    Arguments
    ------------
    odb_id (odb object): odb file identifier
    stepnumber (int): step number for export, usually -1
    framenumber (int): frame number for export
    
    Returns
    ------------
    nodecoord: matrix with [nodenumber,x,y,z] as rows, size N_NODE*4
    
    '''

    step_name=odb_id.steps.keys()[stepnumber]
    step_id=odb_id.steps[step_name]
            
    frame_id=step_id.frames[framenumber]
    if 'COORD' not in frame_id.fieldOutputs.keys():
        nodecoord_matrix=np.array([0 , 0 , 0])
        nodecoord_label=np.array([0])
        nodecoord=np.hstack((nodecoord_label,nodecoord_matrix))
        return nodecoord
        
    t_start=timer()
    coord_val=frame_id.fieldOutputs['COORD'].values
    nodecoord_matrix=np.array([coord_val[ii].data for ii in range(len(coord_val))])
    nodecoord_label=np.zeros((np.shape(nodecoord_matrix)[0],1))
    nodecoord_label[:,0]=np.array([coord_val[ii].nodeLabel for ii in range(len(coord_val))])
    
    t_end=timer()
    print('Time nodecoord ' + str(t_end-t_start) + ' s')
    
    nodecoord=np.hstack((nodecoord_label,nodecoord_matrix))
    
    return nodecoord
        
#%%

def exportsectionforce(odb_id,stepnumber,framenumber=None):
    
    '''
    Export section forces (SF,SM) (beam only) for a single step and multiple frames
    
    Arguments
    ------------
    odb_id (odb object): odb file identifier
    stepnumber (int): step number for export, usually -1
    framenumber (list): frame number(s) for export; None gives all frames; 'skipfirst' gives all except 0
    
    Returns
    ------------
    sf_matrix: matrix with each frame as columns ( e.g. N_SF*N_MODES)
    label_vec: list with DOF labels of all N_DOF
    
    '''
    
    step_name=odb_id.steps.keys()[stepnumber]
    step_id=odb_id.steps[step_name]
    
    if framenumber is None:
        framenumber=range(len(step_id.frames))
    elif framenumber=='skipfirst':
        framenumber=range(1,len(step_id.frames))
    elif isinstance(framenumber,int):
        framenumber=np.array([framenumber])
    
    frame_id=step_id.frames[-1]
    if 'SF' not in frame_id.fieldOutputs.keys():
        sf_matrix=np.array([0 , 0 , 0])
        label_vec=np.array(['SF_not_found'])
        return sf_matrix,label_vec
    
    el_label_all=[ frame_id.fieldOutputs['SF'].values[n].baseElementType for n in range(len(frame_id.fieldOutputs['SF'].values)) ]
    index_B=[n for n, l in enumerate(el_label_all) if l.startswith('B')]
        
    sf_matrix=np.zeros((len(index_B)*6,len(framenumber)))
    
    for z in np.arange(len(framenumber)):
        
        frame_id=step_id.frames[framenumber[z]]
        
        output_sf=frame_id.fieldOutputs['SF']
        output_sf_val=output_sf.values
        
        output_sm=frame_id.fieldOutputs['SM']
        output_sm_val=output_sm.values
        
        sf_temp=np.array([output_sf_val[n].data for n in index_B ])
        sm_temp=np.array([output_sm_val[n].data for n in index_B ])
        
        output_sf_temp=np.hstack((sf_temp,sm_temp)).flatten()
        sf_matrix[:,z]=output_sf_temp
        
    sf_component_labels=output_sf.componentLabels
    
    # For SM:
    # Error in abaqus documentation? States 2 1 3 in odb file, but that is wrong.
    # >> OutputSM.componentLabels
    # >> ('SM2', 'SM1', 'SM3')    
    
    # Overwrite labels manually:    
    sm_component_labels=('SM1', 'SM2', 'SM3') 
    # NB! Important to verify results are reasonable
    
    label_vec_temp=[ [str(output_sf_val[n].elementLabel) + '_' + s  for s in sf_component_labels] + [str(output_sm_val[n].elementLabel) + '_' + s  for s in sm_component_labels] for n in index_B ]
    label_vec=[item for sublist in label_vec_temp for item in sublist]
    
    return sf_matrix,label_vec
    
    # From abaqus manual:
    # Section forces, moments, and transverse shear forces
    # SF1 Axial force.
    # SF2 Transverse shear force in the local 2-direction (not available for B23, B23H, B33, B33H).
    # SF3 Transverse shear force in the local 1-direction (available only for beams in space, not available for B33, B33H).
    # SM1 Bending moment about the local 1-axis.
    # SM2 Bending moment about the local 2-axis (available only for beams in space).
    # SM3 Twisting moment about the beam axis (available only for beams in space).

#%%

def exportelconn(odb_id):
    
    '''
    Export element connectivity (which elements are connected to which nodes)
    
    Arguments
    ------------
    odb_id (odb object): odb file identifier
    
    Returns
    ------------
    # elconn: matrix with rows [Elno,Nodeno_start,Nodeno_end]
    
    '''
    
    t_start=timer()

    instance_keys=odb_id.rootAssembly.instances.keys()
    
    for k in range(len(instance_keys)):
        
        instance_id=odb_id.rootAssembly.instances[instance_keys[k]]
        instance_elements=instance_id.elements
        
        eltype=[instance_elements[j].type for j in range(len(instance_elements))]
        
        idx_B31 = [i for i, s in enumerate(eltype) if 'B31' in s]
        idx_B33 = [i for i, s in enumerate(eltype) if 'B33' in s]
        idx_B32 = [i for i, s in enumerate(eltype) if 'B32' in s]
        
        elconn_B31=np.array( [ [instance_elements[j].label , int(instance_elements[j].connectivity[0]) , int(instance_elements[j].connectivity[1]) ]  for j in idx_B31 ] )
        elconn_B33=np.array( [ [instance_elements[j].label , int(instance_elements[j].connectivity[0]) , int(instance_elements[j].connectivity[1]) ]  for j in idx_B33 ] )
        elconn_B32=np.array( [ [instance_elements[j].label , int(instance_elements[j].connectivity[0]) , int(instance_elements[j].connectivity[1]) , int(instance_elements[j].connectivity[2]) ]  for j in idx_B32 ] )

    # If empty, then set shape to 3 or 4 columns
    if idx_B31==[]:
        elconn_B31=np.array([]).reshape(0,3)
    
    if idx_B33==[]:
        elconn_B33=np.array([]).reshape(0,3)
    
    if idx_B32==[]:
        elconn_B32=np.array([]).reshape(0,4)
        
    # Delete middle node for 3 node element
    elconn_B32_del=np.delete(elconn_B32,2,1)
    
    elconn=np.vstack((elconn_B31,elconn_B33,elconn_B32_del))
    
    t_end=timer()
    print('Time elconn ' + str(t_end-t_start))
    
    return elconn

#%%

def exportelsets(odb_id):
    
    '''
    Export element sets
    
    Arguments
    ------------
    odb_id (odb object): odb file identifier
    
    Returns
    ------------
    elset_numbers: vector with set number (separated by 0 between each set)
    elset_names: list with names
    
    '''
    
    instance_keys=odb_id.rootAssembly.instances.keys()
    elset_numbers=[]
    elset_names=[]
    
    t_start=timer()
    for k in range(len(instance_keys)):

        instance_id=odb_id.rootAssembly.instances[instance_keys[k]]
        elset_keys=instance_id.elementSets.keys()
        elset_names=np.append(elset_names,elset_keys)
        
        for i in range(len(elset_keys)):
            
            el_temp=instance_id.elementSets[elset_keys[i]].elements
            elnumbers_temp=[el_temp[ii].label for ii in range(len(el_temp))]
            elset_numbers=np.append(elset_numbers,np.append(elnumbers_temp,0))
            
    t_end=timer()
    print('Time elsets ' + str(t_end-t_start))
    return elset_numbers,elset_names
    
#%%

def save2txt(folder_save,name_save,A_matrix,atype='string',prefix=''):
    
    '''
    Export element sets
    
    Arguments
    ------------
    folder_save: string with folder name for export
    name_save: string with name for export
    A_matrix: the array to export
    atype: 'string' or 'number' specifies text or numeric data
    prefix: prefix in front of name_save
    
    Returns
    ------------
    None
    
    '''
    
    if atype=='number' or atype==1:
        np.savetxt((folder_save+'\\'+prefix+name_save+'.txt'),A_matrix ,delimiter=',',fmt='%.6e')
    elif atype=='string' or atype==2:
        np.savetxt((folder_save+'\\'+prefix+name_save+'.txt'),A_matrix ,delimiter=' ',fmt='%s')
    
#%%

def save2npy(folder_save,name_save,A_matrix,prefix=''):

    # Save numeric array or string array to npy file
    
    # Inputs:
    # folder_save: string with folder name for export
    # name_save: string with name for export
    # A_matrix: the array to export
    # prefix: prefix in front of name_save
    
    np.save((folder_save+'\\'+prefix+name_save),A_matrix)
    
