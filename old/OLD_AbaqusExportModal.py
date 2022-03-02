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
  
stepNames=myOdb.steps.keys()
nameOfFrequencyStep=stepNames[FrequencyStepNumber]
frequencyStep=myOdb.steps[nameOfFrequencyStep]

# STATIC OR FREQUENCY STEP
if myOdb.steps[nameOfFrequencyStep].procedure=='*STATIC':
    historyOutputKeys='NotRelevant'
    AssemblyName='NotRelevant'
elif myOdb.steps[nameOfFrequencyStep].procedure=='*FREQUENCY' or myOdb.steps[nameOfFrequencyStep].procedure=='*COMPLEX FREQUENCY':
    # FIND ASSEMBLY NAME IF NOT PROVIDED
    if AssemblyName=='' or AssemblyName=='none':
        AssemblyNameKeys=myOdb.steps[nameOfFrequencyStep].historyRegions.keys()
        AssemblyName=AssemblyNameKeys[0]
        
    historyOutputKeys=myOdb.steps[nameOfFrequencyStep].historyRegions[AssemblyName].historyOutputs.keys()
    

# NATURAL FREQUENCIES  

if 'EIGFREQ' in historyOutputKeys:  
    historyOutputFreq=myOdb.steps[nameOfFrequencyStep].historyRegions[AssemblyName].historyOutputs['EIGFREQ']
    if historyOutputFreq.data==None:
        FrequencyVector=np.array([0])
        FrequencyExport=False
        
    else:
        FrequencyVector=[historyOutputFreq.data[j] for j in range(0,len(historyOutputFreq.data))]
        FrequencyVector=np.array(FrequencyVector)[:,1]
        FrequencyExport=True
        
    
else:
    FrequencyVector=np.array([0])
    FrequencyExport=False
    

if 'DAMPRATIO' in historyOutputKeys:                   
    historyOutputDamp=myOdb.steps[nameOfFrequencyStep].historyRegions[AssemblyName].historyOutputs['DAMPRATIO']
    DampingVector=[historyOutputDamp.data[j] for j in range(0,len(historyOutputDamp.data))]
    DampingVector=np.array(DampingVector)[:,1]
    DampingExport=True
    
else:
    DampingVector=np.array([0])
    DampingExport=False
    

if 'EIGREAL' in historyOutputKeys:
    historyOutputEigreal=myOdb.steps[nameOfFrequencyStep].historyRegions[AssemblyName].historyOutputs['EIGREAL']
    EigrealVector=[historyOutputEigreal.data[j] for j in range(0,len(historyOutputEigreal.data))]
    EigrealVector=np.array(EigrealVector)[:,1]
    EigrealExport=True
else:
    EigrealVector=np.array([0])
    EigrealExport=False


if 'EIGIMAG' in historyOutputKeys:                  
    historyOutputEigimag=myOdb.steps[nameOfFrequencyStep].historyRegions[AssemblyName].historyOutputs['EIGIMAG']
    EigimagVector=[historyOutputEigimag.data[j] for j in range(0,len(historyOutputEigimag.data))]
    EigimagVector=np.array(EigimagVector)[:,1]
    EigimagExport=True
else:
    EigimagVector=np.array([0])              
    EigimagExport=False
    

if 'GM' in historyOutputKeys:              
    historyOutputGenmass=myOdb.steps[nameOfFrequencyStep].historyRegions[AssemblyName].historyOutputs['GM']
    GenmassVector=[historyOutputGenmass.data[j] for j in range(0,len(historyOutputGenmass.data))]
    GenmassVector=np.array(GenmassVector)[:,1]
    GenmassExport=True
else:
    GenmassVector=np.array([0])
    GenmassExport=False
    

###################################              
#MODE SHAPES              
###################################              
# t_start=timer()

# PhiExport=True
             
# numZ=len(frequencyStep.frames)
# frequencyFrame=frequencyStep.frames[1]
# numN=len(frequencyFrame.fieldOutputs['U'].values)          

# ModeshapeMatrix=np.zeros((numN*6,numZ))
# ModeshapeConjMatrix=np.zeros((numN*6,numZ))

