# -*- coding: utf-8 -*-                       
from sys import path
import numpy as np
import odbAccess
import os
from textRepr import *
from timeit import default_timer as timer

def p(pstring):
    prettyPrint(pstring)


###################################              
#USER INPUT    
###################################     

# Folder of ODB-file
dir_odb='C:\\Temp'

# Folder of exported files
dir_export='C:\\Temp'

# Name of job (odb-file)
JobName='SB_TempJob_1'

# Step of modal analysis (default -1 aka last step)
FrequencyStepNumber=-1

# Prefix in front of exported filenames (default empty)
OutputPrefix=''

# Name of assembly (if empty, then automatically select first)
AssemblyName=''

# Export all to txt files rather than npy files (required for ABAQUS2019!)
ExportToTXT=False

###################################              
#START EXPORT BELOW            
###################################     

# OPEN ODB
if JobName[-4:]=='.odb':
    odbJobName=JobName+'.odb'
else:
    odbJobName=JobName+'.odb'
    

myOdb=odbAccess.openOdb(dir_odb+'\\'+odbJobName)

#%%

def ExportHistoryOutput(myOdb,StepNumber,hist_str,AssemblyName=''):

    #EIGFREQ,DAMPRATIO,EIGREAL,EIGIMAG,GM
    
    StepNames=myOdb.steps.keys()
    NameOfStep=StepNames[StepNumber]
    
    if AssemblyName=='':
        AssemblyNameKeys=myOdb.steps[NameOfStep].historyRegions.keys()
        AssemblyName=AssemblyNameKeys[0]
    
    HistoryOutputKeys=myOdb.steps[NameOfStep].historyRegions[AssemblyName].historyOutputs.keys()
    
    if hist_str not in HistoryOutputKeys:
        OutputVector=np.array([0])
        return OutputVector
    else:
        HistoryOutput=myOdb.steps[NameOfStep].historyRegions[AssemblyName].historyOutputs[hist_str]
        
    OutputVector=np.array([HistoryOutput.data[j][1] for j in range(0,len(HistoryOutput.data))])
    
    return OutputVector
    
#%%

def Export_U_UR(myOdb,StepNumber,FrameNumber=''):

    StepNames=myOdb.steps.keys()
    NameOfStep=StepNames[StepNumber]
    SelectedStep=myOdb.steps[NameOfStep]
    
    if FrameNumber=='':
        FrameNumber=range(len(SelectedStep.frames))
    
    SelectedFrame=SelectedStep.frames[-1]
    if not SelectedFrame.fieldOutputs.has_key('U'):
        DisplacementMatrix=np.array([0])
        return DisplacementMatrix
    
    N_node=len(SelectedFrame.fieldOutputs['U'].values)          
    N_frame=len(FrameNumber)    
    
    DisplacementMatrix=np.zeros((N_node*6,N_frame))
    
    t_start=timer()
    for z in np.arange(len(FrameNumber)):
        
        SelectedFrame=SelectedStep.frames[FrameNumber[z]]
        
        OutputTrans=SelectedFrame.fieldOutputs['U']
        OutputTransValues=OutputTrans.values
        
        OutputRot=SelectedFrame.fieldOutputs['UR']
        OutputRotValues=OutputRot.values
        
        U_temp=np.array([OutputTransValues[n].data for n in range(N_node) ])
        UR_temp=np.array([OutputRotValues[n].data for n in range(N_node) ])
        
        Displacement_temp=np.hstack((U_temp,UR_temp)).flatten()
        DisplacementMatrix[:,z]=Displacement_temp
    
    LabelVectorTemp=[ [str(OutputTransValues[n].nodeLabel) + '_' + s  for s in OutputTrans.componentLabels] + [str(OutputRotValues[n].nodeLabel) + '_' + s  for s in OutputRot.componentLabels] for n in range(N_node) ]
    LabelVector=[item for sublist in LabelVectorTemp for item in sublist]
    
    t_end=timer()
    print('Time displacement ' + str(t_end-t_start) + ' s')
    return DisplacementMatrix

#%%

