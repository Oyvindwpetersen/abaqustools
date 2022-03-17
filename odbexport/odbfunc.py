# -*- coding: utf-8 -*-                       
from sys import path
import numpy as np
import odbAccess
import os
from textRepr import *
from timeit import default_timer as timer

def p(pstring):
    prettyPrint(pstring)



# This file is imported in Abaqus by "import odbfunc"


#%%

def OpenODB(FolderODB,JobName):

    # Inputs:
    # FolderODB: string with folder name
    # JobName: string with job name
    
    # Outputs:
    # myOdb: ODB object

    # Open ODB
    if JobName[-4:]=='.odb':
        JobName=JobName
    else:
        JobName=JobName+'.odb'
        
    myOdb=odbAccess.openOdb(FolderODB+'\\'+JobName)
    return myOdb

def CloseODB(myOdb):

    # Inputs:
    # myOdb: ODB object

    myOdb.close()

#%%

def Export_HistoryOutput(myOdb,StepNumber,hist_str,AssemblyName=''):

    # Inputs:
    # myOdb: ODB object
    # StepNumber: step number for export, usually -1
    # hist_str: string with desired quantity, e.g. EIGFREQ,GM,DAMPRATIO,EIGREAL,EIGIMAG
    
    # Outputs:
    # OutputVector: vector with numbers

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

    # Inputs:
    # myOdb: ODB object
    # StepNumber: step number for export, usually -1
    # FrameNumber: frame number for export, '' gives all frames in skip, 'skipfirst' gives all except frame 0
    
    # Outputs:
    # DisplacementMatrix: matrix with each frame as column ( e.g. N_DOF*N_MODES)
    # LabelVector: list with DOF labels of all NDOF

    StepNames=myOdb.steps.keys()
    NameOfStep=StepNames[StepNumber]
    SelectedStep=myOdb.steps[NameOfStep]
    
    if FrameNumber=='':
        FrameNumber=range(len(SelectedStep.frames))
    elif FrameNumber=='skipfirst':
        FrameNumber=range(1,len(SelectedStep.frames))
    elif isinstance(FrameNumber,int):
        FrameNumber=np.array([FrameNumber])
        
        
    SelectedFrame=SelectedStep.frames[-1]
    if not SelectedFrame.fieldOutputs.has_key('U'):
        DisplacementMatrix=np.array([0])
        LabelVector=np.array([0])
        return DisplacementMatrix,LabelVector
    
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
    return DisplacementMatrix,LabelVector

#%%

def Export_NodeCoord(myOdb,StepNumber,FrameNumber):

    # Inputs:
    # myOdb: ODB object
    # StepNumber: step number for export, usually -1
    # FrameNumber: frame number for export, usually 0
    
    # Outputs:
    # NodeCoordMatrix: matrix with [x,y,z] as rows, size N_NODE*3
    # NodeCoordLabelVector: vector with node numbers

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
    NodeCoordLabelVector=np.zeros((np.shape(NodeCoordMatrix)[0],1))
    NodeCoordLabelVector[:,0]=np.array([CoordValues[ii].nodeLabel for ii in range(len(CoordValues))])
    
    t_end=timer()
    print('Time nodecoord ' + str(t_end-t_start) + ' s')
    
    NodeCoord=np.hstack((NodeCoordLabelVector,NodeCoordMatrix))
    
    return NodeCoord
        
#%%