# PhiLabelVector=[]; 
# for z in range(len(frequencyStep.frames)): #for each mode
    
    # frequencyFrame=frequencyStep.frames[z]
    
    # modeTrans=frequencyFrame.fieldOutputs['U']
    # modeTransValues=modeTrans.values
    # IndexU=np.array([0, 1, 2])
    
    # modeRot=frequencyFrame.fieldOutputs['UR']
    # modeRotValues=modeRot.values
    # IndexUR=np.array([0, 1, 2])+np.array([3, 3, 3])
    
    
    # if modeTransValues[0].conjugateData==None: # Check if conjugate data is relevant (imaginary mode, rarely used)
        # PhiConjExport=False
    # else:
        # PhiConjExport=True
    
    # for n in range(len(frequencyFrame.fieldOutputs['U'].values)): #for each node

        # phiZ_nodeN_U=modeTransValues[n].data
        # ModeshapeMatrix[IndexU,z]=phiZ_nodeN_U
        
        # phiZ_nodeN_UR=modeRotValues[n].data
        # ModeshapeMatrix[IndexUR,z]=phiZ_nodeN_UR
                
        # if PhiConjExport==True:
        
            # phiZ_nodeN_U_conj=modeTransValues[n].conjugateData
            # ModeshapeConjMatrix[IndexU,z]=phiZ_nodeN_U_conj
            
            # phiZ_nodeN_UR_conj=modeRotValues[n].conjugateData
            # ModeshapeConjMatrix[IndexUR,z]=phiZ_nodeN_UR_conj
        
        # IndexU=IndexU+6
        # IndexUR=IndexUR+6   
        
        # if z==0: 
            # PhiLabelVectorN=[str(modeTransValues[n].nodeLabel) + '_' + s  for s in modeTrans.componentLabels] + [str(modeRotValues[n].nodeLabel) + '_' + s  for s in modeRot.componentLabels]
            # PhiLabelVector.extend(PhiLabelVectorN)
        

# ModeshapeMatrix=ModeshapeMatrix[:,1:] #cut zero mode
# ModeshapeConjMatrix=ModeshapeConjMatrix[:,1:] #cut zero mode 
# PhiLabelVector=np.array(PhiLabelVector).flatten()

# t_end=timer()
# print('Time #MODE SHAPES ' + str(t_end-t_start))

###################################              
#MODE SHAPES (new)
###################################              
t_start=timer()

PhiExport=True
PhiConjExport=False

numZ=len(frequencyStep.frames)
frequencyFrame=frequencyStep.frames[1]
numN=len(frequencyFrame.fieldOutputs['U'].values)          

ModeshapeMatrix=np.zeros((numN*6,numZ))
ModeshapeConjMatrix=np.zeros((numN*6,numZ))

for z in range(len(frequencyStep.frames)): #for each mode
    
    frequencyFrame=frequencyStep.frames[z]
    
    modeTrans=frequencyFrame.fieldOutputs['U']
    modeTransValues=modeTrans.values
    
    modeRot=frequencyFrame.fieldOutputs['UR']
    modeRotValues=modeRot.values
    
    U_temp=[modeTransValues[n].data for n in range(len(frequencyFrame.fieldOutputs['U'].values)) ]
    U_temp=np.array(U_temp)
    
    UR_temp=[modeRotValues[n].data for n in range(len(frequencyFrame.fieldOutputs['UR'].values)) ]
    UR_temp=np.array(UR_temp)   
    
    phi_z_temp=np.hstack((U_temp,UR_temp)).flatten()
    ModeshapeMatrix[:,z]=phi_z_temp
    

PhiLabelVectorTemp=[ [str(modeTransValues[n].nodeLabel) + '_' + s  for s in modeTrans.componentLabels] + [str(modeRotValues[n].nodeLabel) + '_' + s  for s in modeRot.componentLabels] for n in range(len(frequencyFrame.fieldOutputs['U'].values)) ]
PhiLabelVector=[item for sublist in PhiLabelVectorTemp for item in sublist]