def Export_NodeCoord(myOdb,StepNumber,FrameNumber):

    StepNames=myOdb.steps.keys()
    NameOfStep=StepNames[StepNumber]
    SelectedStep=myOdb.steps[NameOfStep]
            
    SelectedFrame=SelectedStep.frames[FrameNumber]
    if 'COORD' not in SelectedFrame.fieldOutputs.keys():
        NodeCoordMatrix=np.array([0 , 0 , 0])
        NodeCoordLabelVector=np.array([0])
        return NodeCoordMatrix,NodeCoordLabelVector
        
    t_start=timer()
    CoordValues=SelectedFrame.fieldOutputs['COORD'].values
    NodeCoordMatrix=np.array([CoordValues[ii].data for ii in range(len(CoordValues))])
    NodeCoordLabelVector=np.array([CoordValues[ii].nodeLabel for ii in range(len(CoordValues))])
    t_end=timer()
    print('Time nodecoord ' + str(t_end-t_start) + ' s')
    
    return NodeCoordMatrix,NodeCoordLabelVector
        
    t_start=timer()

#%%

def Export_SectionForce(myOdb,StepNumber,FrameNumber=''):
    
    StepNames=myOdb.steps.keys()
    NameOfStep=StepNames[StepNumber]
    SelectedStep=myOdb.steps[NameOfStep]
    
    if FrameNumber=='':
        FrameNumber=range(len(SelectedStep.frames))
    
    SelectedFrame=SelectedStep.frames[-1]
    if 'SF' not in SelectedFrame.fieldOutputs.keys():
        SectionForceMatrix=np.array([0 , 0 , 0])
        ElementLabelVector=np.array(['SF_not_found'])
        return SectionForceMatrix,ElementLabelVector
    
    N_frame=len(FrameNumber)
    
    ElementLabelAll=[ SelectedFrame.fieldOutputs['SF'].values[n].baseElementType for n in range(len(SelectedFrame.fieldOutputs['SF'].values)) ]
    index_B=[n for n, l in enumerate(ElementLabelAll) if l.startswith('B')]
        
    SectionForceMatrix=np.zeros((len(index_B)*6,N_frame))
    
    for z in np.arange(len(FrameNumber)):
        
        SelectedFrame=SelectedStep.frames[FrameNumber[z]]
        
        OutputSF=SelectedFrame.fieldOutputs['SF']
        OutputSFValues=OutputSF.values
        
        OutputSM=SelectedFrame.fieldOutputs['SM']
        OutputSMValues=OutputSM.values
        
        SF_temp=np.array([OutputSFValues[n].data for n in index_B ])
        SM_temp=np.array([OutputSMValues[n].data for n in index_B ])
        
        Output_SF_temp=np.hstack((SF_temp,SM_temp)).flatten()
        SectionForceMatrix[:,z]=Output_SF_temp
        
    SF_ComponentLabels=OutputSF.componentLabels
    SM_componentLabels=('SM1', 'SM2', 'SM3') 
    # Error in abaqus documentation? States 2 1 3 in odb, but that is wrong
    # OutputSM.componentLabels
    # ('SM2', 'SM1', 'SM3')    
    
    ElementLabelVectorTemp=[ [str(OutputSFValues[n].elementLabel) + '_' + s  for s in SF_ComponentLabels] + [str(OutputSMValues[n].elementLabel) + '_' + s  for s in SM_componentLabels] for n in index_B ]
    ElementLabelVector=[item for sublist in ElementLabelVectorTemp for item in sublist]
    
    return SectionForceMatrix,ElementLabelVector
    
    # Section forces, moments, and transverse shear forces
    # SF1 Axial force.
    # SF2 Transverse shear force in the local 2-direction (not available for B23, B23H, B33, B33H).
    # SF3 Transverse shear force in the local 1-direction (available only for beams in space, not available for B33, B33H).
    # SM1 Bending moment about the local 1-axis.
    # SM2 Bending moment about the local 2-axis (available only for beams in space).
    # SM3 Twisting moment about the beam axis (available only for beams in space).

#%%