def Export_SectionForce(myOdb,StepNumber,FrameNumber=''):

    # Inputs:
    # myOdb: ODB object
    # StepNumber: step number for export, usually -1
    # FrameNumber: frame number for export, '' gives all frames in skip, 'skipfirst' gives all except frame 0
    
    # Outputs:
    # SectionForceMatrix: matrix with each frame as column ( e.g. N_SF*N_MODES)
    # ElementLabelVector: list with SF labels

    StepNames=myOdb.steps.keys()
    NameOfStep=StepNames[StepNumber]
    SelectedStep=myOdb.steps[NameOfStep]
    
    if FrameNumber=='':
        FrameNumber=range(len(SelectedStep.frames))
    elif FrameNumber=='skipfirst':
        FrameNumber=range(1,len(SelectedStep.frames))
    elif isinstance(FrameNumber,int):
        FrameNumber=np.array([FrameNumber])
    
    SelectedFrame=SelectedStep.frames[-1]
    if 'SF' not in SelectedFrame.fieldOutputs.keys():
        SectionForceMatrix=np.array([0 , 0 , 0])
        ElementLabelVector=np.array(['SF_not_found'])
        return SectionForceMatrix,ElementLabelVector
    
    ElementLabelAll=[ SelectedFrame.fieldOutputs['SF'].values[n].baseElementType for n in range(len(SelectedFrame.fieldOutputs['SF'].values)) ]
    index_B=[n for n, l in enumerate(ElementLabelAll) if l.startswith('B')]
        
    SectionForceMatrix=np.zeros((len(index_B)*6,len(FrameNumber)))
    
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
    SM_ComponentLabels=('SM1', 'SM2', 'SM3') 
    # Error in abaqus documentation? States 2 1 3 in odb, but that is wrong
    # OutputSM.componentLabels
    # ('SM2', 'SM1', 'SM3')    
    
    ElementLabelVectorTemp=[ [str(OutputSFValues[n].elementLabel) + '_' + s  for s in SF_ComponentLabels] + [str(OutputSMValues[n].elementLabel) + '_' + s  for s in SM_ComponentLabels] for n in index_B ]
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

def Export_ElConnectivity(myOdb):

    # Inputs:
    # myOdb: ODB object
    
    # Outputs:
    # ElementConnectivity_B31: matrix with rows [Elno,Nodeno1,Nodeno2]
    # ElementConnectivity_B33: matrix with rows [Elno,Nodeno1,Nodeno2]
    # ElementConnectivity_B32: matrix with rows [Elno,Nodeno1,Nodeno2,Nodeno3]

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
    
    return ElementConnectivity_B31,ElementConnectivity_B33,ElementConnectivity_B32

#%%

def Export_ElSets(myOdb):
    
    # Inputs:
    # myOdb: ODB object
    
    # Outputs:
    # ElementSetNumbers: vector with set number (separated by 0 between each set)
    # ElementSetNames: list with names

    InstanceKeys=myOdb.rootAssembly.instances.keys()
    ElementSetNumbers=[]
    ElementSetNames=[]
    
    t_start=timer()
    for k in range(len(InstanceKeys)):

        SelectedInstance=myOdb.rootAssembly.instances[InstanceKeys[k]]
        ElementSetKeys=SelectedInstance.elementSets.keys()
        ElementSetNames=np.append(ElementSetNames,ElementSetKeys)
        
        for i in range(len(ElementSetKeys)):
            
            Elements=SelectedInstance.elementSets[ElementSetKeys[i]].elements
            ElementNumbers_temp=[Elements[ii].label for ii in range(len(Elements))]
            ElementNumbers_temp=np.append(ElementNumbers_temp,0)
            ElementSetNumbers=np.append(ElementSetNumbers,ElementNumbers_temp)
            
    t_end=timer()
    print('Time #ELEMENT SETS ' + str(t_end-t_start))
    return ElementSetNumbers,ElementSetNames
    
#%%

def SaveToTXT(FolderSave,NameSave,A_matrix,atype='string',Prefix=''):
    
    # Inputs:
    # FolderSave: string with folder name for export
    # NameSave: string with name for export
    # A_matrix: the quantity to export
    # atype: 'string' or 'number' specifies text or numeric data
    # Prefix: prefix in front of NameSave
    
    if atype=='number' or atype==1:
        np.savetxt((FolderSave+'\\'+Prefix+NameSave+'.txt'), A_matrix , delimiter=',', fmt='%.8e')
    elif atype=='string' or atype==2:
        np.savetxt((FolderSave+'\\'+Prefix+NameSave+'.txt'), A_matrix , delimiter=' ', fmt='%s')
    
#%%

def SaveToNPY(FolderSave,NameSave,A_matrix,Prefix=''):
    
    # Inputs:
    # FolderSave: string with folder name for export
    # NameSave: string with name for export
    # A_matrix: the quantity to export
    # Prefix: prefix in front of NameSave
    
    np.save((FolderSave+'\\'+OutputPrefix+NameSave), A_matrix)
    