ModeshapeMatrix=ModeshapeMatrix[:,1:] #cut zero mode
ModeshapeConjMatrix=ModeshapeConjMatrix[:,1:] #cut zero mode 

t_end=timer()
print('Time #MODE SHAPES ' + str(t_end-t_start))

###################################
#MODE SECTION FORCES
###################################
# t_start=timer()


# frequencyFrame=frequencyStep.frames[0]
# PhiSFExport=False
# if 'SF' in frequencyFrame.fieldOutputs.keys():
    # PhiSFExport=True
    

# ModeSectionForceMatrix=np.array([0 , 0 , 0])
# ElementLabelVector=np.array(['none'])

# if PhiSFExport==True:
    # numZ=len(frequencyStep.frames)
    # frequencyFrame=frequencyStep.frames[1]
    # numN=len(frequencyFrame.fieldOutputs['SF'].values)
    
    # ModeSectionForceMatrix=np.zeros((numN*6,numZ))
    # ElementLabelVector=[]
    # for z in range(len(frequencyStep.frames)): #for each mode

        # frequencyFrame=frequencyStep.frames[z]
        # modeSF=frequencyFrame.fieldOutputs['SF']
        # modeSFValues=modeSF.values
        # modeSM=frequencyFrame.fieldOutputs['SM']
        # modeSMValues=modeSM.values
        
        # IndexA=np.array([0, 1, 2])
        
        # for n in range(len(frequencyFrame.fieldOutputs['SF'].values)): #for each node
            
            # if (modeSFValues[n].baseElementType=='B31')==False and (modeSFValues[n].baseElementType=='B32')==False:
                # continue
            
            # phiZ_nodeN_SF=modeSFValues[n].data
            # ModeSectionForceMatrix[IndexA,z]=phiZ_nodeN_SF
            # IndexA=IndexA+3
            
            # phiZ_nodeN_SM=modeSMValues[n].data
            # ModeSectionForceMatrix[IndexA,z]=phiZ_nodeN_SM
            # IndexA=IndexA+3
            
            # if z==0:
                # modeSM_componentLabels_replace=('SM1', 'SM2', 'SM3') # error in abaqus documentation? States 2 1 3
                # ElementLabelVectorN=[str(modeSFValues[n].elementLabel) + '_' + s  for s in modeSF.componentLabels] + [str(modeSMValues[n].elementLabel) + '_' + s  for s in modeSM_componentLabels_replace]
                # ElementLabelVector.extend(ElementLabelVectorN)
    
    # ModeSectionForceMatrix=ModeSectionForceMatrix[0:IndexA[0]:1,1:] #cut zero mode
    # ElementLabelVector=np.array(ElementLabelVector).flatten()

# t_end=timer()
# print('Time #MODAL SECTION FORCES ' + str(t_end-t_start))
###################################
#MODE SECTION FORCES (new)
###################################
t_start=timer()


frequencyFrame=frequencyStep.frames[0]
PhiSFExport=False
if 'SF' in frequencyFrame.fieldOutputs.keys():
    PhiSFExport=True
    

ModeSectionForceMatrix=np.array([0 , 0 , 0])
ElementLabelVector=np.array(['none'])

numZ=len(frequencyStep.frames)
frequencyFrame=frequencyStep.frames[1]

frequencyFrame=frequencyStep.frames[0]
ElementLabelAll=[ frequencyFrame.fieldOutputs['SF'].values[n].baseElementType for n in range(len(frequencyFrame.fieldOutputs['SF'].values)) ]
index_B=[n for n, l in enumerate(ElementLabelAll) if l.startswith('B')]

numN=len(index_B)
    
ModeSectionForceMatrix=np.zeros((numN*6,numZ))

for z in range(len(frequencyStep.frames)):
    
    frequencyFrame=frequencyStep.frames[z]
    
    modeSF=frequencyFrame.fieldOutputs['SF']
    modeSFValues=modeSF.values
    
    modeSM=frequencyFrame.fieldOutputs['SM']
    modeSMValues=modeSM.values
    
    SF_temp=[modeSFValues[n].data for n in index_B ]
    SF_temp=np.array(SF_temp)
    
    SM_temp=[modeSMValues[n].data for n in index_B ]
    SM_temp=np.array(SM_temp)
    
    phi_SF_z_temp=np.hstack((SF_temp,SM_temp)).flatten()
    ModeSectionForceMatrix[:,z]=phi_SF_z_temp
    
    