def Export_ElConnectivity(myOdb,StepNumber,FrameNumber)

    t_start=timer()

    InstanceKeys=myOdb.rootAssembly.instances.keys()
    
    for k in range(len(InstanceKeys)):

        SelectedInstance=myOdb.rootAssembly.instances[InstanceKeys[k]]
        SelectedInstanceElements=SelectedInstance.elements
        
        ElType=[SelectedInstanceElements[j].type for j in range(len(SelectedInstanceElements))]
        
        Index_B31 = [i for i, s in enumerate(ElType) if 'B31' in s]
        Index_B33 = [i for i, s in enumerate(ElType) if 'B33' in s]
        Index_B32 = [i for i, s in enumerate(ElType) if 'B32' in s]
        
        ElementConnectivity_B31=np.array( [ [SelectedInstanceElements[j].label , int(SelectedInstanceElements[j].connectivity[0]) , int(SelectedInstanceElements[j].connectivity[1]) ]  for j in Index_B31 ] )
        ElementConnectivity_B33=np.array( [ [SelectedInstanceElements[j].label , int(SelectedInstanceElements[j].connectivity[0]) , int(SelectedInstanceElements[j].connectivity[1]) ]  for j in Index_B33 ] )
        ElementConnectivity_B32=np.array( [ [SelectedInstanceElements[j].label , int(SelectedInstanceElements[j].connectivity[0]) , int(SelectedInstanceElements[j].connectivity[1]) , int(SelectedInstanceElements[j].connectivity[2]) ]  for j in Index_B32 ] )
        
    t_end=timer()
    print('Time #ELEMENTS ' + str(t_end-t_start))

#%%

def Export_ElSets(myOdb,StepNumber,FrameNumber)

    InstanceKeys=myOdb.rootAssembly.instances.keys()
    ElementSetNumbers=[]
    ElementSetNames=[]
    
    t_start=timer()
    for k in range(len(InstanceKeys)):

        SelectedInstance=myOdb.rootAssembly.instances[InstanceKeys[k]]
        ElementSetKeys=SelectedInstance.elementSets.keys()
        ElementSetNames=np.append(ElementSetNames,ElementSetKeys)
        
        for i in range(len(ElementSetKeys_temp)):
            
            Elements=SelectedInstance.elementSets[ElementSetKeys[i]].elements
            ElementNumbers_temp=[Elements[ii].label for ii in range(len(Elements))]
            ElementNumbers_temp=np.append(ElementNumbers_temp,0)
            ElementSetNumbers=np.append(ElementSetNumbers,ElementNumbers_temp)
            
    t_end=timer()
    print('Time #ELEMENT SETS ' + str(t_end-t_start))
    return ElementSetNumbers,ElementSetNames
    
def SaveToTXT(dir_save,name_save,OutputPrefix,atype,A_matrix):
    
    # Inputs:
    # dir_save: string 
    # name_save: string 
    # OutputPrefix: string 
    # atype: string 
    # A_matrix: numpy array
    
    if atype=='number':
        np.savetxt((dir_save+'\\'+OutputPrefix+name_save+'.txt'), A_matrix , delimiter=',') 
    elif atype=='string':
        np.savetxt((dir_save+'\\'+OutputPrefix+name_save+'.txt'), A_matrix , delimiter=' ', fmt='%s')
    

def SaveToNPY(dir_save,name_save,OutputPrefix,A_matrix):
    
    # Inputs:
    # dir_save: string 
    # name_save: string 
    # OutputPrefix: string 
    # A_matrix: numpy array
    
    np.save((dir_save+'\\'+OutputPrefix+name_save), A_matrix)
    
##############################################################################################
##############################################################################################
# OLD
# OLD
# OLD
##############################################################################################
##############################################################################################

###################################
#EXPORT
###################################



# OutputPrefix=''
t_start=timer()

# ADD PREFIX
if OutputPrefix=='none':
    OutputPrefix=''
    

if FrequencyExport:
    if ExportToTXT==True:
        FunctionSaveToTXT(dir_export,'freq',OutputPrefix,'number',FrequencyVector)
    else:
        FunctionSaveToNPY(dir_export,'freq',OutputPrefix,FrequencyVector)


if DampingExport:
    if ExportToTXT==True:
        FunctionSaveToTXT(dir_export,'damp',OutputPrefix,'number',DampingVector)
    else:
        FunctionSaveToNPY(dir_export,'damp',OutputPrefix,DampingVector)

if EigrealExport:
    if ExportToTXT==True:
        FunctionSaveToTXT(dir_export,'eigreal',OutputPrefix,'number',EigrealVector)
    else:
        FunctionSaveToNPY(dir_export,'eigreal',OutputPrefix,EigrealVector)