modeSM_componentLabels_replace=('SM1', 'SM2', 'SM3') # error in abaqus documentation? States 2 1 3
ElementLabelVectorTemp=[ [str(modeSFValues[n].elementLabel) + '_' + s  for s in modeSF.componentLabels] + [str(modeSMValues[n].elementLabel) + '_' + s  for s in modeSM_componentLabels_replace] for n in index_B ]
ElementLabelVector=[item for sublist in ElementLabelVectorTemp for item in sublist]

ModeSectionForceMatrix=ModeSectionForceMatrix[:,1:] #cut zero mode

t_end=timer()
print('Time #MODAL SECTION FORCES ' + str(t_end-t_start))
###################################
#NODE COORDINATES. EXTRACTION DONE AT CONFIG WHERE FREQUENCIES ARE CALCULATED
################################### 
t_start=timer()

initialFrame=frequencyStep.frames[0]
NodeCoordExport=False
if 'COORD' in initialFrame.fieldOutputs.keys():    
    NodeCoordExport=True

NodeCoordMatrix=np.array([0 , 0 , 0])
NodeCoordLabelVector=np.array([0 ])
if NodeCoordExport==True:
    coordValues=initialFrame.fieldOutputs['COORD'].values
    
    NodeCoordMatrix=[coordValues[ii].data for ii in range(len(coordValues))]
    NodeCoordLabelVector=[coordValues[ii].nodeLabel for ii in range(len(coordValues))]
    NodeCoordMatrix=np.array(NodeCoordMatrix)


t_end=timer()
print('Time NODE COORDINATES ' + str(t_end-t_start))

###################################
# SECTION FORCES AT DEAD LOAD. EXTRACTION DONE AT CONFIG WHERE FREQUENCIES ARE CALCULATED
###################################
t_start=timer()

nameOfTensionStep=stepNames[FrequencyStepNumber]
tensionStep=myOdb.steps[nameOfTensionStep]    
tensionFrame=tensionStep.frames[0] 

SF_Matrix=np.array([0 , 0 , 0])
SM_Matrix=np.array([0 , 0 , 0])
ElementLabelVector_SF=np.array([0])
ElementLabelVector_SM=np.array([0])

if 'SF' in tensionFrame.fieldOutputs.keys():       
    
    SFExport=True
    
    SF_SectionForces=tensionFrame.fieldOutputs['SF'].values
    elementLabelAll=[ SF_SectionForces[ii].elementLabel  for ii in range(len(SF_SectionForces))]
    # elementLabelAll=np.unique(elementLabelAll)
    
    # indexElementForceExport=[elementLabelAll.index(elementLabelForceExport[ii]) for ii in range(len(elementLabelAll))]
    indexElementForceExport=range(len(elementLabelAll))
    SF_Matrix=[SF_SectionForces[ii].data[0:3]  for ii in indexElementForceExport]
    SF_Matrix=np.array(SF_Matrix)
    
    SM_SectionForces=tensionFrame.fieldOutputs['SM'].values
    SM_Matrix=[SM_SectionForces[ii].data[0:3]  for ii in indexElementForceExport]
    SM_Matrix=np.array(SM_Matrix)
    
    # ELEMENTLABEL
    ElementLabelVector_SF=[ SF_SectionForces[ii].elementLabel  for ii in indexElementForceExport]
    ElementLabelVector_SF=np.array(ElementLabelVector_SF)
    
    ElementLabelVector_SM=[ SM_SectionForces[ii].elementLabel  for ii in indexElementForceExport]
    ElementLabelVector_SM=np.array(ElementLabelVector_SM).flatten()
    
    # PhiLabelVector=[ [ [str(SF_SectionForces[ii].elementLabel) + '_' + s  for s in fieldOutputSF.componentLabels] , [str(modeRot.values[ii].nodeLabel) + '_' + s  for s in modeRot.componentLabels] ] for ii in indexElementForceExport]
    # PhiLabelVector=np.array(PhiLabelVector).flatten()
    

t_end=timer()
print('Time #SF AT DEAD LOAD ' + str(t_end-t_start))

###################################              
# ELEMENTS CONNECTIVITY
###################################  
t_start=timer()

ElementConnectivityExport=True

ElementConnectivity2NodeMatrix=np.array([ [0 , 0 , 0 ],[0 , 0 , 0 ]])
ElementConnectivity3NodeMatrix=np.array([ [0 , 0 , 0 , 0],[0 , 0 , 0 , 0]])

InstanceKeys=myOdb.rootAssembly.instances.keys()

for k in range(len(InstanceKeys)):

    myInstance=myOdb.rootAssembly.instances[InstanceKeys[k]]
    myInstanceElements=myInstance.elements
    
    j_select=[]
    for j in range(len(myInstanceElements)):
        if myInstanceElements[j].type=='B31' or myInstanceElements[j].type=='B33':
            j_select.append(j)
    
    ElementConnectivity2NodeMatrix_temp=np.array( [ [myInstanceElements[j].label , int(myInstanceElements[j].connectivity[0]) , int(myInstanceElements[j].connectivity[1]) ]  for j in j_select ] )
    
    if len(ElementConnectivity2NodeMatrix_temp)>0:    
        ElementConnectivity2NodeMatrix=np.vstack((ElementConnectivity2NodeMatrix,ElementConnectivity2NodeMatrix_temp))
    
    j_select=[]
    for j in range(len(myInstanceElements)):
        if myInstanceElements[j].type=='B32':
            j_select.append(j)
    
    ElementConnectivity3NodeMatrix_temp=np.array( [ [myInstanceElements[j].label , int(myInstanceElements[j].connectivity[0]) , int(myInstanceElements[j].connectivity[1]) , int(myInstanceElements[j].connectivity[2]) ]  for j in j_select ] )
    
    if len(ElementConnectivity3NodeMatrix_temp)>0:    
        ElementConnectivity3NodeMatrix=np.vstack((ElementConnectivity3NodeMatrix,ElementConnectivity3NodeMatrix_temp))


ElementConnectivity2NodeMatrix=ElementConnectivity2NodeMatrix[2:,:] #cut dummy values 
ElementConnectivity3NodeMatrix=ElementConnectivity3NodeMatrix[2:,:] #cut dummy values 

t_end=timer()
print('Time #ELEMENTS ' + str(t_end-t_start))

###################################
#ELEMENT SETS
###################################
t_start=timer()

ElementSetExport=True
ElementSetNumbers=[]
ElementSetNames=[]
for k in range(len(InstanceKeys)):

    myInstance=myOdb.rootAssembly.instances[InstanceKeys[k]]
    elementSetKeys_temp=myInstance.elementSets.keys()
    ElementSetNames=np.append(ElementSetNames,elementSetKeys_temp)
    
    for i in range(len(elementSetKeys_temp)):
        
        Elements=myInstance.elementSets[elementSetKeys_temp[i]].elements
        ElementNumbers_temp=[Elements[ii].label for ii in range(len(Elements))]
        ElementNumbers_temp=np.append(ElementNumbers_temp,0)
        ElementSetNumbers=np.append(ElementSetNumbers,ElementNumbers_temp)
        
        
    

t_end=timer()
print('Time #ELEMENT SETS ' + str(t_end-t_start))


###################################
#EXPORT
###################################

def FunctionSaveToTXT(dir_save,name_save,OutputPrefix,atype,A_matrix):
    
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
    


def FunctionSaveToNPY(dir_save,name_save,OutputPrefix,A_matrix):
    
    # Inputs:
    # dir_save: string 
    # name_save: string 
    # OutputPrefix: string 
    # A_matrix: numpy array
    
    np.save((dir_export+'\\'+OutputPrefix+name_save), A_matrix)
    

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