if EigimagExport:
    if ExportToTXT==True:
        FunctionSaveToTXT(dir_export,'eigimag',OutputPrefix,'number',EigimagVector)
    else:    
        np.save((dir_export+'\\'+OutputPrefix+'eigimag'), EigimagVector)
        FunctionSaveToNPY(dir_export,'eigimag',OutputPrefix,EigimagVector)

if GenmassExport:
    if ExportToTXT==True:
        FunctionSaveToTXT(dir_export,'genmass',OutputPrefix,'number',GenmassVector)
    else:
        FunctionSaveToNPY(dir_export,'genmass',OutputPrefix,GenmassVector)

if PhiExport:
    if ExportToTXT==True:
        FunctionSaveToTXT(dir_export,'phi',OutputPrefix,'number',ModeshapeMatrix)
    else:    
        FunctionSaveToNPY(dir_export,'phi',OutputPrefix,ModeshapeMatrix)
    
    FunctionSaveToTXT(dir_export,'phi_label',OutputPrefix,'string',PhiLabelVector)


if PhiConjExport:
    if ExportToTXT==True:
        FunctionSaveToTXT(dir_export,'phi_conj',OutputPrefix,'number',ModeshapeConjMatrix)
    else:    
        FunctionSaveToNPY(dir_export,'phi_conj',OutputPrefix,ModeshapeConjMatrix)


if PhiSFExport:
    if ExportToTXT==True:
        FunctionSaveToTXT(dir_export,'phi_sf',OutputPrefix,'number',ModeSectionForceMatrix)
    else:    
        FunctionSaveToNPY(dir_export,'phi_sf',OutputPrefix,ModeSectionForceMatrix)
    
    FunctionSaveToTXT(dir_export,'phi_sf_label',OutputPrefix,'string',ElementLabelVector)
    

if NodeCoordExport:
    if ExportToTXT==True:
        FunctionSaveToTXT(dir_export,'nodecoord',OutputPrefix,'number',NodeCoordMatrix)
        FunctionSaveToTXT(dir_export,'nodecoord_label',OutputPrefix,'number',NodeCoordLabelVector)
    else:    
        FunctionSaveToNPY(dir_export,'nodecoord',OutputPrefix,NodeCoordMatrix)
        FunctionSaveToNPY(dir_export,'nodecoord_label',OutputPrefix,NodeCoordLabelVector)


if SFExport:
    if ExportToTXT==True:
        FunctionSaveToTXT(dir_export,'SF',OutputPrefix,'number',SF_Matrix)
        FunctionSaveToTXT(dir_export,'SM',OutputPrefix,'number',SM_Matrix)
    else:
        FunctionSaveToNPY(dir_export,'SF',OutputPrefix,SF_Matrix)
        FunctionSaveToNPY(dir_export,'SM',OutputPrefix,SM_Matrix)
    
    FunctionSaveToTXT(dir_export,'SF_label',OutputPrefix,'string',ElementLabelVector_SF)
    FunctionSaveToTXT(dir_export,'SM_label',OutputPrefix,'string',ElementLabelVector_SM)

if ElementConnectivityExport:
    if ExportToTXT==True:
        FunctionSaveToTXT(dir_export,'ElementConnectivity2Node',OutputPrefix,'number',ElementConnectivity2NodeMatrix)
        FunctionSaveToTXT(dir_export,'ElementConnectivity3Node',OutputPrefix,'number',ElementConnectivity3NodeMatrix)
    else:
        FunctionSaveToNPY(dir_export,'ElementConnectivity2Node',OutputPrefix,ElementConnectivity2NodeMatrix)
        FunctionSaveToNPY(dir_export,'ElementConnectivity3Node',OutputPrefix,ElementConnectivity3NodeMatrix)
        
    

if ElementSetExport:
    if ExportToTXT==True:
        FunctionSaveToTXT(dir_export,'ElementSetNumbers',OutputPrefix,'number',ElementSetNumbers)
    else:
        FunctionSaveToNPY(dir_export,'ElementSetNumbers',OutputPrefix,ElementSetNumbers)
        
    FunctionSaveToTXT(dir_export,'ElementSetNames',OutputPrefix,'string',ElementSetNames)
    

t_end=timer()
print('Time #EXPORT ' + str(t_end-t_start))


###################################
#CLOSE
###################################

myOdb.close()
    
#sys.exit(0)


################################################################
################################################################
################################################################
################################################################
################################################################
################################################################
